import re
from urllib.parse import urljoin, urlparse

import requests


START_URL = "https://sanand0.github.io/tdsdata/crawl_html/"
ALLOWED_PREFIX = "https://sanand0.github.io/tdsdata/crawl_html/"
HREF_RE = re.compile(r'href=["\\\']([^"\\\']+)["\\\']', re.IGNORECASE)


def crawl_html_files(start_url: str) -> set[str]:
    session = requests.Session()
    seen_pages = set()
    queue = [start_url]
    html_files = set()

    while queue:
        url = queue.pop(0)
        if url in seen_pages:
            continue
        seen_pages.add(url)

        try:
            resp = session.get(url, timeout=20)
        except requests.RequestException:
            continue

        if resp.status_code != 200:
            continue

        for href in HREF_RE.findall(resp.text):
            nxt = urljoin(url, href).split("#")[0]
            if not nxt.startswith(ALLOWED_PREFIX):
                continue
            parsed = urlparse(nxt)
            normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

            if parsed.path.lower().endswith(".html"):
                html_files.add(normalized)

            if (
                normalized.endswith("/") or normalized.lower().endswith(".html")
            ) and normalized not in seen_pages and normalized not in queue:
                queue.append(normalized)

    return html_files


def count_m_to_z(html_files: set[str]) -> int:
    count = 0
    for url in html_files:
        name = url.rsplit("/", 1)[-1]
        if name and "M" <= name[0].upper() <= "Z":
            count += 1
    return count


if __name__ == "__main__":
    files = crawl_html_files(START_URL)
    print(count_m_to_z(files))
