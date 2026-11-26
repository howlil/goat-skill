"""CI adapter for report.py.

The report command writes one JSON result to stdout when it succeeds.
For unreadable input, report.py should exit 2 and put the diagnostic on stderr.
"""

import json
import subprocess
import sys
from pathlib import Path


def main(source):
    report = Path(__file__).with_name("report.py")
    result = subprocess.run([sys.executable, str(report), source], capture_output=True, text=True)
    if result.returncode:
        sys.stderr.write(result.stderr)
        return result.returncode
    print(f"Report rows: {json.loads(result.stdout)['count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
