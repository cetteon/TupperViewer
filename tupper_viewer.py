#!/usr/bin/env python3

import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path


SEPARATOR = "=" * 50


def error_exit(message):
    """Display an error, wait for acknowledgement, then exit."""
    print(f"\nError: {message}")
    input("\nPress Enter to exit...")
    sys.exit(1)


def load_export(filename):
    """Load a Tupper export JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        error_exit(f"File not found: {filename}")
    except json.JSONDecodeError as e:
        error_exit(f"Invalid JSON: {e}")

    if not isinstance(data, dict) or "tuppers" not in data:
        error_exit("JSON file does not contain a 'tuppers' list.")

    if not isinstance(data["tuppers"], list):
        error_exit("'tuppers' is not a list.")

    return data["tuppers"]


def print_header(title):
    """Print a consistent section header."""
    print(f"\n{SEPARATOR}")
    print(title)
    print(SEPARATOR)


def get_last_used(tupper):
    """Return a Tupper's last_used timestamp as a datetime."""
    last_used = tupper.get("last_used")

    if not last_used:
        return None

    try:
        return datetime.fromisoformat(
            last_used.replace("Z", "+00:00")
        )
    except (ValueError, TypeError):
        return None


def get_created_at(tupper):
    """Return a Tupper's created_at timestamp as a datetime."""
    created_at = tupper.get("created_at")

    if not created_at:
        return None

    try:
        return datetime.fromisoformat(
            created_at.replace("Z", "+00:00")
        )
    except (ValueError, TypeError):
        return None


def format_last_used(tupper):
    """Return a human-readable last-used timestamp."""
    last_used = get_last_used(tupper)

    if last_used is None:
        return "Never"

    return last_used.strftime("%Y-%m-%d %H:%M:%S UTC")


def display_tupper(tupper, number=None):
    """Display information about a single Tupper."""
    if number is not None:
        print_header(f"Tupper #{number}")
    else:
        print_header("Random Tupper")

    fields = [
        ("Name", "name"),
        ("ID", "id"),
        ("User ID", "user_id"),
        ("Brackets", "brackets"),
        ("Avatar", "avatar"),
        ("Avatar URL", "avatar_url"),
        ("Posts", "posts"),
        ("Group ID", "group_id"),
        ("Group Name", "group_name"),
        ("Description", "description"),
        ("Tag", "tag"),
        ("Nickname", "nick"),
        ("Birthday", "birthday"),
        ("Created", "created_at"),
        ("Last Used", "last_used"),
    ]

    for label, key in fields:
        if key not in tupper:
            continue

        value = tupper[key]

        if value is None:
            value = "None"

        print(f"{label}: {value}")


def display_list(tuppers):
    """Display a numbered list of tuppers."""
    print_header("Tupper Export")

    if not tuppers:
        print("No tuppers found.")
        return

    for number, tupper in enumerate(tuppers, start=1):
        name = tupper.get("name", "Unnamed")
        user_id = tupper.get("user_id", "Unknown")

        print(f"{number}. {name}")
        print(f"   User ID: {user_id}")

        brackets = tupper.get("brackets")
        if brackets:
            print(f"   Brackets: {brackets}")

        posts = tupper.get("posts")
        if posts is not None:
            print(f"   Posts: {posts}")

        last_used = tupper.get("last_used")
        if last_used:
            print(f"   Last Used: {format_last_used(tupper)}")
        else:
            print("   Last Used: Never")

        group_name = tupper.get("group_name")
        if group_name:
            print(f"   Group: {group_name}")

        print()


def search_tuppers_by_name(tuppers, query):
    """Return tuppers whose names contain the search query."""
    query = query.lower()

    return [
        tupper
        for tupper in tuppers
        if query in tupper.get("name", "").lower()
    ]


def search_tuppers_by_brackets(tuppers, query):
    """Return tuppers whose brackets contain the search query."""
    query = query.lower()

    results = []

    for tupper in tuppers:
        brackets = tupper.get("brackets")

        if not brackets or not isinstance(brackets, list):
            continue

        for bracket in brackets:
            if bracket and query in bracket.lower():
                results.append(tupper)
                break

    return results


def sort_tuppers_by_last_used(tuppers, descending=True):
    """Sort tuppers by last used date."""
    return sorted(
        tuppers,
        key=lambda tupper: (
            get_last_used(tupper)
            or datetime.min.replace(tzinfo=timezone.utc)
        ),
        reverse=descending
    )


def sort_tuppers_by_created_at(tuppers, descending=True):
    """Sort tuppers by creation date."""
    return sorted(
        tuppers,
        key=lambda tupper: (
            get_created_at(tupper)
            or datetime.min.replace(tzinfo=timezone.utc)
        ),
        reverse=descending
    )


def sort_tuppers_by_posts(tuppers, descending=True):
    """Sort tuppers by total messages."""
    def get_posts(tupper):
        posts = tupper.get("posts")

        if posts is None:
            return 0

        try:
            return int(posts)
        except (ValueError, TypeError):
            return 0

    return sorted(
        tuppers,
        key=get_posts,
        reverse=descending
    )


def sort_tuppers_by_name(tuppers, descending=False):
    """Sort tuppers alphabetically by name."""
    return sorted(
        tuppers,
        key=lambda tupper: tupper.get("name", "").casefold(),
        reverse=descending
    )


def select_sort_order():
    """Ask the user whether to sort ascending or descending."""
    while True:
        print()
        print("1. Ascending")
        print("2. Descending")
        print("b. Back")

        choice = input("\nChoose sort order: ").strip().lower()

        if choice == "1":
            return False

        if choice == "2":
            return True

        if choice == "b":
            return None

        print("\nPlease enter 1, 2, or 'b'.")


def select_tupper(tuppers):
    """Allow the user to select a Tupper from a list."""
    if not tuppers:
        print("\nNo tuppers found.")
        input("\nPress Enter to continue...")
        return

    while True:
        display_list(tuppers)

        choice = input(
            "\nSelect a Tupper number, or 'b' to go back: "
        ).strip()

        if choice.lower() == "b":
            return

        try:
            number = int(choice)
        except ValueError:
            print("\nPlease enter a valid number.")
            continue

        if number < 1 or number > len(tuppers):
            print(f"\nPlease enter a number between 1 and {len(tuppers)}.")
            continue

        display_tupper(tuppers[number - 1], number)

        input("\nPress Enter to return to the list...")


def random_tupper(tuppers):
    """Select and display a random Tupper."""
    if not tuppers:
        print("\nNo tuppers found.")
        input("\nPress Enter to continue...")
        return

    tupper = random.choice(tuppers)

    display_tupper(tupper)

    input("\nPress Enter to return to the main menu...")


def display_help():
    """Display information about available commands."""
    print_header("Help")

    print("""
1. View all tuppers
   Displays every Tupper in the export.
   You can select one by entering its number.

2. Search by name
   Searches Tupper names using partial, case-insensitive
   matching.

   Example:
       Search for a Tupper name: mist

   This could match:
       mist
       Mister
       Misty

3. Search by brackets
   Searches both the opening and closing brackets of
   each Tupper.

   Example:
       Search for a bracket: mst:

   This will find a Tupper with:
       ['mst:', '']

4. Search by last used
   Sorts all tuppers by when they were last used.

   You can choose:
       Ascending: oldest use -> newest use
       Descending: newest use -> oldest use

   Tuppers that have never been used are treated as
   having the oldest possible date.

5. Search by date created
   Sorts all tuppers by their creation date.

   You can choose:
       Ascending: oldest -> newest
       Descending: newest -> oldest

   Tuppers without a creation date are treated as
   having the oldest possible date.

6. Search by total messages
   Sorts all tuppers by their total number of messages.

   You can choose:
       Ascending: fewest -> most
       Descending: most -> fewest

7. Search by name
   Sorts all tuppers alphabetically by name.

   You can choose:
       Ascending: A -> Z
       Descending: Z -> A

   Sorting is case-insensitive.

8. Random Tupper
   Selects one Tupper at random from the entire export.

h / help
   Displays this help message.

q
   Quits the program.

Inside a Tupper list:
   Enter a number to view that Tupper.
   Enter 'b' to go back.
""")


def main():
    if len(sys.argv) != 2:
        error_exit(
            f"Usage: python {Path(sys.argv[0]).name} <tuppers.json>"
        )

    filename = sys.argv[1]
    tuppers = load_export(filename)

    while True:
        print_header("Tupper Viewer")

        print(f"Total tuppers: {len(tuppers)}")
        print()
        print("1. View all tuppers")
        print("2. Search by name")
        print("3. Search by brackets")
        print("4. Search by last used")
        print("5. Search by date created")
        print("6. Search by total messages")
        print("7. Search by name")
        print("8. Random Tupper")
        print("h. Help")
        print("q. Quit")

        choice = input("\nChoose an option: ").strip().lower()

        if choice == "q":
            print("\nGoodbye!")
            break

        elif choice == "1":
            select_tupper(tuppers)

        elif choice == "2":
            query = input("\nSearch for a Tupper name: ").strip()

            if not query:
                print("\nPlease enter a search term.")
                continue

            results = search_tuppers_by_name(tuppers, query)

            print(f"\nFound {len(results)} matching Tupper(s).")

            if results:
                select_tupper(results)
            else:
                input("\nPress Enter to return to the main menu...")

        elif choice == "3":
            query = input("\nSearch for a bracket: ").strip()

            if not query:
                print("\nPlease enter a search term.")
                continue

            results = search_tuppers_by_brackets(tuppers, query)

            print(f"\nFound {len(results)} matching Tupper(s).")

            if results:
                select_tupper(results)
            else:
                input("\nPress Enter to return to the main menu...")

        elif choice == "4":
            print_header("Search by Last Used")

            descending = select_sort_order()

            if descending is not None:
                results = sort_tuppers_by_last_used(
                    tuppers,
                    descending=descending
                )
                select_tupper(results)

        elif choice == "5":
            print_header("Search by Date Created")

            descending = select_sort_order()

            if descending is not None:
                results = sort_tuppers_by_created_at(
                    tuppers,
                    descending=descending
                )
                select_tupper(results)

        elif choice == "6":
            print_header("Search by Total Messages")

            descending = select_sort_order()

            if descending is not None:
                results = sort_tuppers_by_posts(
                    tuppers,
                    descending=descending
                )
                select_tupper(results)

        elif choice == "7":
            print_header("Search by Name")

            descending = select_sort_order()

            if descending is not None:
                results = sort_tuppers_by_name(
                    tuppers,
                    descending=descending
                )
                select_tupper(results)

        elif choice == "8":
            random_tupper(tuppers)

        elif choice in ("h", "help"):
            display_help()
            input("\nPress Enter to return to the main menu...")

        else:
            print("\nInvalid option. Enter 'h' for help.")


if __name__ == "__main__":
    main()
