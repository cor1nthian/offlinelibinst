# Python Offline Library Installer
Script to install Python (.whl libraries) offline. Usage:

`libinst.py <path to pip> <path to library folder>`

Or, instead of using script argements, specify paths in the script (pipPath and targetFolder variables respectively)

Can be called with arguments:
| Position | Suggested type | Description |
| --- | --- | --- |
| 1 | String | Path to pip tool
| 2 | String | Path to the folder comtaining .whl libraries
| 3 | Boolean | If true, script creates library install report. True by default.
| 4 | Int | Maximum libraries to install. 256 by default.

:exclamation: Variables set in the script have priority over script arguments

Script return codes:
| Code | Description |
| --- | --- |
| 0 | Successful execution
| 1 | Path to pip does not exist
| 2 | Path to pip not set
| 3 | Path to target folder does not exist
| 4 | Path to target folder not set
| 5 | Install report generation flag not set
| 6 | Incorrect max lib quantity set
| 7 | Max lib quantity not set
| 8 | Could not find any lib
| 9 | Max lib quamtity exceeded
