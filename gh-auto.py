#! /usr/bin/env python3
"""
Author: Jef van der Avoirt

Script that automates the process of creating a new GitHub repository.
"""


import os
from time import sleep
import requests
from pprint import pprint
import argparse
from pathlib import Path

from secrets import ACCESS_TOKEN


BASE_URI = "https://api.github.com"


parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="command")
create_parser = subparser.add_parser("create")

create_parser.add_argument("--name", "-n", help="Name of the repository", required=True, type=str, dest="name")
create_parser.add_argument("--private", "-p", help="Make the repository private", action="store_true", dest="is_private")
create_parser.add_argument("--init", "-i", help="Initialize the repository with a README.md", action="store_true", dest="needs_init")
create_parser.add_argument("--ignore", "-ign", help="Choose language for .gitignore template", type=str, dest="ignore_template")

args = parser.parse_args()


def main():
    match args.command:
        case "create":
            create_repo()
        case _:
            print("No command specified")


def create_repo():
    # Create a new repository on GitHub
    payload = {
        "name": args.name,
        "private": str(args.is_private).lower(),
        "auto_init": str(args.needs_init).lower(),
        "gitignore_template": args.ignore_template.lower().capitalize()
    }
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    print("Creating repository...")
    result = requests.post(f"{BASE_URI}/user/repos", json=payload, headers=headers)

    result.callback = clone_repo(result)


def clone_repo(result):
    print("Repository created! Cloning...")

    # Clone repository locally
    try:
        os.chdir(f"{Path.home()}/Projects")
    except FileNotFoundError:
        os.mkdir(f"{Path.home()}/Projects")
        os.chdir(f"{Path.home()}/Projects")

    os.system(f"git clone {result.json()['ssh_url']}")  
    os.chdir(f"{Path.home()}/Projects/{args.name}")
    os.system("gnome-terminal")  


if __name__ == "__main__":
    main()
