from __future__ import annotations

from pathlib import Path
import hashlib
import pandas as pd


ROOT = Path(".")
ARCHIVE = ROOT / "archive"
OUTPUT = ROOT / "replication_dataset_manifest.csv"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_csv(path: Path) -> dict[str, object]:
    info: dict[str, object] = {
        "file": str(path.relative_to(ROOT)),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "rows": None,
        "columns": None,
        "column_names": None,
        "first_date_like_value": None,
        "last_date_like_value": None,
        "read_error": None,
    }

    try:
        df = pd.read_csv(path)
        info["rows"] = len(df)
        info["columns"] = len(df.columns)
        info["column_names"] = " | ".join(map(str, df.columns.tolist()))

        # Try to find a date-like first column without modifying anything
        first_col = df.columns[0]
        parsed = pd.to_datetime(df[first_col], errors="coerce")

        if parsed.notna().sum() > 0:
            info["first_date_like_value"] = str(parsed.dropna().iloc[0].date())
            info["last_date_like_value"] = str(parsed.dropna().iloc[-1].date())

    except Exception as exc:
        info["read_error"] = repr(exc)

    return info


def main() -> None:
    rows: list[dict[str, object]] = []

    # Root-level CSV files
    for path in sorted(ROOT.glob("*.csv")):
        rows.append(inspect_csv(path))

    # Archived exact dataset CSV files
    for path in sorted(ARCHIVE.glob("*.csv")):
        rows.append(inspect_csv(path))

    manifest = pd.DataFrame(rows)
    manifest.to_csv(OUTPUT, index=False)

    print(f"Manifest written to: {OUTPUT.resolve()}")
    print()
    print("Summary:")
    print(f"Root CSV files       : {len(list(ROOT.glob('*.csv')))}")
    print(f"Archive CSV files    : {len(list(ARCHIVE.glob('*.csv')))}")
    print(f"Total CSV files      : {len(rows)}")
    print()
    print("Potentially empty CSV files:")
    empty = manifest[manifest["size_bytes"] == 0]
    if empty.empty:
        print("None")
    else:
        print(empty[["file", "size_bytes"]].to_string(index=False))


if __name__ == "__main__":
    main()