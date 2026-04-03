/**
 * Scrape FDA CDRH guidance documents using Puppeteer (headless Chrome).
 * The FDA DataTables table is JS-rendered, so we need a real browser.
 * Output: public/guidance-docs/guidance-data.json
 */
import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const __dirname = path.dirname(fileURLToPath(import.meta.url));

const URL =
  "https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/guidance-documents-medical-devices-and-radiation-emitting-products";

(async () => {
  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();
  await page.setUserAgent(
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  );

  console.log("Loading page...");
  await page.goto(URL, { waitUntil: "networkidle2", timeout: 60000 });

  // Wait for DataTables to render
  console.log("Waiting for table to render...");
  await page.waitForSelector("table.lcds-datatable--cdrh tbody tr", {
    timeout: 30000,
  });

  // Change page length to show all entries
  console.log('Selecting "All" entries...');
  const hasAllOption = await page.evaluate(() => {
    const sel = document.querySelector('select[name*="length"]');
    if (!sel) return false;
    const opts = Array.from(sel.options);
    const allOpt = opts.find((o) => o.value === "-1" || o.text === "All");
    if (allOpt) {
      sel.value = allOpt.value;
      sel.dispatchEvent(new Event("change"));
      return true;
    }
    return false;
  });

  if (hasAllOption) {
    console.log("Waiting for all rows to load...");
    await page.waitForFunction(
      () => {
        const info = document.querySelector(".dataTables_info");
        if (!info) return false;
        const m = info.textContent.match(/of (\d+)/);
        const total = m ? parseInt(m[1]) : 0;
        const rows = document.querySelectorAll(
          "table.lcds-datatable--cdrh tbody tr",
        );
        return rows.length >= total;
      },
      { timeout: 120000 },
    );
  } else {
    console.log('No "All" option found, will paginate...');
  }

  // Extract data from the table
  console.log("Extracting data...");
  const docs = await page.evaluate(() => {
    const rows = document.querySelectorAll(
      "table.lcds-datatable--cdrh tbody tr",
    );
    const results = [];
    for (const row of rows) {
      const cells = row.querySelectorAll("td");
      if (cells.length < 5) continue;

      // Cell 0: Summary (contains title link + expand details)
      const summaryLink = cells[0].querySelector("a");
      const title = summaryLink
        ? summaryLink.textContent.trim()
        : cells[0].textContent.trim();
      const pageUrl = summaryLink ? summaryLink.href : "";

      // Cell 1: Document (PDF link)
      const pdfLink = cells[1].querySelector("a");
      const pdfUrl = pdfLink ? pdfLink.href : "";

      // Cell 2: Issue Date
      const issueDate = cells[2].textContent.trim();

      // Cell 3: Topic, Cell 4: Guidance Status, Cell 5: Open for Comment
      // Cell 6: Comment Closing Date (hidden), Cell 7: Docket Number (hidden)
      const topic = cells[3] ? cells[3].textContent.trim() : "";
      const status = cells[4] ? cells[4].textContent.trim() : "";
      const openForComment = cells[5] ? cells[5].textContent.trim() : "";
      const docketNumber = cells[7] ? cells[7].textContent.trim() : "";

      results.push({
        title,
        pageUrl,
        pdfUrl,
        issueDate,
        topic,
        status,
        openForComment,
        docketNumber,
      });
    }
    return results;
  });

  console.log(`Extracted ${docs.length} documents`);

  // Ensure output dir exists
  const outDir = path.join(__dirname, "public", "guidance-docs");
  fs.mkdirSync(outDir, { recursive: true });

  // Write JSON
  const outFile = path.join(outDir, "guidance-data.json");
  fs.writeFileSync(outFile, JSON.stringify(docs, null, 2));
  console.log(`Wrote ${outFile}`);

  // Print first 3 for verification
  console.log("\nSample entries:");
  for (const d of docs.slice(0, 3)) {
    console.log(`  ${d.title.substring(0, 80)}...`);
    console.log(
      `    Date: ${d.issueDate}, Status: ${d.status}, Topic: ${d.topic.substring(0, 60)}`,
    );
  }

  await browser.close();
})();
