// This is an outline of the crawler's program when query parameters 
// are sent using the Report function of the authorization server(https://oooauth.beginners.seccon.games:3001/report).

const USERNAME = process.env.USERNAME; // admin username
const PASSWORD = process.env.PASSWORD; // admin password
const SERVER_URL = process.env.SERVER_URL;


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

const targetURL = new url.URL(SERVER_URL);
targetURL.pathname = "/auth";

// query: ex. ?response_type=code&...&scopes=email profile
if (query) {
    const searchParams = new url.URLSearchParams(query);
    targetURL.search = searchParams.toString();
}

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
await browser.close();