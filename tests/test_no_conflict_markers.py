from pathlib import Path


def test_no_conflict_markers():
    repo_root = Path(__file__).resolve().parent.parent
    markers = ("<<<<<<<", "=======", ">>>>>>>")
    offenders = []
    for path in repo_root.rglob("*"):
        if (
            path.is_file()
            and ".git" not in path.parts
            and "node_modules" not in path.parts
            and "__pycache__" not in path.parts
        ):
            try:
                for line in path.read_text(errors="ignore").splitlines():
                    if any(line.startswith(marker) for marker in markers):
                        offenders.append(str(path))
                        break
            except Exception:
                continue
    assert not offenders, f"Conflict markers found in: {offenders}"
