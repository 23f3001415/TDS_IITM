const { chromium } = require("playwright");

const SEEDS = Array.from({ length: 10 }, (_, i) => i);

async function sumSeed(page, seed) {
  const url = `https://sanand0.github.io/tdsdata/js_table/?seed=${seed}`;
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForSelector("table", { timeout: 60000 });
  await page.waitForTimeout(1500);
  return page.evaluate(() => {
    let total = 0;
    const cells = Array.from(document.querySelectorAll("table td, table th"));
    for (const cell of cells) {
      const text = cell.textContent || "";
      const nums = text.match(/-?\d+(?:\.\d+)?/g);
      if (!nums) continue;
      for (const n of nums) {
        const v = Number(n);
        if (Number.isFinite(v)) total += v;
      }
    }
    return total;
  });
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  let grandTotal = 0;
  for (const seed of SEEDS) {
    const s = await sumSeed(page, seed);
    console.log(`SEED_${seed}_SUM=${s}`);
    grandTotal += s;
  }
  console.log(`TOTAL_SUM=${grandTotal}`);
  await browser.close();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
