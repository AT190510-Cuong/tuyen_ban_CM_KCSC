const express = require("express");
const cookieParser = require("cookie-parser");
const path = require("path");
const { initDB } = require("./models");
const router = require("./router");

const app = express();
const PORT = process.env.PORT || 80;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "static")));

app.set("view engine", "pug");
app.set("views", path.join(__dirname, "views"));

app.use("/", router);

app.use((err, req, res, next) => {
    console.error("Unhandled error:", err.stack);
    res.status(500).json({ message: "Internal server error" });
});

initDB()
    .then(() => {
        const server = app.listen(PORT, () => {
            console.log(`Server running on port ${PORT}`);
        });

        const shutdown = () => {
            console.log("Shutting down server...");
            server.close(() => {
                console.log("Server closed. Exiting process.");
                process.exit(0);
            });
        };

        process.on("SIGTERM", shutdown);
        process.on("SIGINT", shutdown);
    })
    .catch((err) => {
        console.error("Error starting the server:", err);
        process.exit(1);
    });

module.exports = app;
