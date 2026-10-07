# Forms handover inventory checker
Local synthetic record checker. Does not connect to Google, make changes, or verify platform facts.
Run from extracted root:
python3 check_inventory.py examples/before.csv
python3 check_inventory.py examples/after.csv
python3 -m unittest -v
Read WALKTHROUGH.md for the complete procedure and limitations. All CSV ownership/status/evidence values are fictional fixtures, never real approvals or verified platform facts. Actual outputs and exit statuses are captured. 14 tests passed Linux Python 3.10.12, 7 Oct 2026; Windows/macOS and real Google handover not tested. Record completeness is not platform verification. Never redirect output into an input file.

Published by William Baptist | Tidy Desk Digital
