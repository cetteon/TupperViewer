# Tupper Viewer [![License](https://img.shields.io/github/license/cetteon/TupperViewer?style=flat-square)](https://github.com/cetteon/TupperViewer/blob/main/LICENSE)

A simple command-line Python program for viewing, searching, and sorting Tupperbox JSON exports.

Tupper Viewer lets you browse your exported Tupperbox data, search for Tuppers by name or brackets, sort Tuppers by various properties, view detailed information, and randomly select a Tupper.

## Features

- View all Tuppers from an export
- Search Tuppers by name
- Search Tuppers by brackets
- Sort Tuppers by last used date
- Sort Tuppers by creation date
- Sort Tuppers by total messages
- Sort Tuppers alphabetically by name
- Ascending and descending sorting options
- Select a random Tupper
- Built-in help command
- Display detailed Tupper information
- Handle missing or `null` fields gracefully
- Case-insensitive searching and name sorting
- Windows drag-and-drop launcher

## Requirements

- Python 3.8 or newer
- A Tupperbox JSON export

The program only uses Python's standard library, so no additional packages are required.

## Installation

Clone or download the project:

```
git clone https://github.com/cetteon/TupperViewer.git
cd TupperViewer
```

 No dependencies need to be installed.

 ## Usage

 ### Command Line

 Run the program with your Tupperbox JSON export:

```
python tupper_viewer.py tuppers.json
```

 On some systems, you may need to use:

```
python3 tupper_viewer.py tuppers.json
```

 ### Windows Drag and Drop

 Windows users can use the included `run_tupper_viewer.bat` file to launch the program by dragging a Tupperbox JSON export onto it.

 The project should contain:

```
TupperViewer/
├── tupper_viewer.py
├── run_tupper_viewer.bat
└── README.md
```

 To use it:

 1. Locate your Tupperbox JSON export.
2. Drag the JSON file onto `run_tupper_viewer.bat`.
3. The batch file will automatically launch `tupper_viewer.py` with the JSON file.
4. The Tupper Viewer menu will open in a command prompt window.

 The batch file automatically locates `tupper_viewer.py` relative to itself, so the project can be moved to another folder without modifying the batch file.

 ## Main Menu

 After starting the program, you'll see:

```
==================================================
Tupper Viewer
==================================================
Total tuppers: 127

1. View all tuppers
2. Search by name
3. Search by brackets
4. Search by last used
5. Search by date created
6. Search by total messages
7. Search by name
8. Random Tupper
h. Help
q. Quit

Choose an option:
```

 ## View All Tuppers

 Select `1` to display every Tupper in the export.

 Each Tupper is assigned a number:

```
1. mist
   User ID: 1493163396194111498
   Brackets: ['mst:', '']
   Posts: 11
   Last Used: 2026-04-29 19:44:39 UTC
   Group: fraid

2. fraid
   User ID: 1493163396194111498
   Last Used: Never
```

 Enter the number of a Tupper to view its full information.

 When viewing a list, enter `b` to return to the previous menu.

 ## Search by Name

 Select `2` to search for Tuppers by name.

 The search is case-insensitive and supports partial matches.

 For example:

```
Search for a Tupper name: mist
```

 Could find:

```
mist
Misty
mister
```

 The search only returns Tuppers whose names contain the search term.

 ## Search by Brackets

 Select `3` to search for Tuppers based on their brackets.

 For example, a Tupper with:

```
"brackets": ["mst:", ""]
```

 can be found by searching:

```
Search for a bracket: mst:
```

 The search checks both the opening and closing bracket values.

 Bracket searches are case-insensitive and support partial matches.

 ## Search by Last Used

 Select `4` to sort Tuppers according to when they were last used.

 You will be prompted to choose an order:

```
1. Ascending
2. Descending
b. Back

Choose sort order:
```

 ### Ascending

 Ascending order displays Tuppers from:

```
Oldest use -> Newest use
```

 ### Descending

 Descending order displays Tuppers from:

```
Newest use -> Oldest use
```

 Tuppers without a `last_used` value are treated as having the oldest possible date and therefore appear at the beginning when sorting ascending and at the end when sorting descending.

 ## Search by Date Created

 Select `5` to sort Tuppers according to their creation date.

 You will be prompted to choose an order.

 ### Ascending

 Ascending order displays:

```
Oldest created -> Newest created
```

 ### Descending

 Descending order displays:

```
Newest created -> Oldest created
```

 Tuppers without a `created_at` value are treated as having the oldest possible date.

 ## Search by Total Messages

 Select `6` to sort Tuppers according to their total number of messages.

 The `posts` field from the Tupperbox export is used for this sorting.

 ### Ascending

 Ascending order displays:

```
Fewest messages -> Most messages
```

 ### Descending

 Descending order displays:

```
Most messages -> Fewest messages
```

 Tuppers without a valid `posts` value are treated as having `0` messages.

 For example:

```
1. character_a
   Posts: 1250

2. character_b
   Posts: 743

3. character_c
   Posts: 12
```

 ## Search by Name

 Select `7` to sort all Tuppers alphabetically by name.

 You will be prompted to choose an order.

 ### Ascending

 Ascending order displays:

```
A -> Z
```

 ### Descending

 Descending order displays:

```
Z -> A
```

 Name sorting is case-insensitive.

 For example:

```
mist
Mister
Misty
Zed
```

 will be sorted alphabetically regardless of capitalization.

 Tuppers without a name are placed according to an empty name value.

 ## Random Tupper

 Select `8` to randomly select a Tupper from the export.

 The selected Tupper will be displayed with its available information.

 ## Help

 Enter either:

```
h
```

 or:

```
help
```

 to display information about the available commands.

 ## Quit

 Enter:

```
q
```

 to exit the program.

 Commands are case-insensitive, so `Q`, `q`, `H`, and `help` will all work.

 ## Selecting a Tupper

 Whenever Tuppers are displayed as a list, each Tupper is assigned a number.

 For example:

```
1. mist
   User ID: 1493163396194111498
   Brackets: ['mst:', '']
   Posts: 11
   Last Used: 2026-04-29 19:44:39 UTC
   Group: fraid

2. another_tupper
   User ID: 123456789
   Posts: 42
   Last Used: Never
```

 Enter the corresponding number to view that Tupper's full information.

 Enter:

```
b
```

 to return to the previous menu.

 ## Supported Tupper Data

 The program can display the following fields when they are present in the export:

 - Name
- ID
- User ID
- Brackets
- Avatar
- Avatar URL
- Posts
- Group ID
- Group Name
- Description
- Tag
- Nickname
- Birthday
- Created date
- Last used date

 Missing fields and `null` values are handled without causing the program to crash.

 ## Date Handling

 Tupperbox exports use ISO 8601 timestamps for fields such as `created_at` and `last_used`.

 For example:

```
2026-04-29T19:44:39.064Z
```

 The program converts these timestamps into Python `datetime` objects when sorting.

 When displayed in Tupper lists, `last_used` timestamps are formatted as:

```
2026-04-29 19:44:39 UTC
```

 Missing or invalid dates are handled gracefully.

 ## Project Structure

 A typical project setup looks like:

```
TupperViewer/
├── tupper_viewer.py
├── run_tupper_viewer.bat
├── tuppers.json
└── README.md
```

 Your actual export file does not need to be named `tuppers.json`. You can provide any JSON filename when using the command line or drag-and-drop launcher.

 ## Windows Batch Launcher

 The included `run_tupper_viewer.bat` file allows JSON exports to be opened by dragging them onto the batch file.

 The batch file passes the dropped file as an argument to the Python program.

 For example, dragging:

```
C:\TupperViewer\my_export.json
```

 onto:

```
C:\TupperViewer\run_tupper_viewer.bat
```

 is equivalent to running:

```
python tupper_viewer.py "C:\TupperViewer\my_export.json"
```

 The batch file uses the location of the `.bat` file to find `tupper_viewer.py`, so spaces in file and folder names are supported.

 If Python is not recognized when running the batch file, make sure Python is installed and available through your system's PATH. The Windows Python launcher (`py`) can also be used in the batch file if necessary.

 ## Error Handling

 The program will report an error if:

 - The specified JSON file doesn't exist.
- The JSON file is invalid.
- The JSON doesn't contain a `tuppers` list.
- The `tuppers` value isn't a list.

 For example:

```
Error: File not found: tuppers.json
```

 or:

```
Error: Invalid JSON: Expecting ',' delimiter
```

 Invalid or missing individual Tupper fields are handled separately and generally do not prevent the program from loading the export.

 ## License

Tupper Viewer is licensed under the GNU General Public License v3.0. [Click here for more information.](https://github.com/cetteon/TupperViewer/blob/main/LICENSE)
