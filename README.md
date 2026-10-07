# Check a Google Forms handover record

This free program checks whether a written handover record has missing or unresolved items. It runs on your computer. It does not connect to Google, change anything or prove that a real handover worked.

The two supplied examples are made up. Their owners, status labels and evidence references are not real approvals or checked Google account facts.

## Try the examples

You need Python installed. Open a command window in the folder containing `check_inventory.py`, then run:

```sh
python3 check_inventory.py examples/before.csv
python3 check_inventory.py examples/after.csv
python3 -m unittest -v
```

The first command finds gaps in a made-up record. The second finds a record that meets the program's rules. Both reports say that Google account facts have not been checked. The third command runs the 14 supplied automated checks.

A complete record is not proof of a successful handover. The responsible person must check the form, response spreadsheet, uploaded files, alerts, automatic tasks and links in the real accounts.

Read `WALKTHROUGH.md` for the full procedure and limits. The example files use CSV, a text format that stores a table with commas between its columns. Saved report files show the actual program output and whether each run reported open items or a complete written record.

The 14 automated checks passed on Linux with Python 3.10.12 on 7 October 2026. Windows, macOS and a real Google handover have not been tested. If you save a report to a file, choose a new filename. Never save it over an input file.

Published by William Baptist | Tidy Desk Digital
