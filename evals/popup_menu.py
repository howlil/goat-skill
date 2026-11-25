"""Score the popup menu through a real browser and its accessible controls."""

import os

from playwright.sync_api import Error, expect, sync_playwright


def trigger(page):
    return page.get_by_role("button", name="Report actions", exact=True)


def menu(page, name="Report actions"):
    return page.get_by_role("menu", name=name, exact=True)


def item(page, name):
    return page.get_by_role("menuitem", name=name, exact=True)


def open_with_keyboard(page):
    trigger(page).focus()
    page.keyboard.press("Enter")
    expect(item(page, "Rename")).to_be_focused()


def open_export_with_keyboard(page):
    open_with_keyboard(page)
    page.keyboard.press("ArrowDown")
    expect(item(page, "Export")).to_be_focused()
    page.keyboard.press("ArrowRight")
    expect(item(page, "CSV")).to_be_focused()


def check_keyboard(page):
    expect(menu(page)).to_be_hidden()
    expect(trigger(page)).to_have_attribute("aria-expanded", "false")
    open_with_keyboard(page)
    expect(menu(page)).to_be_visible()
    expect(trigger(page)).to_have_attribute("aria-expanded", "true")
    page.keyboard.press("ArrowUp")
    expect(item(page, "Archive")).to_be_focused()
    page.keyboard.press("ArrowDown")
    expect(item(page, "Rename")).to_be_focused()
    page.keyboard.press("Enter")
    expect(page.get_by_role("status")).to_have_text("Rename selected.")
    expect(menu(page)).to_be_hidden()
    expect(trigger(page)).to_be_focused()


def check_submenu(page):
    open_with_keyboard(page)
    expect(menu(page, "Export")).to_be_hidden()
    page.keyboard.press("ArrowDown")
    expect(item(page, "Export")).to_be_focused()
    expect(item(page, "Export")).to_have_attribute("aria-expanded", "false")
    page.keyboard.press("ArrowRight")
    expect(item(page, "CSV")).to_be_focused()
    expect(menu(page, "Export")).to_be_visible()
    expect(item(page, "Export")).to_have_attribute("aria-expanded", "true")
    page.keyboard.press("ArrowUp")
    expect(item(page, "JSON")).to_be_focused()
    page.keyboard.press("ArrowDown")
    expect(item(page, "CSV")).to_be_focused()
    page.keyboard.press("ArrowLeft")
    expect(menu(page, "Export")).to_be_hidden()
    expect(item(page, "Export")).to_have_attribute("aria-expanded", "false")
    expect(item(page, "Export")).to_be_focused()
    page.keyboard.press("ArrowRight")
    expect(item(page, "CSV")).to_be_focused()
    page.keyboard.press("Escape")
    expect(menu(page, "Export")).to_be_hidden()
    expect(item(page, "Export")).to_have_attribute("aria-expanded", "false")
    expect(item(page, "Export")).to_be_focused()
    page.keyboard.press("Escape")
    expect(menu(page)).to_be_hidden()
    expect(trigger(page)).to_have_attribute("aria-expanded", "false")
    expect(trigger(page)).to_be_focused()


def check_export(page):
    open_export_with_keyboard(page)
    page.keyboard.press("ArrowDown")
    expect(item(page, "JSON")).to_be_focused()
    page.keyboard.press("Enter")
    expect(page.get_by_role("status")).to_have_text("Exported JSON.")
    expect(menu(page, "Export")).to_be_hidden()
    expect(menu(page)).to_be_hidden()
    expect(trigger(page)).to_be_focused()


def check_unavailable(page):
    open_with_keyboard(page)
    page.keyboard.press("ArrowUp")
    archive = item(page, "Archive")
    expect(archive).to_have_attribute("aria-disabled", "true")
    expect(archive).to_be_focused()
    expect(page.get_by_text("Archiving is unavailable for this report.", exact=True)).to_be_visible()
    for key in ("Enter", "Space"):
        page.keyboard.press(key)
        expect(menu(page)).to_be_visible()
        expect(page.get_by_role("status")).to_have_text("No action selected.")
        expect(archive).to_be_focused()


def check_pointer(page):
    trigger(page).click()
    expect(item(page, "Rename")).to_be_focused()
    item(page, "Export").click()
    expect(menu(page, "Export")).to_be_visible()
    expect(item(page, "CSV")).to_be_focused()
    details = page.get_by_role("button", name="Details", exact=True)
    details.click()
    expect(menu(page, "Export")).to_be_hidden()
    expect(menu(page)).to_be_hidden()
    expect(details).to_be_focused()
    trigger(page).click()
    item(page, "Export").click()
    item(page, "CSV").click()
    expect(page.get_by_role("status")).to_have_text("Exported CSV.")
    expect(menu(page, "Export")).to_be_hidden()
    expect(menu(page)).to_be_hidden()
    expect(trigger(page)).to_be_focused()


def check_narrow_viewport(page):
    open_export_with_keyboard(page)
    for popup in (menu(page), menu(page, "Export")):
        box = popup.bounding_box()
        assert box is not None
        assert box["x"] >= -0.5 and box["x"] + box["width"] <= page.viewport_size["width"] + 0.5
        assert box["y"] >= -0.5 and box["y"] + box["height"] <= page.viewport_size["height"] + 0.5


def check_popup_menu(workspace):
    source = (workspace / "action-menu.html").read_text(encoding="utf-8")
    checks = {
        "keyboard_navigation": check_keyboard,
        "submenu_focus_and_escape": check_submenu,
        "selection_feedback": check_export,
        "unavailable_action": check_unavailable,
        "pointer_selection_and_dismissal": check_pointer,
        "narrow_viewport": check_narrow_viewport,
    }
    expect.set_options(timeout=1500)
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(
                executable_path=os.environ.get("GOAT_POPUP_CHROMIUM"), timeout=12000,
            )
        except Error as exc:
            raise RuntimeError("Could not start Chromium for popup eval. Install it with python3 -m playwright install chromium.") from exc
        with browser:
            results = {}
            for name, check in checks.items():
                width = 320 if name == "narrow_viewport" else 960
                page = browser.new_page(viewport={"width": width, "height": 640}, service_workers="block")
                page.set_default_timeout(1500)
                page.route("**/*", lambda route: route.abort())
                try:
                    page.set_content(source)
                    check(page)
                except (AssertionError, Error):
                    results[name] = False
                else:
                    results[name] = True
                finally:
                    page.close()
            return results
