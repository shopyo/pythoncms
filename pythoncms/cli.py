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
import os
import subprocess
import sys
from pathlib import Path

import click
from shopyo.api.file import trycopytree
from shopyo.api.file import trymkfile
from shopyo.api.file import tryrmfile

from pythoncms import __version__

path = Path(__file__)


@click.group()
@click.version_option(__version__)
def cli():
    """pythoncms CLI - The fastest way to build CMS in Python"""
    pass


@cli.command("start")
@click.argument("name")
@click.option("--run", is_flag=True, help="Initialize and run the server immediately")
def start(name, run):
    """Create a new pythoncms project"""
    dest = os.path.join(os.getcwd(), name)

    if os.path.exists(dest):
        click.echo(f"Error: Directory {name} already exists.")
        return

    # Copy the project structure
    # We copy the parent of this file (pythoncms/ directory)
    # but we need to exclude things like __pycache__ and cli.py from the target if needed
    # actually the original logic was trycopytree(str(path.parent.absolute()), dest)
    trycopytree(str(path.parent.absolute()), dest)
    
    # Cleanup target
    tryrmfile(os.path.join(dest, "cli.py"))
    
    # Create requirements.txt
    reqs = f"pythoncms=={__version__}"
    trymkfile(os.path.join(dest, "requirements.txt"), reqs)
    
    # Setup .env
    env_demo = os.path.join(dest, ".env_demo")
    env_real = os.path.join(dest, ".env")
    if os.path.exists(env_demo):
        os.rename(env_demo, env_real)
    
    click.echo(f"🍭  Pythoncms project {name} is ready!")

    if run:
        os.chdir(dest)
        click.echo("Running initialization...")
        subprocess.run(["shopyo", "initialise"], check=True)
        click.echo("Seeding database...")
        subprocess.run(["flask", "shopyo-seed"], check=True)
        click.echo("Starting server...")
        subprocess.run(["flask", "--debug", "run"], check=True)


@cli.command("initialise")
def initialise():
    """Initialise the project database and assets"""
    subprocess.run(["shopyo", "initialise"], check=True)


@cli.command("seed")
def seed():
    """Seed the database with default data"""
    subprocess.run(["flask", "shopyo-seed"], check=True)


@cli.command("run")
@click.option("--debug", is_flag=True, default=True)
def run(debug):
    """Run the development server"""
    args = ["flask"]
    if debug:
        args.append("--debug")
    args.append("run")
    subprocess.run(args, check=True)
