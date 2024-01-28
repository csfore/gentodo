'''Module for the Gentodo class and its cli functions'''

import json
import os
from gentodo import bugs

OLD_PATH = os.path.expanduser("~/.local/share/todo/todo.json")
STORAGE_DIR = os.path.expanduser("~/.local/share/gentodo")
TODO_FILE = os.path.join(STORAGE_DIR, "todo.json")

class Gentodo:
    '''Main class for parsing the todo file and storing data'''

    __slots__ = ["data", "longest"]

    def __init__(self):
        try:
            if os.path.isfile(OLD_PATH):
                os.rename(OLD_PATH, TODO_FILE)
        except:
            pass

        if not os.path.isdir(STORAGE_DIR):
            os.makedirs(STORAGE_DIR)

        if not os.path.isfile(TODO_FILE):
            with open(TODO_FILE, "w", encoding="utf_8") as todo:
                json.dump({}, todo, indent=4)

        self.data = self.read()
        self.longest = self.calc_length()

    def calc_length(self):
        '''Calculates the longest title in the todo list'''
        longest = 0

        if self.data is None:
            return longest

        for todo_id in self.data:
            # Edge case in case someone doesn't put anything in
            if self.data[todo_id]['title'] is None:
                continue
            if len(self.data[todo_id]['title']) > longest:
                longest = len(self.data[todo_id]['title'])

        return longest


    def read(self):
        '''Reads from the todo file into `data`'''
        with open(TODO_FILE, "r", encoding="utf_8") as todo:
            try:
                data = json.load(todo)
            except json.decoder.JSONDecodeError:
                return None
            return data


    def write(self):
        '''Writes `data` into the todo file'''
        with open(TODO_FILE, "w", encoding="utf_8") as todo:
            json.dump(self.data, todo, indent=4)



# TODO:
# Fix long titles breaking the output
# TODO:
# Implement a form of wrapping
def show_todo(args, gentodo):
    '''Shows the items to do'''
    spaces = gentodo.longest + 2

    if gentodo.data is None:
        print("Nothing to do!")
        return

    # Verbose output
    if args.verbose:
        print(f"ID | {'Title'.ljust(spaces)}| Detail")
        print(f"{'─'*(spaces+14)}")
        for key in gentodo.data:
            print(f"{key:<2} │ {gentodo.data[key]['title'].ljust(spaces)}│ {gentodo.data[key]['details']}")
    elif args.brief:
        print("Title".center(spaces))
        print(f"{'─'*spaces}")
        for key in gentodo.data:
            title = gentodo.data[key]['title']
            match args.brief:
                case 'left':
                    print(title)
                case 'center':
                    print(title.center(spaces))
                case 'right':
                    print(title.rjust(spaces))
    else:
        print(f"{'Title'.ljust(spaces)}| Details")
        print(f"{'─'*(spaces+9)}")
        for key in gentodo.data:
            print(f"{gentodo.data[key]['title'].ljust(spaces)}| {gentodo.data[key]['details']}")


def add_item(args, gentodo):
    '''Adds an item to the todo list'''
    newest_id = 0 if len(gentodo.data.keys()) == 0 else int(list(gentodo.data.keys())[-1])

    if args.details is None:
        args.details = ["No", "details"]

    if args.title is None:
        print("Missing required title argument, did you forget `-t`?")
        return
    
    title = args.title
    if type(title) is not str:
        title = " ".join(title)
    if len(title) > 40:
        title = title[:40]
        title += "..."

    gentodo.data[newest_id + 1] = {
        "title": title,
        "details": " ".join(args.details)
    }

    gentodo.write()
    print(f"Added: {title} | {' '.join(args.details)}")


def rm_item(args, gentodo):
    '''Removes an item from the todo list by ID'''
    if os.path.exists(TODO_FILE) and os.path.getsize(TODO_FILE) > 0:
        gentodo.data.pop(f"{args.id}")
        gentodo.write()


def item_count(args, gentodo):
    '''Tallies up the amount of items in the list'''

    remaining = len(gentodo.data.keys())
    print(f"Items remaining: {remaining}")


def edit_item(args, gentodo):
    '''Edits an item entry'''
    gentodo.data[args.id]['title'] = " ".join(args.title)
    gentodo.data[args.id]['details'] = " ".join(args.details)

    gentodo.write()


def search_items(args, gentodo):
    '''Searches for an item in the todo list'''
    print(f"Searching for: {args.term}\n\n")
    print("ID | Title")
    print(f"{'─'*int(gentodo.longest/2)}")
    for key in gentodo.data:
        for val in gentodo.data[key]:
            if args.term in gentodo.data[key][val]:
                print(f"{key} | {gentodo.data[key][val]}")

def pull_bugs(args, gentodo):
    bz = bugs.Bugs()
    allbugs = []
    if args.cc:
        cced = bz.get_cced()
        for bug in cced:
            bug = "[BUGZILLA] " + f"{bug}"
            allbugs.append(bug)

    if args.assigned:
        assigned = bz.get_assigned()
        for bug in assigned:
            bug = "[BUGZILLA]" + f"{bug}"
            allbugs.append(bug)
    
    # Make sure bugs are unique
    set(allbugs)

    for bug in allbugs:
        args.title = bug
        args.details = None
        add_item(args, gentodo)
