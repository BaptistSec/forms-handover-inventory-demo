# A volunteer's Google Form needs a handover, not just a new editor

Inventory the form, linked response sheet, uploaded files, notifications, automation and public entry points separately. Check which account owns each item before choosing a transfer or replacement route. Giving someone editor access to the form does not finish the handover.

The downloadable local checker below finds missing or unresolved items in that inventory. It does not connect to Google, transfer anything or verify account access. Its before/after CSVs contain invented records; the script outputs are real captured runs.

## First, check which ownership route is possible

If a volunteer created the form in a personal Google account, don't promise a direct transfer to the charity's Workspace account. Google's Drive guidance says you cannot transfer a file from a personal account to someone with a work or school account.[1]

For work/school accounts, direct ownership transfers are limited to the same organisation. Google's admin guidance lists alternatives for external files, including copies and certain shared-drive moves, depending on permissions and policies.[2] A copy has a different URL. Do not pick a route without checking the current instructions, file features and administrator approval.

If the form collects uploads, don't move it to a shared drive blindly: Google's shared-drive guidance says forms in shared drives cannot accept file uploads.[3] A form that still opens but no longer accepts a required upload is not a successful handover.

No step requires the volunteer to give you their password or personal account. Arrange the authorised transfer/copy process with the owner, preserve records under the charity's policy and avoid deleting the old workflow before checking the replacement.

## The six-part inventory

Use a restricted record with references, not beneficiary data or credentials:

- **Form:** owner, editors, responder access, questions and settings.
- **Response sheet:** separate file, owner, sharing and destination for new responses.
- **Uploads:** folders and individual files, where applicable, with their owners and access.
- **Notifications:** who needs new-response alerts and whether they receive them.
- **Automation:** scripts/add-ons and the identity under which they operate.
- **Entry points:** website links, QR codes, posters and emails sending people to the form.

Google explicitly says permission changes on a form do not automatically synchronise with its linked spreadsheet; change or remove access on each separately.[4] Changing a folder's owner also does not change the owners of its files.[1]

For Apps Script, installable triggers run under their creator's account, and an account cannot see another account's installed triggers.[5] A new form editor therefore isn't evidence that every automated action has a continuing authorised operator. Have the maintainer inspect and test any automation through its approved process.

## Run the local record check

From the extracted demonstration folder, run:

```sh
python3 check_inventory.py examples/before.csv
```

The input is an invented incomplete handover. It contains a pending form, blocked response sheet, a claimed notification check without its evidence reference, and no entry-points row.

Actual captured output:

```json
{
  "record_check": "open_items",
  "issues": [
    {"component": "entry_points", "issue": "missing component"},
    {"component": "form", "issue": "pending"},
    {"component": "notifications", "issue": "missing confirmed fields: evidence"},
    {"component": "response_sheet", "issue": "blocked"}
  ],
  "platform_verified": false
}
```

Exit status 1 means the record contains open items. It is not a failed Google operation: no Google operation occurred.

The checker requires one row for each of the six components. For a confirmed row it requires a reference, current owner, target owner and evidence reference. For an unused component it requires an explanation. A Forms workflow cannot mark its form unused.

These rules catch omissions, not lies. A made-up evidence reference still satisfies a nonblank field. The responsible owner must retrieve and assess the evidence independently.

## Compare a complete fictional record

Run:

```sh
python3 check_inventory.py examples/after.csv
```

Actual output:

```json
{
  "record_check": "complete_on_paper",
  "issues": [],
  "platform_verified": false
}
```

Exit status 0 means the CSV meets the checker rules, not that the handover worked. The after file's "confirmed" statuses and SYNTHETIC-CHECK references are invented fixture values. They are not platform evidence, approvals or tests of a real charity form.

For a real handover, replace them only with facts and evidence the authorised owner has checked. "Complete on paper" is intentionally weaker than "Google migration verified".

## What to verify in the real workflow

Using harmless test information and authorised accounts, the responsible team should check that the continuing person can administer the intended form, receive a test response in the correct sheet and obtain required notifications. If uploads or automation exist, check those paths too under the current provider instructions.

Preserve historic responses separately according to the charity's records rules. Do not assume a copied form carries its response history, links or automation. Agree a cutover time and update entry points if the URL changes. Check what the old link displays so responses are not silently split between two workflows.

Finally, remove the departing person's unneeded access on each affected file/system. Ownership transfer is not access removal: Google's admin guidance states that transferring files does not change who has access.[2]

## What was actually tested

On 7 October 2026, both fixture runs and 14 synthetic unit tests passed locally on Linux with Python 3.10.12. The test suite checks missing components, blocked/pending states, absent evidence/owners, unused reasons, duplicates, unknown components, invalid statuses, headers, exit codes and unchanged input bytes.

Before/after SHA256 lists match. The checker reads CSVs and prints JSON; it doesn't write back to inputs. If redirecting output, choose a new report filename: redirecting into the input path can destroy the file before Python reads it.

Windows, macOS and a real Google handover were not tested. The checker cannot discover missing apps, validate links, verify an owner's identity or authenticate evidence. Use it as a completeness prompt alongside live checks, not as a migration or compliance tool.

## Optional companion and sources

The free [Essential Security Kit](https://payhip.com/b/Jy4qE?utm_source=substack&utm_medium=article&utm_campaign=forms_handover_demo) from Tidy Desk Digital offers broader account/incident preparation. It doesn't automate a Forms transfer. Its listing says its workbook was checked in LibreOffice, not Excel itself. You can use this demonstration without the kit.

Demonstration download: pending public repository and QA link check. Do not publish until linked.

Google documentation checked 7 October 2026:

[1] Ownership limits and folder/file distinction:
https://support.google.com/drive/answer/2494892

[2] Admin transfers and external alternatives:
https://support.google.com/a/answer/1247799?hl=en

[3] Shared-drive limitations:
https://support.google.com/a/users/answer/12382709?hl=en

[4] Form and linked-sheet permissions:
https://support.google.com/docs/answer/2917111

[5] Installable trigger identity:
https://developers.google.com/apps-script/guides/triggers/installable
