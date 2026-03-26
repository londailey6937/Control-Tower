import puppeteer from "puppeteer";
const browser = await puppeteer.launch({
  headless: true,
  defaultViewport: { width: 1440, height: 2400 },
});
const page = await browser.newPage();
await page.goto("http://localhost:5200/", {
  waitUntil: "networkidle0",
  timeout: 15000,
});
// Scroll to the showcase section
await page.evaluate(() => document.getElementById("demo")?.scrollIntoView());
await new Promise((r) => setTimeout(r, 500));
await page.screenshot({ path: "/tmp/website-showcase.png", fullPage: false });
console.log("showcase screenshot saved");
await browser.close();
