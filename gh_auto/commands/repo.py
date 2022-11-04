import os
import typer
import requests
from pathlib import Path

import gh_auto.helpers.authentication as authentication

BASE_URI = "https://api.github.com"

app = typer.Typer()


@app.command()
def create(
    name: str = typer.Argument(..., help="Name of the repository"),
    is_private: bool = typer.Option(False, "--private", "-p", help="Make the repository private"),
    needs_init: bool = typer.Option(False, "--init", "-i", help="Initialize the repository with a README.md"),
    ignore_template: str = typer.Option("", "--ignore", "-ign", help="Choose language for .gitignore template"),
):
    """Command to create a new repository on GitHub, and clone it locally"""

    # Create a new repository on GitHub
    payload = {
        "name": name,
        "private": str(is_private).lower(),
        "auto_init": str(needs_init).lower(),
        "gitignore_template": ignore_template.lower().capitalize()
    }
    headers = {
        "Authorization": f"token {authentication.get_token()}",
        "Accept": "application/vnd.github+json"
    }
    print("Creating repository...")
    result = requests.post(f"{BASE_URI}/user/repos", json=payload, headers=headers)

    # Clone repository locally
    print("Repository created! Cloning...")
    try:
        os.chdir(f"{Path.home()}/Projects")
    except FileNotFoundError:
        os.mkdir(f"{Path.home()}/Projects")
        os.chdir(f"{Path.home()}/Projects")

    os.system(f"git clone {result.json()['ssh_url']}")  
    os.chdir(f"{Path.home()}/Projects/{name}")
    os.system("gnome-terminal")