#!/usr/bin/env python
# (c) 2023 Christopher Fore
# This code is licensed under the GPLv3 license (see LICENSE for details)

__version__ = '0.0.3'

import json
import os
import argparse

STORAGE_DIR = os.path.expanduser("~/.local/share/todo")
TODO_FILE = os.path.join(STORAGE_DIR, "todo.json")

def read_storage():
    with open(TODO_FILE, "r") as todo:
        return json.load(todo)

def write_storage(data):
    with open(TODO_FILE, "w") as todo:
        json.dump(data, todo, indent=4)

def show_todo(args):
    '''Shows the items to do'''
    #print(f"ID entered: {args.id}")
    
    # If the file cannot be opened, there is nothing to do, implying it has not
    # been made yet.
    try:
        data = read_storage()
    except FileNotFoundError:
        print("Nothing to do!")
        return

    #if args.id is not None:
    #    print(type(args.id))
    #    print(f"{data[args.id]}")

    # Verbose output
    if args.verbose:    
        print("ID\tItem\tDetails")
        print("=======================")
        for key in data:
            print(f"{key}\t{data[key]['title']}\t{data[key]['details']}")
    else:
        print("Title\tDetails")
        for key in data:
            print(f"{data[key]['title']}\t{data[key]['details']}")


def add_item(args):
    '''Adds an item to the todo list'''
    if os.path.exists(TODO_FILE) and os.path.getsize(TODO_FILE) > 0:
        data = read_storage()
        newest_id = 0 if len(data.keys()) == 0 else int(list(data.keys())[-1])
    else:
        data = {}
        newest_id = 0
    
    data[newest_id + 1] = { 
        "title": " ".join(args.title),
        "details": " ".join(args.details)
    }

    write_storage(data)
    print(f"Added: {' '.join(args.title)} | {' '.join(args.details)}")


def rm_item(args):
    '''Removes an item from the todo list by ID'''
    if os.path.exists(TODO_FILE) and os.path.getsize(TODO_FILE) > 0:
        data = read_storage()
        data.pop("{0}".format(args.id))
        
        write_storage(data)

def item_count(args):
    '''Tallies up the amount of items in the list'''
    data = read_storage()
        
    remaining = len(data.keys())
    print(f"Items remaining: {remaining}")


def edit_item(args):
    '''Edits an item entry'''
    data = read_storage()

    data[args.id]['title'] = " ".join(args.title)
    data[args.id]['details'] = " ".join(args.details)
    
    write_storage(data)


def search_items():
    print(f"Searching for: {args.term}")



def setup_parser():
    '''Sets up the parser and adds arguments'''

    # Main parser
    parser = argparse.ArgumentParser(usage="todo <command> [-h]")
    parser.add_argument('--version', action='version', version='0.0.1')
    parser.add_argument('-v', '--verbose', action='store_true',help="Be descriptive about output (i.e. show item IDs)")
    #parser.add_argument('id')
    parser.set_defaults(func=show_todo)
    
    subparsers = parser.add_subparsers(help='sub-command help', metavar='')
    
    # Parser for adding items
    add_parser = subparsers.add_parser('add', help="Add an item to your todo list", usage="todo add [-h] -t <title> -d <details>")
    add_parser.add_argument('-t', '--title', nargs='+', help="Item to add to your todo list")
    add_parser.add_argument('-d', '--details', nargs='+', help="Add some information to your item")
    add_parser.set_defaults(func=add_item)
    
    # Parser for removing items
    del_parser = subparsers.add_parser('del', help="Remove an item from your todo list", usage="todo rm <id>")
    del_parser.add_argument('id', help="ID to remove from your todo list")
    del_parser.set_defaults(func=rm_item)

    # Parser for counting items
    count_parser = subparsers.add_parser('count', help="Shows your remaining item count")
    count_parser.set_defaults(func=item_count)

    # Parser for editing
    edit_parser = subparsers.add_parser('edit', help="Edit an item by id", usage="todo edit <id> -t <title> -d <details>")
    edit_parser.add_argument('id')
    edit_parser.add_argument('-t', '--title', nargs='+', help="New title")
    edit_parser.add_argument('-d', '--details', nargs='+', help="New details")
    edit_parser.set_defaults(func=edit_item)

    # Parser for searching
    search_parser = subparsers.add_parser('search', help="Search for an item", usage="todo search [term]")
    search_parser.add_argument('term')
    search_parser.set_defaults(func=search_items)

    return parser


def main():
    if not os.path.isdir(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
    parser = setup_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
