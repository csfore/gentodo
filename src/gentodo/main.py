'''Gentodo (c) 2023 Christopher Fore
This code is licensed under the GPLv3 license (see LICENSE for details)
'''

#import bugzilla // commented out until used
from gentodo import cli, parser

def main():
    '''Main function'''
    todo = cli.Gentodo()
    unparsed = parser.setup_parser()

    args = unparsed.parse_args()
    args.func(args, todo)

if __name__ == "__main__":
    main()
