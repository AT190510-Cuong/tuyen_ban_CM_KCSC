const express = require("express");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const pug = require("pug");
const { verifyJWT, signJWT } = require("./jwt_helpers");
const { getUserByUsername, createUser } = require("./models");
const { sanitizeUsername } = require("./sanitizer");
const { promises: fsPromises } = require("fs");

const router = express.Router();

function base64urlEncode(data) {
    return data.toString("base64url").replace(/=+$/, "");
}

function hashPassword(password) {
    return crypto.createHash("sha256").update(password).digest("hex");
}

router.get("/jwks.json", async (req, res) => {
    try {
        const publicKey = await fsPromises.readFile(path.join(__dirname, "..", "public_key.pem"), "utf8");
        const publicKeyObj = crypto.createPublicKey(publicKey);
        const publicKeyDetails = publicKeyObj.export({ format: "jwk" });

        const jwk = {
            kty: "RSA",
            n: base64urlEncode(Buffer.from(publicKeyDetails.n, "base64")),
            e: base64urlEncode(Buffer.from(publicKeyDetails.e, "base64")),
            alg: "RS256",
            use: "sig",
        };

        res.json({ keys: [jwk] });
    } catch (err) {
        res.status(500).json({ message: "Error generating JWK" });
    }
});

function getCurrentUser(req, res, next) {
    const token = req.cookies.token;

    if (token) {
        verifyJWT(token)
            .then((payload) => {
                req.user = payload.username;
                res.locals.user = req.user;
                next();
            })
            .catch(() => {
                req.user = null;
                res.locals.user = null;
                next();
            });
    } else {
        req.user = null;
        res.locals.user = null;
        next();
    }
}

router.get("/", getCurrentUser, (req, res) => {
    res.render("index", { title: "Home - Cat Club" });
});

router.get(["/register", "/login"], (req, res) => {
    res.render("login");
});

router.post("/login", async (req, res) => {
    const { username, password } = req.body;

    try {
        const user = await getUserByUsername(username);
        if (!user || hashPassword(password) !== user.hashed_password) {
            return res.render("login", { error: "Invalid username or password" });
        }

        const token = await signJWT({ username: user.username });
        res.cookie("token", token, { httpOnly: true });
        res.redirect("/");
    } catch (err) {
        res.render("login", { error: "Error during login. Please try again later." });
    }
});

router.post("/register", async (req, res) => {
    const { username, password } = req.body;

    try {
        sanitizeUsername(username);

        const userExists = await getUserByUsername(username);
        if (userExists) {
            return res.render("login", {
                error: "Username already exists. Please choose another.",
            });
        }

        const hashedPassword = hashPassword(password);
        const newUser = await createUser({ username, hashed_password: hashedPassword });

        const token = await signJWT({ username: newUser.username });
        res.cookie("token", token, { httpOnly: true });
        res.redirect("/");
    } catch (err) {
        if (err.name === "BadRequestError") {
            return res.render("login", { error: err.message });
        }

        res.render("login", { error: "Error during registration. Please try again later." });
    }
});

router.get("/cats", getCurrentUser, (req, res) => {
    if (!req.user) {
        return res.redirect("/login?error=Please log in to view the cat gallery");
    }

    const templatePath = path.join(__dirname, "views", "cats.pug");

    fs.readFile(templatePath, "utf8", (err, template) => {
        if (err) {
            return res.render("cats");
        }

        if (typeof req.user != "undefined") {
            template = template.replace(/guest/g, req.user);
        }

        const html = pug.render(template, {
            filename: templatePath,
            user: req.user,
        });

        res.send(html);
    });
});

router.get("/logout", (req, res) => {
    res.clearCookie("token");
    res.redirect("/");
});

router.use((err, req, res, next) => {
    res.status(500).json({ message: "Internal server error" });
});

module.exports = router;
