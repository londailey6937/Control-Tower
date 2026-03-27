#!/usr/bin/env node
/**
 * Capture Chinese-language screenshots of every Control Tower tab for the
 * marketing website CN page.
 * Outputs to arch-medical/public/screenshots/ with -cn suffix.
 */
import puppeteer from "puppeteer";
import { mkdirSync } from "fs";
import { join } from "path";

const OUT = "/Users/londailey/arch-medical/public/screenshots";
mkdirSync(OUT, { recursive: true });

const TABS = [
  { id: "dual-track", name: "dual-track" },
  { id: "gates", name: "gate-system" },
  { id: "regulatory", name: "regulatory-tracker" },
  { id: "risks", name: "risk-dashboard" },
  { id: "audit", name: "audit-trail" },
  { id: "doc-library", name: "document-control" },
  { id: "actions", name: "actions" },
  { id: "timeline", name: "timeline" },
  { id: "budget", name: "budget" },
  { id: "cash-runway", name: "cash-runway" },
  { id: "us-investment", name: "us-investment" },
  { id: "resources", name: "resources" },
  { id: "suppliers", name: "suppliers" },
  { id: "qa-sheet", name: "message-board" },
  { id: "fda-comms", name: "fda-comms" },
];

async function main() {
  const browser = await puppeteer.launch({
    headless: true,
    defaultViewport: { width: 1440, height: 900 },
  });
  const page = await browser.newPage();

  // Load app — uses index.vite.html via Vite
  await page.goto("http://localhost:5199/index.vite.html", {
    waitUntil: "networkidle0",
    timeout: 30000,
  });

  // Authenticate through login gate
  try {
    await page.waitForSelector("#loginPassword", { timeout: 5000 });
    await page.type("#loginPassword", "arch2026");
    await page.click('#loginForm button[type="submit"]');
    console.log("  → Logged in");
    await new Promise((r) => setTimeout(r, 2000));
  } catch {
    console.log("  → No login gate detected, proceeding");
  }

  // Wait for the wizard to appear and click "Load Demo Data"
  await page.waitForSelector(".tab-btn", { timeout: 10000 });
  await new Promise((r) => setTimeout(r, 1000));

  // Click "Load Demo Data" button to bypass wizard and populate dashboard
  try {
    await page.waitForSelector("#wiz-demo", { timeout: 5000 });
    await page.click("#wiz-demo");
    console.log("  → Clicked Load Demo Data");
    await new Promise((r) => setTimeout(r, 2500));
  } catch {
    console.log("  → No wizard detected, proceeding");
  }

  // Switch to Chinese language
  const langBtn = await page.$("#langToggle");
  if (langBtn) {
    await langBtn.click();
    console.log("  → Switched to Chinese (中文)");
    await new Promise((r) => setTimeout(r, 1500));
  } else {
    console.error("  ✕ Could not find language toggle button!");
    await browser.close();
    process.exit(1);
  }

  for (const tab of TABS) {
    // Scroll tab button into view and click it
    const btn = await page.$(`.tab-btn[data-tab="${tab.id}"]`);
    if (btn) {
      await page.evaluate((el) => el.scrollIntoView({ inline: "center" }), btn);
      await new Promise((r) => setTimeout(r, 300));
      await page.evaluate((el) => el.click(), btn);
    }
    await new Promise((r) => setTimeout(r, 800));

    const outPath = join(OUT, `${tab.name}-cn.png`);
    await page.screenshot({ path: outPath, fullPage: false });
    console.log(`  ✓ ${tab.name}-cn.png`);
  }

  await browser.close();
  console.log(`\nDone — ${TABS.length} CN screenshots saved to ${OUT}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
