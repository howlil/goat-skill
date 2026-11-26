"""Exercise search requests and results in a headless browser with controlled responses."""

import os
import re

from playwright.sync_api import Error, expect, sync_playwright


# Hold fetch responses until the test releases them, honoring normal cancellation.
SEARCH_TRANSPORT = """
window.searchRequests = [];
window.fetch = (input, options = {}) => new Promise((resolve, reject) => {
    const request = new Request(input instanceof Request ? input : new URL(input, location.href), options);
    const url = new URL(request.url);
    if (url.pathname !== "/api/reports" || request.method !== "GET") throw new Error("Unexpected request");
    if (request.signal.aborted) {
        reject(request.signal.reason);
        return;
    }
    request.signal.addEventListener("abort", () => reject(request.signal.reason), {once: true});
    window.searchRequests.push({query: url.searchParams.get("q"), resolve});
});
"""


def type_query(page, query):
    page.get_by_role("searchbox").fill(query)
    page.wait_for_function("query => searchRequests.some(r => r.query === query)", arg=query)


def respond(page, query, names, status=200):
    page.evaluate(
        """async ([query, reports, status]) => {
            const request = searchRequests.find(r => r.query === query);
            request.resolve(new Response(JSON.stringify({reports}), {
                status, headers: {"Content-Type": "application/json"}
            }));
            await new Promise(requestAnimationFrame);
            await new Promise(requestAnimationFrame);
        }""",
        [query, names, status],
    )


def latest_query(page):
    type_query(page, "quarter")
    type_query(page, "quarter & year")
    respond(page, "quarter & year", ["Latest quarterly summary"])
    row = page.get_by_role("listitem")
    expect(row).to_have_text("Latest quarterly summary")
    respond(page, "quarter", ["Older quarterly report"])
    expect(row).to_have_text("Latest quarterly summary")


def recover_after_failure(page):
    type_query(page, "accounts")
    respond(page, "accounts", [], status=503)
    status = page.get_by_role("status")
    diagnostic = re.compile(r"error|unavailable|fail|could not|couldn.t|unable|try again", re.I)
    expect(status).to_contain_text(diagnostic)
    expect(page.get_by_role("searchbox")).to_have_value("accounts")
    type_query(page, "receipts")
    respond(page, "receipts", ["Receipt reconciliation"])
    expect(page.get_by_role("listitem")).to_have_text("Receipt reconciliation")
    expect(status).not_to_contain_text(diagnostic)


def check_async_search(workspace):
    source = (workspace / "report-search.html").read_text(encoding="utf-8")
    checks = {"latest_query_wins": latest_query, "http_error_and_recovery": recover_after_failure}
    expect.set_options(timeout=2000)
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(
                executable_path=os.environ.get("GOAT_POPUP_CHROMIUM"), timeout=12000,
            )
        except Error as exc:
            raise RuntimeError("Could not start Chromium for search eval. Install it with python3 -m playwright install chromium.") from exc
        with browser:
            results = {}
            for name, check in checks.items():
                page = browser.new_page(service_workers="block")
                page.set_default_timeout(2500)
                page.add_init_script(SEARCH_TRANSPORT)
                page.route("**/*", lambda route: route.abort())
                page.route("https://reports.test/", lambda route: route.fulfill(content_type="text/html", body=source))
                try:
                    page.goto("https://reports.test/")
                    check(page)
                except (AssertionError, Error):
                    results[name] = False
                else:
                    results[name] = True
                finally:
                    page.close()
            return results
