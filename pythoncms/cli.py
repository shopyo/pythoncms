"""
file: cli.py
description: Add your custom cli commands here
documentation: https://click.palletsprojects.com/en/7.x/

You will need to run ``python -m pip install -e .`` to load the setup.py
which contains the entry point to this file before being able to run your
custom commands

Usage ``pythoncms [OPTIONS] COMMAND [ARGS]...``

Example command 'welcome' has been added.
- To get your project version, run ``pythoncms --version``
- Run the sample command as ``pythoncms welcome [OPTIONS] NAME``
"""
from pathlib import Path

import click
from shopyo.api.file import trycopytree
from shopyo.api.file import trymkfile
from shopyo.api.file import tryrmfile
from shopyo.api.file import tryrmtree

from pythoncms import __version__

path = Path(__file__)
import os


@click.group()
@click.version_option(__version__)
@click.pass_context
def cli(ctx):
    """CLI entry point"""
    pass


# @cli.command("welcome")
# @click.argument("name")
# @click.option("--verbose", "-v", is_flag=True, default=False)
# def welcome(name, verbose):
#     """Sample command to welcome users.

#     NAME will be printed along with the welcome message
#     """
#     click.secho(f"Hi {name}. Welcome to pythoncms", fg="cyan")

#     if verbose:
#         click.echo("See you soon")

reqs = f"""pythoncms=={__version__}"""


@cli.command("start")
@click.argument("name")
def start(name):
    """
    New project
    """
    dest = os.getcwd() + f"/{name}"

    trycopytree(str(path.parent.absolute()), dest)
    tryrmfile(dest + "/cli.py")
    trymkfile(dest + "/requirements.txt", reqs)
    try:
        os.rename('.env_demo', '.env')
    except Exception as e:
        print(e)
    click.echo(f"🍭  Pythoncms project {name} is ready to go!")
