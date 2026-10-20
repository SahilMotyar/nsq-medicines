"""Copy the CDSCO alert data collected by grab (E:\\Projects\\grab) into this project.

- cache/pdfs/                  monthly alert PDFs from the `cdsco-drug-alerts` recipe (Feb 2013 - Jun 2025);
                               files already here are never overwritten
- data/raw/pdf_index.csv       one row per alert PDF: title, alert_month, source_type, is_revised, links,
                               local_path, sha256, bytes
- data/raw/portal_batches.csv  one row per batch from CDSCO's online NSQ portal (`cdsco-nsq-portal` recipe),
                               which replaced the PDFs from Jul 2025; nsq and spurious

Refresh:  grab run cdsco-drug-alerts  and  grab run cdsco-nsq-portal,  then  python scripts/sync_from_grab.py
Standard library only.
"""
import csv
import hashlib
import json
import shutil
from pathlib import Path

GRAB_DATA = Path(r"E:\Projects\grab\data")
ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "cache" / "pdfs"
RAW_DIR = ROOT / "data" / "raw"


def load_rows(recipe):
    path = GRAB_DATA / recipe / "latest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f"{recipe}: {len(data['rows'])} rows from grab run of {data['meta']['time']}")
    return data["rows"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  wrote {path.relative_to(ROOT)} ({len(rows)} rows)")


def sync_pdfs():
    rows = load_rows("cdsco-drug-alerts")
    files = GRAB_DATA / "cdsco-drug-alerts" / "files"
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    copied = missing = 0
    for row in rows:
        src, dst = files / row["file"], PDF_DIR / row["file"]
        if not row["file"] or not src.exists():
            missing += 1
            row.update(local_path="", sha256="", bytes="")
            continue
        if not dst.exists():
            shutil.copy2(src, dst)
            copied += 1
        elif sha256(dst) != sha256(src):
            print(f"  kept the different {dst.name} already in cache/pdfs (grab has another version)")
        row.update(local_path=dst.relative_to(ROOT).as_posix(), sha256=sha256(dst), bytes=dst.stat().st_size)
    print(f"  PDFs: {copied} copied, {len(rows) - copied - missing} already here, {missing} not downloaded in grab")
    write_csv(RAW_DIR / "pdf_index.csv", rows)


def sync_portal():
    write_csv(RAW_DIR / "portal_batches.csv", load_rows("cdsco-nsq-portal"))


if __name__ == "__main__":
    sync_pdfs()
    sync_portal()
