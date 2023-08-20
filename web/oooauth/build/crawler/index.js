const url = require("url");
const { v4: uuidv4 } = require("uuid");
const puppeteer = require("puppeteer");
const Redis = require("ioredis");
const connection = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
});

const USERNAME = process.env.USERNAME; // admin username
const PASSWORD = process.env.PASSWORD; // admin password
const SERVER_URL = process.env.SERVER_URL;

const crawl = async (query, ID) => {
  const browser = await puppeteer.launch({
    args: [
      "--no-sandbox",
      "--disable-background-networking",
      "--disk-cache-dir=/dev/null",
      "--disable-default-apps",
      "--disable-extensions",
      "--disable-gpu",
      "--disable-sync",
      "--disable-translate",
      "--hide-scrollbars",
      "--metrics-recording-only",
      "--mute-audio",
      "--no-first-run",
      "--safebrowsing-disable-auto-update",
    ],
  });
  const page = await browser.newPage();
  try {
    const targetURL = new url.URL(SERVER_URL);
    targetURL.pathname = "/auth";

    if (query) {
      const searchParams = new url.URLSearchParams(query);
      targetURL.search = searchParams.toString();
    }
    
    console.log("request url:", targetURL.toString());
    await page.goto(targetURL.toString(), {
        waitUntil: "networkidle2",
        timeout: 3000, 
    }); 
    await page.waitForSelector("input[name=username]");
    await page.type("input[name=username]", USERNAME);
    await page.type("input[name=password]", PASSWORD);
    await page.click("input[name=approved]");

    await page.waitForTimeout(1000);

    await page.close();
  } catch (err) {
    console.error("crawl", ID, err.message);
  } finally {
    await browser.close();
    console.log("crawl", ID, "browser closed");
  }
};

(async () => {
  while (true) {
    console.log(
      "[*] waiting new query",
      await connection.get("queued_count"),
      await connection.get("proceeded_count")
    );
    const ID = uuidv4();
    await connection
      .blpop("query", 0)
      .then((v) => {
        const path = v[1];
        console.log("crawl", ID, path);
        return crawl(path, ID);
      })
      .then(() => {
        console.log("crawl", ID, "finished");
        return connection.incr("proceeded_count");
      })
      .catch((e) => {
        console.log("crawl", ID, e);
      });
  }
})();