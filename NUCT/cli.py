import click
import NUCT

@click.group()
def nuct():
    pass

@click.option("--all", "-a", default=False, is_flag=True, help="全ての講義を表示します")
@click.option("--detail", "-d", default=False, is_flag=True, help="講義の説明を表示します")
@click.option("--id", "-i", default=False, is_flag=True, help="講義のsiteidを表示します")
@click.option("--year", "-y", default=None, help="講義の年度を指定します")
@nuct.command()
def site(all, detail, id, year):
    nuct = NUCT.NUCT()
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


@click.option("--grep", "-g", default="", help="リソースの名前の一部を指定します")
@click.option("--download", "-d", default=False, is_flag=True, help="コンテンツを全てダウンロードします")
@click.option("--link", "-l", default=False, is_flag=True, help="URLを表示します")
@click.argument("siteid")
@nuct.command()
def content(siteid, link, download, grep):
    c = NUCT.Content()    
    data = c.site(siteid)
    for d in data:
        dl = False
        if download:
            if (grep in d["title"]) and (not d["url"].split("/")[-1] == ""):
                c.load_contents([d["url"]])
                dl = True
        click.echo("💾: "*dl + d["entityTitle"] + ("\t" + d["url"])*link)


@nuct.command()
def assignment():
    a = NUCT.Assignment()
    data = a.my()
    for d in data:
        click.echo(a.site_id_title[d["context"]] + "\t" + d["entityTitle"])