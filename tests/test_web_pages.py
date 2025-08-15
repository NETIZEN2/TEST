from pathlib import Path

PAGES = [
    "web/app/pages/search.tsx",
    "web/app/pages/disambiguation.tsx",
    "web/app/pages/profile.tsx",
    "web/app/pages/evidence.tsx",
    "web/app/pages/compare.tsx",
    "web/app/pages/watchlists.tsx",
    "web/app/pages/settings.tsx",
]


def test_pages_exist_and_have_main():
    for page in PAGES:
        p = Path(page)
        assert p.is_file(), f"{page} missing"
        content = p.read_text()
        assert "<main" in content, f"{page} missing <main> landmark"
