# A volunteer who made your charity's sign-up form is leaving. What do you need to check?

If a volunteer built your charity's sign-up form using their own Google account, giving another person permission to edit it may not be enough. Responses might still go to a spreadsheet the charity cannot control. Email alerts might still reach the departing volunteer. If you replace the form, links on your website may still point to the old one.

Start by listing the form and everything it uses. Check who owns the response spreadsheet, where uploaded files go, who receives alerts and whether anything automatically sends emails or updates records. Then agree what must be transferred or replaced, test that the next person can run it, and remove access that is no longer needed.

This guide explains those checks. It also includes a small tool that spots missing items in your written list. It is written in Python, programming software you must install before running the commands below. The tool was tested locally with fictional records; it does not connect to Google or prove that a real form works. You can follow the checks without using Python.

## First, check how the charity can take control of the files

If a volunteer created the form in a personal Google account, don't promise a direct transfer to the charity's Google Workspace work account. Google's Drive guidance says you cannot transfer a file from a personal account to someone with a work or school account.[1]

For work/school accounts, giving a file to a new owner is limited to accounts in the same organisation. Google's instructions for account managers list other ways to bring in files owned outside the charity. These include copies and, where allowed, moving files into a shared drive, a team-owned storage area. The available choices depend on the account's sharing rules.[2] A copy has a different web address. Do not pick a route without checking the current instructions, what the form does and approval from the person allowed to manage the accounts.

If the form collects uploads, don't move it to a shared drive blindly: Google's shared-drive guidance says forms in shared drives cannot accept file uploads.[3] A form that still opens but no longer accepts a required upload is not a successful handover.

No step requires the volunteer to give you their password or personal account. Agree the permitted transfer or copying steps with the owner. Keep records under the charity's rules and keep the old form and its supporting files until the replacement has been checked.

## List these six parts separately

Keep this list available only to people who need it. Use labels for the files, not information about people the charity helps, passwords or other sign-in secrets:

- **Form:** who owns it, who can edit it, who can fill it in, and its questions and settings.
- **Response spreadsheet:** who owns this separate file, who can open it, and where new answers are recorded.
- **Uploaded files:** who owns and can open the folders and files people submit, if the form allows this.
- **Email alerts:** who needs to hear about new answers and whether those alerts reach them.
- **Automatic actions:** any code or extra app that sends emails or updates records, and whose account it uses.
- **Ways to reach the form:** website links, QR codes (square patterns people scan with a phone to open a web address), posters and emails that people use to open it.

Google explicitly says changing who can open or edit the form does not automatically make the same change on the spreadsheet holding its answers; change or remove access on each separately.[4] Changing a folder's owner also does not change the owners of its files.[1]

If the form uses Apps Script, Google's tool for running code, check who set up its automatic actions. An installable trigger is a saved instruction to run code when something happens, such as a new answer arriving. Google says it runs using the account that created it; another account cannot see that person's installed triggers.[5] Letting someone edit the form does not prove those actions will keep working. Have the person responsible for the code check and test them through the agreed process.

## Run the optional check on your written list

The Python tool reads a CSV file, a text file with rows and columns separated by commas. After downloading and unpacking the demonstration, open a terminal, the window where you type commands, in its main folder. Run:

```sh
python3 check_inventory.py examples/before.csv
```

The first file contains a made-up, incomplete list. It contains a form change still waiting to finish and a response spreadsheet whose change cannot proceed, an email-alert check marked complete but without a record of what was checked, and no row listing the ways people reach the form.

This is what the actual run printed. The labels in the result are the code's field names: open_items means something remains unfinished; platform_verified:false means Google was not checked. component names the part of the change; entry_points means ways people reach the form; notifications means email alerts; evidence means a record of a real check.

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

The command finishes with a number, called an exit status. Here, 1 means the list contains unfinished items. It is not a failed Google operation: no Google operation occurred.

The checker requires one row for each of the six parts. A row marked confirmed must name the item, its current owner, its intended owner and a record of the check. A part marked not_used must explain why it is not needed. The form itself cannot be marked unused.

These rules find missing entries, not false statements. A made-up check label still fills a cell. The responsible person must find the real records and check them.

## Compare a complete made-up list

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

The finishing number 0 means the list meets the checker rules, not that a form was successfully passed to someone else. The after file's confirmed labels and SYNTHETIC-CHECK names are made-up test values. They are not real checks, approvals or tests of a charity form.

For real work, use only facts and records checked by the person allowed to approve the change. complete_on_paper means the list is filled in; it does not mean the changes in Google worked.

## What to check on the real form

Using harmless test information and accounts you are allowed to use, the responsible team should check that the next person can manage the form, see a test answer in the right spreadsheet and receive the required email alerts. If people submit files or the form starts automatic actions, test those too using the current Google instructions.

Keep old answers separately under the charity's rules for keeping records. Do not assume a copied form includes old answers or keeps its links and automatic actions working. Agree when to switch to the new form and update website links, posters and other ways to reach it if its web address changes. Check what the old link displays so responses are not silently split between the old and new forms.

Finally, remove the departing person's unneeded access on each affected file/system. Giving a file to a new owner does not remove the old person's access: Google's instructions for account managers state that transferring files does not change who has access.[2]

## What was actually tested

On 7 October 2026, both runs on made-up files and 14 automated checks passed on the demonstration computer on Linux with Python 3.10.12. Those checks cover missing parts, unfinished changes, absent owners or check records, reasons for unused parts, repeated or unknown parts, invalid labels, column names, finishing numbers and unchanged input files.

The before/after SHA256 lists match. SHA256 makes a file fingerprint: matching fingerprints show that these input files stayed unchanged. The checker reads the text table and prints JSON, the labelled text result shown above. It does not change the input files. If saving the result with a command, use a new report filename. Saving it over the input file can destroy that file before Python reads it.

Windows, macOS and a real Google handover were not tested. The checker cannot find missing apps, check links, establish who owns an account or prove a check record is genuine. Use it to notice gaps in your list alongside real checks, not to approve a file transfer or claim legal compliance.

## Optional companion and sources

The free [Essential Security Kit](https://payhip.com/b/Jy4qE?utm_source=substack&utm_medium=article&utm_campaign=forms_handover_demo) from Tidy Desk Digital offers help preparing for account problems and other security problems. It doesn't automate a Forms transfer. Its listing says its workbook was checked in LibreOffice, not Excel itself. You can use this demonstration without the kit.

Download the code, made-up example files and the results printed by the program from the public [handover-list checker](https://github.com/BaptistSec/forms-handover-inventory-demo). Use Code → Download ZIP, extract it, and run the commands from the main folder you unpacked.

Google documentation checked 7 October 2026:

[1] Who can own the files and why a folder and its files need separate checks:
https://support.google.com/drive/answer/2494892

[2] Moving ownership and handling files owned outside the charity:
https://support.google.com/a/answer/1247799?hl=en

[3] Shared-drive limitations:
https://support.google.com/a/users/answer/12382709?hl=en

[4] Who can open or edit the form and its response spreadsheet:
https://support.google.com/docs/answer/2917111

[5] Whose account runs automatic actions:
https://developers.google.com/apps-script/guides/triggers/installable
