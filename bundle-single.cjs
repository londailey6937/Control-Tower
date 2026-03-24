#!/usr/bin/env node
// bundle-single.cjs — Inlines CSS + JS into a single self-contained HTML file
const fs = require("fs");
const path = require("path");

const dist = path.join(__dirname, "dist");
const htmlPath = path.join(dist, "index.html");
let html = fs.readFileSync(htmlPath, "utf8");

// Inline CSS: <link rel="stylesheet" ... href="/assets/xxx.css">
html = html.replace(
  /<link\s+rel="stylesheet"[^>]*href="\/assets\/([^"]+)"[^>]*>/g,
  (_, file) => {
    const css = fs.readFileSync(path.join(dist, "assets", file), "utf8");
    return `<style>${css}</style>`;
  },
);

// Inline JS: <script type="module" ... src="/assets/xxx.js"></script>
html = html.replace(
  /<script\s+type="module"[^>]*src="\/assets\/([^"]+)"[^>]*><\/script>/g,
  (_, file) => {
    const js = fs.readFileSync(path.join(dist, "assets", file), "utf8");
    return `<script type="module">${js}<\/script>`;
  },
);

const outPath = path.join(__dirname, "PM-Dashboard.html");
fs.writeFileSync(outPath, html, "utf8");
const kb = (fs.statSync(outPath).size / 1024).toFixed(1);
console.log(`✓ ${outPath}  (${kb} KB)`);
