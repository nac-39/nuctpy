import click

import nuctpy

from .nuct import nuct


@click.option("--detail", "-d", default=False, is_flag=True, help="講義の説明を表示します")
@click.option("--site_id", "-i", default=False, is_flag=True, help="講義のsite_idを表示します")
@click.option("--year", "-y", default=None, help="講義の年度を指定します")
@nuct.command()
def site(detail, site_id, year):
    """授業の一覧を表示."""
    nuct = nuctpy.NUCT()
    _data = nuct.site_data  # 授業一覧のjsonを読み込む
    for d in _data:
        if year:
            if year in d["entityTitle"]:
                pass
            else:
                continue
        string = d["entityTitle"]
        if site_id:
            string += "\t" + d["entityId"]
        if detail:
            string += "\n\t" + d["description"]
        click.echo(string)
