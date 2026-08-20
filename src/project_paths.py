from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_project_path(*parts):
    """Build an absolute path from the project root."""
    return (PROJECT_ROOT.joinpath(*parts)).resolve()


def resolve_user_path(value):
    """Convert a relative path from the project root or keep absolute paths as-is."""
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return resolve_project_path(path).resolve()


def find_csv_file():
    """Return the first existing CSV file from the standard project locations."""
    candidates = [
        resolve_project_path("data", "transactions.csv"),
        resolve_project_path("data", "raw", "transactions.csv"),
        resolve_project_path("raw", "transactions.csv"),
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]
