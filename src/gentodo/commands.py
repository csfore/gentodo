'''Module for the Gentodo class and its cli functions'''

import json
import os
import click

from gentodo import bugs

OLD_PATH = os.path.expanduser("~/.local/share/todo/todo.json")
STORAGE_DIR = os.path.join(
    os.getenv('XDG_DATA_HOME', os.path.expanduser("~/.local/share")),
    "gentodo")
TODO_FILE = os.path.join(STORAGE_DIR, "todo.json")

class Gentodo:
    '''Main class for parsing the todo file and storing data'''

    __slots__ = ["data", "longest"]

    def __init__(self):
        if os.path.isfile(OLD_PATH):
            os.rename(OLD_PATH, TODO_FILE)

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
            longest = max(longest, len((self.data[todo_id]['title'])))

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
@click.command(help="Shows the todo list")
@click.pass_context
@click.option("--verbose", is_flag=True)
@click.option("--brief", type=click.STRING, default='left', required=False)
def show(ctx, verbose, brief):
    '''Shows the items to do'''
    spaces = ctx.obj['GENTODO'].longest + 2

    if ctx.obj['GENTODO'].data is None:
        print("Nothing to do!")
        return

    # Verbose output
    if verbose:
        print(f"ID | {'Title'.ljust(spaces)}| Detail")
        print(f"{'─'*(spaces+14)}")
        for key in ctx.obj['GENTODO'].data:
            print(f"{key:<2} │ {ctx.obj['GENTODO'].data[key]['title'].ljust(spaces)}"\
                  f"│ {ctx.obj['GENTODO'].data[key]['details']}")
    elif brief:
        print("Title".center(spaces))
        print(f"{'─'*spaces}")
        for key in ctx.obj['GENTODO'].data:
            title = ctx.obj['GENTODO'].data[key]['title']
            print(title)
            match brief:
                case 'left':
                    print(title)
                case 'center':
                    print(title.center(spaces))
                case 'right':
                    print(title.rjust(spaces))
    else:
        print(f"{'Title'.ljust(spaces)}| Details")
        print(f"{'─'*(spaces+9)}")
        for key in ctx.obj['GENTODO'].data:
            print(f"{ctx.obj['GENTODO'].data[key]['title'].ljust(spaces)}"\
                  f"| {ctx.obj['GENTODO'].data[key]['details']}")


@click.command(help="Add an item to your todo list")
@click.pass_context
@click.option("-t", "--title", required=True)
@click.option("-d", "--details", default="No details")
def add(ctx, title, details):
    '''Adds an item to the todo list'''
    gentodo = ctx.obj['GENTODO']

    newest_id = 0 if len(gentodo.data.keys()) == 0 else int(list(gentodo.data.keys())[-1])

    if len(title) > 40:
        title = title[:40]
        title += "..."

    gentodo.data[newest_id + 1] = {
        "title": title,
        "details": details
    }

    gentodo.write()
    print(f"Added: {title} | {details}")


@click.command(name="del", help="Remove an item from the todo list")
@click.pass_context
@click.argument("id_", metavar="ID")
def rm(ctx, id_):
    '''Removes an item from the todo list by ID'''
    gentodo = ctx.obj['GENTODO']

    if os.path.exists(TODO_FILE) and os.path.getsize(TODO_FILE) > 0:
        gentodo.data.pop(f"{id_}")
        gentodo.write()

@click.command(help="Shows the number of items remaining")
@click.pass_context
def count(ctx):
    '''Tallies up the amount of items in the list'''
    gentodo = ctx.obj['GENTODO']

    remaining = len(gentodo.data.keys())
    print(f"Items remaining: {remaining}")


@click.command(help="Edit an item by ID")
@click.pass_context
@click.argument("id_", metavar="ID")
@click.option("-t", "--title", required=True)
@click.option("-d", "--details", default="No details")
def edit(ctx, id_, title, details):
    '''Edits an item entry'''
    gentodo = ctx.obj['GENTODO']

    gentodo.data[id_]['title'] = title
    gentodo.data[id_]['details'] = details

    gentodo.write()


@click.command(help="Search for an item")
@click.pass_context
@click.argument("term")
def search(ctx, term):
    '''Searches for an item in the todo list'''
    gentodo = ctx.obj['GENTODO']
    print(f"Searching for: {term}\n")
    print("ID | Title")
    print(f"{'─'*int(gentodo.longest/2)}")
    for key in gentodo.data:
        for val in gentodo.data[key]:
            if term in gentodo.data[key][val]:
                print(f"{key} | {gentodo.data[key][val]}")


@click.command(name="pull", help="Pulls bugs relating to you from the Bugzilla")
@click.pass_context
@click.option("-c", "--cc", is_flag=True)
@click.option("-a", "--assigned", is_flag=True)
def pull_bugs(ctx, cc, assigned):
    '''Pulls bugs from the Bugzillas'''
    bz = bugs.Bugs()
    allbugs = []
    if cc:
        cced = bz.get_cced()
        for bug in cced:
            bug = "[BUGZILLA] " + f"{bug}"
            allbugs.append(bug)

    if assigned:
        assigned = bz.get_assigned()
        for bug in assigned:
            bug = "[BUGZILLA]" + f"{bug}"
            allbugs.append(bug)

    # Make sure bugs are unique
    set(allbugs)

    for bug in allbugs:
        # Passing it over to add to actually add the bug
        ctx.invoke(add, title=bug)
