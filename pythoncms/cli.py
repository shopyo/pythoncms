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
import secrets
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
@click.version_option(__version__, prog_name="pythoncms")
def cli():
    """pythoncms CLI - The fastest way to build CMS in Python"""
    pass


@cli.command("start")
@click.argument("name")
@click.option("--run", is_flag=True, help="Initialize and run the server immediately")
def start(name, run):
    """Create a new pythoncms project"""
    dest = os.path.abspath(name)

    if os.path.exists(dest):
        click.echo(f"Error: Directory {name} already exists.")
        return


    # Copy the project structure
    trycopytree(str(path.parent.absolute()), dest)
    
    # Cleanup target
    tryrmfile(os.path.join(dest, "cli.py"))
    
    # Create requirements.txt
    reqs = f"pythoncms=={__version__}"
    trymkfile(os.path.join(dest, "requirements.txt"), reqs)
    
    # Setup .env
    env_real = os.path.join(dest, ".env")
    
    env_content = f"""ACTIVE_FRONT_THEME = 'editorial'
ACTIVE_BACK_THEME = 'sneat'
APP_NAME = 'Demo'
ACTIVE_ICONSET = 'boxicons'
SITE_TITLE = 'Site title'
SITE_DESCRIPTION = 'Site title'
SECRET_KEY = '{secrets.token_hex(32)}'
"""
    trymkfile(env_real, env_content)
    
    click.echo(f"🍭  Pythoncms project {name} is ready!")

    if run:
        os.chdir(dest)
        click.echo("Running initialization...")
        bin_dir = os.path.dirname(sys.executable)
        shopyo_cmd = os.path.join(bin_dir, "shopyo")
        flask_cmd = os.path.join(bin_dir, "flask")
        
        subprocess.run([shopyo_cmd, "initialise"], check=True)
        click.echo("Seeding database...")
        subprocess.run([flask_cmd, "shopyo-seed"], check=True)
        click.echo("Starting server...")
        subprocess.run([flask_cmd, "--debug", "run"], check=True)


@cli.command("initialise")
def initialise():
    """Initialise the project database and assets"""
    bin_dir = os.path.dirname(sys.executable)
    shopyo_cmd = os.path.join(bin_dir, "shopyo")
    subprocess.run([shopyo_cmd, "initialise"], check=True)


@cli.command("seed")
def seed():
    """Seed the database with default data"""
    bin_dir = os.path.dirname(sys.executable)
    flask_cmd = os.path.join(bin_dir, "flask")
    subprocess.run([flask_cmd, "shopyo-seed"], check=True)


@cli.command("run")
@click.option("--debug", is_flag=True, default=True)
def run(debug):
    """Run the development server"""
    bin_dir = os.path.dirname(sys.executable)
    flask_cmd = os.path.join(bin_dir, "flask")
    args = [flask_cmd]
    if debug:
        args.append("--debug")
    args.append("run")
    subprocess.run(args, check=True)


@cli.command("deploy")
def deploy():
    """Generate production deployment files"""
    
    dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=pythoncms.app:create_app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pythoncms.app:create_app('production')"]
"""

    dockerignore_content = """__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.DS_Store
"""

    docker_compose_content = """version: '3.8'

services:
  web:
    build: .
    command: gunicorn --bind 0.0.0.0:8000 "pythoncms.app:create_app('production')"
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      - FLASK_ENV=production
"""

    trymkfile("Dockerfile", dockerfile_content)
    trymkfile(".dockerignore", dockerignore_content)
    trymkfile("docker-compose.yml", docker_compose_content)
    
    click.echo("🚀 Deployment files generated!")
    click.echo("Run 'docker-compose up --build' to test locally.")
    click.echo("Or deploy the Dockerfile to any cloud provider (Fly.io, Railway, etc).")
