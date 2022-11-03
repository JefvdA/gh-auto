#! /usr/bin/env python3
"""
Author: Jef van der Avoirt

Script that automates the process of managing your github repo.

Better then 'gh' because this script also automates the process managing the local repo.
"""


import typer

import commands.repo


app = typer.Typer()
app.add_typer(commands.repo.app, name="repo")


if __name__ == "__main__":
    app()