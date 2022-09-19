import click

import nuctpy

from .nuct import nuct


@nuct.command()
def assignment():
    """課題の一覧を表示."""
    a = nuctpy.Assignment()
    data = a.my()
    for d in data:
        click.echo(a.site_id_title[d["context"]] + "\t" + d["entityTitle"])
