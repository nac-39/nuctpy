import click
import datetime
from .nuct import NUCT

@click.option("--all", "-a", default=False, is_flag=True)
@click.option("--detail", "-d", default=False, is_flag=True)
@click.option("--id", "-i", default=False, is_flag=True)
@click.option("--year", "-y", default=None)
@click.command()
def nuct(all, detail, id, year):
    nuct = NUCT()
    _data = nuct.site_data
    if all:
        num = len(_data)
    else:
        num = 5
    for d in _data[0:num]:
        if year:
            if year in d["entityTitle"]:
                pass
            else:
                continue
        string = d["entityTitle"]
        if id:
            string += "\t" + d["entityId"]
        if detail:
            string += "\n\t" + d["description"]
        click.echo(string)
