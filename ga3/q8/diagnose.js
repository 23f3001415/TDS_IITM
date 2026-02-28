const { chromium } = require("playwright");

const START_URL =
  "https://sanand0.github.io/tdsdata/cdp_trap/index.html?student=23f3001415%2540ds.study.iitm.ac.in";
const TARGET_PAGE_COUNT = 15;
const ASYNC_WAIT_MS = 3500;

function pageNameFromUrl(urlString) {
  const u = new URL(urlString);
  const parts = u.pathname.split("/");
  return parts[parts.length - 1] || "index.html";
}

function normalizeUrl(href, studentValue) {
  try {
    const base = new URL(START_URL);
    const u = new URL(href, base);
    if (u.origin !== base.origin) return null;
    if (!u.pathname.includes("/tdsdata/cdp_trap/")) return null;
    if (!u.pathname.endsWith(".html")) return null;
    u.searchParams.set("student", studentValue);
    return u.toString();
  } catch {
    return null;
  }
}

async function collectLinks(page, studentValue) {
  const hrefs = await page.$$eval("a[href]", (anchors) =>
    anchors.map((a) => a.getAttribute("href")).filter(Boolean)
  );
  return hrefs
    .map((href) => normalizeUrl(href, studentValue))
    .filter((v) => v !== null);
}

async function visitAndRecord(page, url, state) {
  const name = pageNameFromUrl(url);
  state.currentPageName = name;
  await page.goto(url, { waitUntil: "load", timeout: 60000 });
  await page.waitForTimeout(ASYNC_WAIT_MS);
  if (!state.visitOrder.includes(name)) {
    state.visitOrder.push(name);
  }
}

async function runDiagnostics() {
  const studentValue = new URL(START_URL).searchParams.get("student") || "";
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  const state = {
    currentPageName: "index.html",
    visitOrder: [],
    uncaughtErrorPages: new Set(),
    consoleEvents: [],
  };

  page.on("console", (msg) => {
    state.consoleEvents.push({
      page: state.currentPageName,
      type: msg.type(),
      text: msg.text(),
    });
  });

  page.on("pageerror", (err) => {
    state.uncaughtErrorPages.add(state.currentPageName);
    state.consoleEvents.push({
      page: state.currentPageName,
      type: "pageerror",
      text: err.message || String(err),
    });
  });

  const queue = [START_URL];
  const visitedUrls = new Set();

  while (queue.length > 0 && visitedUrls.size < TARGET_PAGE_COUNT) {
    const nextUrl = queue.shift();
    if (!nextUrl || visitedUrls.has(nextUrl)) continue;

    await visitAndRecord(page, nextUrl, state);
    visitedUrls.add(nextUrl);

    const links = await collectLinks(page, studentValue);
    for (const link of links) {
      if (!visitedUrls.has(link) && !queue.includes(link)) {
        queue.push(link);
      }
    }
  }

  // Safety fallback in case traversal discovers fewer pages.
  if (visitedUrls.size < TARGET_PAGE_COUNT) {
    const base = new URL(START_URL);
    const candidates = [new URL("index.html", base)];
    for (let i = 1; i <= 14; i += 1) {
      candidates.push(new URL(`page_${i}.html`, base));
    }
    for (const u of candidates) {
      u.searchParams.set("student", studentValue);
      const s = u.toString();
      if (visitedUrls.has(s)) continue;
      if (visitedUrls.size >= TARGET_PAGE_COUNT) break;
      await visitAndRecord(page, s, state);
      visitedUrls.add(s);
    }
  }

  await context.close();
  await browser.close();

  const errorPagesInVisitOrder = state.visitOrder.filter((p) =>
    state.uncaughtErrorPages.has(p)
  );

  const report = {
    TOTAL_PAGES_VISITED: visitedUrls.size,
    TOTAL_ERRORS: state.uncaughtErrorPages.size,
    FIRST_ERROR_PAGE: errorPagesInVisitOrder[0] || "NONE",
  };

  console.log(`TOTAL_PAGES_VISITED=${report.TOTAL_PAGES_VISITED}`);
  console.log(`TOTAL_ERRORS=${report.TOTAL_ERRORS}`);
  console.log(`FIRST_ERROR_PAGE=${report.FIRST_ERROR_PAGE}`);
}

runDiagnostics().catch((err) => {
  console.error("Diagnostics failed:", err);
  process.exit(1);
});
