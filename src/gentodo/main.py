#!/usr/bin/env python
# (c) 2023 Christopher Fore
# This code is licensed under the GPLv3 license (see LICENSE for details)

import os
from gentodo import cli
import bugzilla
import argparse


def setup_parser():
    """Sets up the parser and adds arguments"""

    # Main parser
    parser = argparse.ArgumentParser(usage="gentodo <command> [-h]")
    parser.add_argument('--version', action='version', version='0.0.1')
    parser.add_argument('-v', '--verbose', action='store_true',help="Be descriptive about output (i.e. show item IDs)")
    parser.add_argument('-b', '--brief', action='store_true', help="Show just the title")
    parser.set_defaults(func=cli.show_todo)
    
    subparsers = parser.add_subparsers(help='sub-command help', metavar='')
    
    # Parser for adding items
    add_parser = subparsers.add_parser('add', help="Add an item to your todo list", usage="gentodo add [-h] -t <title> -d <details>")
    add_parser.add_argument('-t', '--title', nargs='+', help="Item to add to your todo list")
    add_parser.add_argument('-d', '--details', nargs='+', help="Add some information to your item")
    add_parser.set_defaults(func=cli.add_item)
    
    # Parser for removing items
    del_parser = subparsers.add_parser('del', help="Remove an item from your todo list", usage="gentodo del <id>")
    del_parser.add_argument('id', help="ID to remove from your todo list")
    del_parser.set_defaults(func=cli.rm_item)

    # Parser for counting items
    count_parser = subparsers.add_parser('count', help="Shows your remaining item count")
    count_parser.set_defaults(func=cli.item_count)

    # Parser for editing
    edit_parser = subparsers.add_parser('edit', help="Edit an item by id", usage="gentodo edit <id> -t <title> -d <details>")
    edit_parser.add_argument('id')
    edit_parser.add_argument('-t', '--title', nargs='+', help="New title")
    edit_parser.add_argument('-d', '--details', nargs='+', help="New details")
    edit_parser.set_defaults(func=cli.edit_item)

    # Parser for searching
    search_parser = subparsers.add_parser('search', help="Search for an item", usage="gentodo search [term]")
    search_parser.add_argument('term')
    search_parser.set_defaults(func=cli.search_items)

    return parser


def main():
    todo = cli.Gentodo()
    parser = setup_parser()

    args = parser.parse_args()
    args.func(args, todo)

if __name__ == "__main__":
    main()
