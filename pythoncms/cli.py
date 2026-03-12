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
import shutil
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
    # Bulletproof path resolution
    try:
        dest = os.path.abspath(name)
    except FileNotFoundError:
        # Fallback for deleted CWD
        base_dir = os.environ.get("PWD") or os.getcwd()
        dest = os.path.join(base_dir, name)
    
    click.echo(f"📂  Creating project at: {dest}")

    if os.path.exists(dest):
        click.echo(f"❌ Error: Directory already exists at {dest}")
        return

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    # Copy the project structure
    source_dir = str(path.parent.absolute())
    try:
        shutil.copytree(source_dir, dest, ignore=shutil.ignore_patterns('__pycache__', 'cli.py', '*.db', 'instance'))
        click.echo(f"✅ Scaffolding complete in {dest}")
    except Exception as e:
        click.echo(f"❌ Error during scaffolding: {e}")
        return
    
    # Create requirements.txt
    reqs = f"pythoncms=={__version__}"
    trymkfile(os.path.join(dest, "requirements.txt"), reqs)
    
    # Setup .env
    env_real = os.path.join(dest, ".env")
    
    env_content = f"""ACTIVE_FRONT_THEME = 'editorial'
ACTIVE_BACK_THEME = 'sneat'
APP_NAME = 'PythonCMS'
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
@click.option("--port", default=5000, help="Port to run the server on")
@click.option("--host", default="127.0.0.1", help="Host to bind to")
def run(debug, port, host):
    """Run the development server"""
    bin_dir = os.path.dirname(sys.executable)
    flask_cmd = os.path.join(bin_dir, "flask")
    args = [flask_cmd]
    if debug:
        args.append("--debug")
    args.extend(["run", "--port", str(port), "--host", host])
    subprocess.run(args, check=True)


@cli.command("deploy")
def deploy():
    """Generate production deployment files (Docker + Nginx)"""
    
    dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=pythoncms.app:create_app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

# Ensure static files are collected if needed
# RUN flask shopyo-collectstatic

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "pythoncms.app:create_app('production')"]
"""

    nginx_content = """# Hardened Nginx Config for PythonCMS
server {
    listen 80;
    server_name localhost; # Replace with your domain

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options "nosniff";
    add_header Referrer-Policy "no-referrer-when-downgrade";
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline';";

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml;
    gzip_disable "MSIE [1-6]\\.";

    # Max upload size
    client_max_body_size 20M;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Proxy timeouts
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }

    location /static/ {
        alias /app/pythoncms/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
"""

    docker_compose_content = """version: '3.8'

services:
  web:
    build: .
    volumes:
      - .:/app
      - static_volume:/app/pythoncms/static
    env_file:
      - .env
    environment:
      - FLASK_ENV=production

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - static_volume:/app/pythoncms/static:ro
    depends_on:
      - web

volumes:
  static_volume:
"""

    trymkfile("Dockerfile", dockerfile_content)
    trymkfile("nginx.conf", nginx_content)
    trymkfile("docker-compose.yml", docker_compose_content)
    trymkfile(".dockerignore", "__pycache__\\n*.pyc\\n.env\\nvenv/\\ninstance/\\n")
    
    click.echo("🚀 Production deployment files generated!")
    click.echo("Included: Dockerfile, nginx.conf, docker-compose.yml")
    click.echo("")
    click.echo("To deploy:")
    click.echo("1. Edit 'nginx.conf' to set your real domain name.")
    click.echo("2. Run 'docker-compose up --build -d'")
