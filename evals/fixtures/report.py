import json
import sys
from pathlib import Path


def main():
    try:
        rows = json.loads(Path(sys.argv[1]).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read report: {exc}")
        return 0
    print(json.dumps({"count": len(rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
