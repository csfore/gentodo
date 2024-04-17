# Gentodo

A simple todo app written in Python for the CLI

I made this because I got sick of keeping track of my todo stuff in a markdown 
file.

This is mostly aimed at devs and power users who need to be able to keep track
of the stuff they have to do while not having to leave their terminal.

## Features

Currently a small feature set but currently the program has:
- Human-readable data storage 
  - Can't count how many times I've seen programs use sqlite for stuff like this
- Simple enough syntax for anyone to use
- Sync Bugzilla bugs to keep track of them in one place

## Building

Gentodo currently uses setuptools as its build system so building it is extremely easy.

1. Ensure you have Python installed (Gentodo is tested on Python 3.11 and 3.12)
2. Create a virtual environment with `python -m venv .venv`
3. Source the environment with `. .venv/bin/activate`
4. Use pip to build it with `pip install .`
5. In `.venv/bin` there should now be an executable called `gentodo` and any changes in `src/gentodo` will be reflected in this executable.

## Installing

### Gentoo

#### GURU

1. Add the GURU Repository
2. `emerge -av app-misc/gentodo`

#### Local Repository

1. Put the ebuild into your local repository
2. In `package.accept_keywords` put `app-misc/gentodo ~amd64`
3. `emerge -av app-misc/gentodo::local`

## Configuration

Note: Only the first email and URL are queried for now.

The configuration file is currently stored in `~/.config/gentodo/config.toml` with the following fields:

| Name      | Type         | Description                                      |
|-----------|--------------|--------------------------------------------------|
| token     | String       | The API key for Bugzilla (overrides `token-cmd`) |
| token-cmd | String       | The command that provides a token for Bugzilla   |
| urls      | String Array | Bugzilla URLs                                    |
| emails    | String Array | Emails to query Bugzilla for                     |

## Todo for gentodo

- [x] Add ability to edit entries
  - Added in [9490b63](https://github.com/csfore/gentodo/commit/9490b63381a3f0ea7affca174d3b3eaf27bee64f)
- [x] Search ability (for those that have an infinitely growing todo list)
  - Added in [c62be08](https://github.com/csfore/gentodo/commit/9490b63381a3f0ea7affca174d3b3eaf27bee64f)
- [x] bugs.gentoo.org support?
  - bgo has an API so this might be do-able
  - Automatically add assigned bugs?
  - Broaden to bugzilla in general?
- [ ] 

# Acknowledgements

Thanks to [@immolo](https://github.com/immolo) for the name suggestion. It is far better than `todo`.
