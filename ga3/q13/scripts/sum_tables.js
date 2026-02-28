const { chromium } = require("playwright");

const SEEDS = Array.from({ length: 10 }, (_, i) => 70 + i);

function extractNumbers(text) {
  const matches = String(text).match(/-?\d+(?:\.\d+)?/g);
  if (!matches) return [];
  return matches.map(Number).filter((n) => Number.isFinite(n));
}

async function sumPage(page, seed) {
  const url = `https://sanand0.github.io/tdsdata/js_table/?seed=${seed}`;
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForSelector("table", { timeout: 60000 });
  await page.waitForTimeout(1500);

  const sum = await page.evaluate(() => {
    const cells = Array.from(document.querySelectorAll("table td, table th"));
    let total = 0;
    for (const cell of cells) {
      const text = cell.textContent || "";
      const matches = text.match(/-?\d+(?:\.\d+)?/g);
      if (!matches) continue;
      for (const m of matches) {
        const n = Number(m);
        if (Number.isFinite(n)) total += n;
      }
    }
    return total;
  });

  return sum;
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  let total = 0;
  for (const seed of SEEDS) {
    const pageSum = await sumPage(page, seed);
    console.log(`SEED_${seed}_SUM=${pageSum}`);
    total += pageSum;
  }

  const rounded = Math.round((total + Number.EPSILON) * 100) / 100;
  console.log(`FINAL_TOTAL_SUM=${rounded}`);
  await browser.close();
}

main().catch((err) => {
  console.error("Scrape failed:", err);
  process.exit(1);
});
