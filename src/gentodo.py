import json
import os
import parser

STORAGE_DIR = os.path.expanduser("~/.local/share/todo")
TODO_FILE = os.path.join(STORAGE_DIR, "todo.json")

class Gentodo:

    def __init__(self):
        if not os.path.isdir(STORAGE_DIR):
            os.makedirs(STORAGE_DIR)
        self.data = self.read()
        self.longest = self.calc_length()
        self.parser = parser.setup_parser()

    def calc_length(self):
        """Calculates the longest title in the todo list"""
        longest = 0

        for todo_id in self.data:
            # Edge case in case someone doesn't put anything in
            if self.data[todo_id]['title'] == None:
                continue
            if len(self.data[todo_id]['title']) > longest:
                longest = len(self.data[todo_id]['title'])

        return longest


    def read(self):
        with open(TODO_FILE, "r") as todo:
            return json.load(todo)


    def write(self):
        with open(TODO_FILE, "w") as todo:
            json.dump(self.data, todo, indent=4)



# TODO:
# Fix long titles breaking the output
# TODO:
# Implement a form of wrapping
def show_todo(args, gentodo):
    """Shows the items to do"""
    spaces = gentodo.longest + 2
    hspaces = (spaces // 2) + 3

    # Verbose output
    if args.verbose:
        print("{} | {:<20}| {}".format("ID", "Title", "Detail"))
        print("{}".format("─" * 50))
        for key in gentodo.data:
            print(f"{key} │ {gentodo.data[key]['title']:<20}│ {gentodo.data[key]['details']}")
    elif args.brief:
        print("Title".rjust(hspaces))
        print("{}".format("─" * spaces))
        for key in gentodo.data:
            print(f"{gentodo.data[key]['title']}")
    else:
        print("{}| {}".format("Title".ljust(spaces), "Details"))
        print("{}".format("─" * int(48*1.5)))
        for key in gentodo.data:
            print("{}| {}".format(gentodo.data[key]['title'].ljust(spaces), gentodo.data[key]['details']))


def add_item(args, gentodo):
    """Adds an item to the todo list"""
    if os.path.exists(TODO_FILE) and os.path.getsize(TODO_FILE) > 0:
        #data = read_storage()
        newest_id = 0 if len(gentodo.data.keys()) == 0 else int(list(gentodo.data.keys())[-1])
    else:
        data = {}
        newest_id = 0

    if args.details is None:
        args.details = ["No", "details"]


    gentodo.data[newest_id + 1] = {
        "title": " ".join(args.title),
        "details": " ".join(args.details)
    }

    gentodo.write()
    print(f"Added: {' '.join(args.title)} | {' '.join(args.details)}")


def rm_item(args, gentodo):
    """Removes an item from the todo list by ID"""
    if os.path.exists(TODO_FILE) and os.path.getsize(TODO_FILE) > 0:
        gentodo.data.pop("{0}".format(args.id))
        gentodo.write()


def item_count(args, gentodo):
    """Tallies up the amount of items in the list"""

    remaining = len(gentodo.data.keys())
    print(f"Items remaining: {remaining}")


def edit_item(args, gentodo):
    """Edits an item entry"""
    gentodo.data[args.id]['title'] = " ".join(args.title)
    gentodo.data[args.id]['details'] = " ".join(args.details)

    gentodo.write()


def search_items(args, gentodo):
    print(f"Searching for: {args.term}\n\n")
    print("ID | Title")
    print("{}".format("─" * int(gentodo.longest/2)))
    for key in gentodo.data:
        for val in gentodo.data[key]:
            if args.term in gentodo.data[key][val]:
                print("{} | {}".format(key, gentodo.data[key][val]))
