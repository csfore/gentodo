# Todo

A simple todo app written in Python for the CLI

I made this because I got sick of keeping track of my todo stuff in a markdown 
file.

This is mostly aimed at devs and power users who need to be able to keep track
of the stuff they have to do while not having to leave their terminal.

## Features

Currently a small feature set but currently the program has:
- Human-readable data storage 
  - Can't count how many times I've seen programs use sqlite for stuff like this)
- 0 external dependencies outside of Python 3 (as of 2023-11-22)
  - Might use Click? See Todo
- Simple enough syntax for anyone to use

## Installing

### Gentoo

1. Put the ebuild into your local repository
2. `emerge gentodo::local` or `ebuild ./gentodo-9999.ebuild clean install merge`

That's it! Gentodo will update automagically now since it is a git ebuild.

### Other

Note: you'll have to update manually if you do this method

1. Copy `./todo` to a place in PATH (probably `/usr/bin`)
2. Enjoy!

## Todo for todo

- [x] Add ability to edit entries
  - Added in [9490b63](https://github.com/csfore/gentodo/commit/9490b63381a3f0ea7affca174d3b3eaf27bee64f)
- [x] Search ability (for those that have an infinitely growing todo list)
  - Added in [c62be08](https://github.com/csfore/gentodo/commit/9490b63381a3f0ea7affca174d3b3eaf27bee64f)
- [ ] Refactor/rewrite in other language? 
  - Not sure how wise or doable this would be. Current candidates are Rust, Go, or Racket.
  - If refactor, using the Click library maybe? I'd rather keep dependencies to a minimum though
- [ ] bugs.gentoo.org support?
  - bgo has an API so this might be do-able
  - Automatically add assigned bugs?
  - Broaden to bugzilla in general?
- [ ] motd in the terminal for when a user logs in?
  - Can somewhat be done already with `todo count` but could be better
