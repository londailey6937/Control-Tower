import puppeteer from "puppeteer";
const browser = await puppeteer.launch({
  headless: true,
  defaultViewport: { width: 1440, height: 900 },
});
const page = await browser.newPage();
await page.goto("http://localhost:5199/index.vite.html", {
  waitUntil: "networkidle0",
  timeout: 30000,
});
await page.waitForSelector(".tab-btn", { timeout: 10000 });
await new Promise((r) => setTimeout(r, 1000));
try {
  await page.waitForSelector("#wiz-demo", { timeout: 5000 });
  await page.click("#wiz-demo");
  await new Promise((r) => setTimeout(r, 2500));
} catch (e) {}
// Switch role to PMP to access FDA Comms tab
await page.evaluate(() => {
  window._setRole("pmp");
});
await new Promise((r) => setTimeout(r, 1500));
const btn = await page.waitForSelector('.tab-btn[data-tab="fda-comms"]', {
  timeout: 5000,
});
await page.evaluate((el) => {
  el.scrollIntoView({ inline: "center" });
  el.click();
}, btn);
await new Promise((r) => setTimeout(r, 800));
await page.screenshot({
  path: "/Users/londailey/arch-medical/public/screenshots/fda-comms.png",
});
console.log("fda-comms captured");
await browser.close();
