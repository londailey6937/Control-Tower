#!/usr/bin/env node
/**
 * Capture screenshots of Predicate Finder and FDA Guidance Docs
 * from the live Control Tower deployment.
 * Outputs to arch-medical/public/screenshots/
 */
import puppeteer from "puppeteer";
import { mkdirSync } from "fs";
import { join } from "path";

const OUT = "/Users/londailey/arch-medical/public/screenshots";
mkdirSync(OUT, { recursive: true });

async function main() {
  const browser = await puppeteer.launch({
    headless: true,
    defaultViewport: { width: 1440, height: 900 },
  });

  // ── Predicate Finder ──
  console.log("Capturing Predicate Finder...");
  const pfPage = await browser.newPage();
  await pfPage.goto("https://ct.510kbridge.com/predicate-finder/", {
    waitUntil: "networkidle0",
    timeout: 30000,
  });
  await new Promise((r) => setTimeout(r, 2000));
  await pfPage.screenshot({
    path: join(OUT, "predicate-finder.png"),
    fullPage: false,
  });
  console.log("  ✓ predicate-finder.png");
  await pfPage.close();

  // ── FDA Guidance Docs ──
  console.log("Capturing FDA Guidance Docs...");
  const gdPage = await browser.newPage();
  await gdPage.goto("https://ct.510kbridge.com/guidance-docs/", {
    waitUntil: "networkidle0",
    timeout: 30000,
  });
  await new Promise((r) => setTimeout(r, 2000));
  await gdPage.screenshot({
    path: join(OUT, "guidance-docs.png"),
    fullPage: false,
  });
  console.log("  ✓ guidance-docs.png");
  await gdPage.close();

  // ── Control Tower with Predicate Finder tab ──
  console.log("Capturing Control Tower tabs...");
  const ctPage = await browser.newPage();
  await ctPage.goto("https://ct.510kbridge.com/index.vite.html", {
    waitUntil: "networkidle0",
    timeout: 30000,
  });
  await new Promise((r) => setTimeout(r, 2000));

  // Try to load demo data
  try {
    await ctPage.waitForSelector("#wiz-demo", { timeout: 5000 });
    await ctPage.click("#wiz-demo");
    console.log("  → Clicked Load Demo Data");
    await new Promise((r) => setTimeout(r, 2500));
  } catch {
    console.log("  → No wizard detected, proceeding");
  }

  // Click predicate-finder tab
  const pfBtn = await ctPage.$(`.tab-btn[data-tab="predicate-finder"]`);
  if (pfBtn) {
    await ctPage.evaluate(
      (el) => el.scrollIntoView({ inline: "center" }),
      pfBtn,
    );
    await new Promise((r) => setTimeout(r, 300));
    await ctPage.evaluate((el) => el.click(), pfBtn);
    await new Promise((r) => setTimeout(r, 3000));
    await ctPage.screenshot({
      path: join(OUT, "predicate-finder-tab.png"),
      fullPage: false,
    });
    console.log("  ✓ predicate-finder-tab.png");
  }

  // Click guidance-docs tab
  const gdBtn = await ctPage.$(`.tab-btn[data-tab="guidance-docs"]`);
  if (gdBtn) {
    await ctPage.evaluate(
      (el) => el.scrollIntoView({ inline: "center" }),
      gdBtn,
    );
    await new Promise((r) => setTimeout(r, 300));
    await ctPage.evaluate((el) => el.click(), gdBtn);
    await new Promise((r) => setTimeout(r, 3000));
    await ctPage.screenshot({
      path: join(OUT, "guidance-docs-tab.png"),
      fullPage: false,
    });
    console.log("  ✓ guidance-docs-tab.png");
  }

  await ctPage.close();
  await browser.close();
  console.log("\nDone — product screenshots saved to " + OUT);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
