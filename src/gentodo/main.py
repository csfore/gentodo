import click

from gentodo import commands, __version__


@click.group(invoke_without_command=True)
@click.version_option(__version__)
@click.option('--verbose', '-v', default=False, is_flag=True)
@click.option('--brief', '-b', default=None, type=str)
@click.pass_context
def cmd(ctx, verbose, brief):
    '''General purpose command group'''
    ctx.ensure_object(dict)
    ctx.obj['GENTODO'] = commands.Gentodo()
    if ctx.invoked_subcommand is None:
        ctx.forward(commands.show)


@cmd.group()
@click.pass_context
def bugs(ctx):
    '''Bugs command group'''
    ctx.ensure_object(dict)
    ctx.obj['GENTODO'] = commands.Gentodo()

cmd.add_command(commands.show)
cmd.add_command(commands.add)
cmd.add_command(commands.rm)
cmd.add_command(commands.count)
cmd.add_command(commands.edit)
cmd.add_command(commands.search)
bugs.add_command(commands.pull_bugs)


def main():
    '''Main entrypoint'''
    cmd()

if __name__ == "__main__":
    # Alternative Entrypoint
    main()
