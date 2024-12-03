const express = require("express");
const puppeteer = require("puppeteer");
const app = express();
const PORT = 8000;

const FLAG = process.env.FLAG;
const BASE_URL = process.env.BASE_URL || "http://127.0.0.1";

app.use(express.json());

function sleep(s) {
    return new Promise((resolve) => setTimeout(resolve, s));
}

app.post("/visit", async (req, res) => {
    let { url } = req.body;
    if (!url) {
        return res.status(400).json({ error: "URL is required" });
    }

    if (!url.startsWith(BASE_URL)) {
        return res
            .status(400)
            .json({ error: `URL must start with ${BASE_URL}` });
    }

    let browser;
    try {
        browser = await puppeteer.launch({
            headless: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=800x600',
            ],
        });
        const page = await browser.newPage();

        await page.setCookie({
            name: "flag",
            value: FLAG,
            url: BASE_URL,
        });

        await page.goto(url, { waitUntil: "networkidle2", timeout: 9999 });

        await sleep(5000);

        await browser.close();
        res.json({ status: "success" });
    } catch (error) {
        console.error(`Error visiting page: ${error}`);
        res.status(500).json({ error: error.toString() });
    } finally {
        if (browser) {
            await browser.close();
        }
    }
});

app.listen(PORT, () => {
    console.log(`Bot service running on port ${PORT}`);
});
