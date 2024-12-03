import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from urllib.parse import urlparse, urljoin
from app import db
from app.models import User, Note, LogEntry
from app.forms import LoginForm, RegisterForm, NoteForm, ContactForm, ReportForm
import logging
import requests
import threading
import uuid

main = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1')
BOT_URL = os.getenv('BOT_URL', 'http://bot:8000')

reporting_users = set()
reporting_lock = threading.Lock()


@main.route('/')
def index():
    # Change for remote infra deployment
    return render_template('home.html')


@main.route('/home')
def home():
    return render_template('home.html')


@main.route('/api/notes/fetch/<note_id>', methods=['GET'])
def fetch(note_id):
    note = Note.query.get(note_id)
    if note:
        return jsonify({'content': note.content, 'note_id': note.id})
    return jsonify({'error': 'Note not found'}), 404


@main.route('/api/notes/store', methods=['POST'])
@login_required
def store():
    data = request.get_json()
    content = data.get('content')

    # Since we removed the dangerous "debug" field, bleach is no longer needed - DOMPurify should be enough

    note = Note.query.filter_by(user_id=current_user.id).first()
    if note:
        note.content = content
    else:
        note = Note(user_id=current_user.id, content=content)
        db.session.add(note)

    db.session.commit()
    return jsonify({'success': 'Note stored', 'note_id': note.id})


# Monitor for suspicious activity
@main.route('/api/notes/log/<username>', methods=['POST'])
def log_note_access(username):
    data = request.get_json()
    note_id = data.get('note_id')
    content = data.get('content')

    if not note_id or not username or not content:
        return jsonify({"error": "Missing data"}), 400

    log_entry = LogEntry(note_id=note_id, username=username, content=content)
    db.session.add(log_entry)
    db.session.commit()

    return jsonify({"success": "Log entry created", "log_id": log_entry.id, "note_id": note_id}), 201


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            user = User(username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('main.home'))
    elif request.method == 'POST':
        flash('Registration Unsuccessful. Please check the errors and try again.', 'danger')
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(user_id=current_user.id, content=form.content.data)
        db.session.merge(note)
        db.session.commit()
        return redirect(url_for('main.view_note', note=note.id))
    return render_template('create.html', form=form)


@main.route('/view', methods=['GET'])
def view_note():
    note_id = request.args.get('note') or ''
    username = current_user.username if current_user.is_authenticated else 'Anonymouse'
    return render_template('view.html', note_id=note_id, username=username)


# People were exploiting an open redirect here, should be secure now!
@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('name')
            content = data.get('content')

            if not username or not content:
                return jsonify({"message": "Please provide both your name and message."}), 400

            return jsonify({"message": f'Thank you for your message, {username}. We will be in touch!'}), 200

        username = request.form.get('name')
        content = request.form.get('content')

        if not username or not content:
            flash('Please provide both your name and message.', 'danger')
            return redirect(url_for('main.contact'))

        return render_template('contact.html', msg=f'Thank you for your message, {username}. We will be in touch!')

    return render_template('contact.html', msg='Feel free to reach out to us using the form below. We would love to hear from you!')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


def call_bot(note_url, user_id):
    try:
        response = requests.post(f"{BOT_URL}/visit/", json={"url": note_url})
        if response.status_code == 200:
            logger.info('Bot visit succeeded')
        else:
            logger.error('Bot visit failed')
    finally:
        with reporting_lock:
            reporting_users.remove(user_id)


@main.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    form = ReportForm()
    if form.validate_on_submit():
        note_url = form.note_url.data
        parsed_url = urlparse(note_url)
        base_url_parsed = urlparse(BASE_URL)

        if not parsed_url.scheme.startswith('http'):
            flash('URL must begin with http(s)://', 'danger')
        elif parsed_url.netloc == base_url_parsed.netloc and parsed_url.path == '/view' and 'note=' in parsed_url.query:
            note_id = parsed_url.query[-36:]
            try:
                if uuid.UUID(note_id):
                    with reporting_lock:
                        if current_user.id in reporting_users:
                            flash(
                                'You already have a report in progress. Please respect our moderation capabilities.', 'danger')
                        else:
                            reporting_users.add(current_user.id)
                            threading.Thread(target=call_bot, args=(
                                note_url, current_user.id)).start()
                            flash('Note reported successfully', 'success')
            except ValueError:
                flash(
                    'Invalid note ID! Example format: 12345678-abcd-1234-5678-abc123def456', 'danger')
        else:
            logger.warning(f"Invalid URL provided: {note_url}")
            flash('Please provide a valid note URL, e.g. ' + BASE_URL +
                  '/view?note=12345678-abcd-1234-5678-abc123def456', 'danger')

        return redirect(url_for('main.report'))

    return render_template('report.html', form=form)
