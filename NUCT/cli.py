import click
import datetime
import NUCT


@click.group()
def nuct():
    pass


@click.option("--detail", "-d", default=False, is_flag=True, help="講義の説明を表示します")
@click.option("--id", "-i", default=False, is_flag=True, help="講義のsiteidを表示します")
@click.option("--year", "-y", default=None, help="講義の年度を指定します")
@nuct.command()
def site(detail, id, year):
    nuct = NUCT.NUCT()
    _data = nuct.site_data # 授業一覧のjsonを読み込む
    for d in _data:
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


@click.option("--out", "-o", type=click.Path(exists=True,  dir_okay=True, file_okay=False), default=None, help="ファイルの保存先ディレクトリを指定します")
@click.option("--grep", "-g", multiple=True, default=[""], help="リソースの名前の一部を指定します")
@click.option("--download", "-d", default=False, is_flag=True, help="コンテンツを全てダウンロードします")
@click.option("--link", "-l", default=False, is_flag=True, help="URLを表示します")
@click.argument("siteid")
@nuct.command()
def content(siteid, link, download, grep, out):
    c = NUCT.Content()
    data = c.site(siteid)
    
    # downloadオプションがないのにgrep, outがあっても無駄なので警告する。
    if (not download) and (grep or out):
        click.echo(click.style("Warning: --grep "*bool(grep)+"--out"*bool(out)+"が設定されていますが、"+
                               "--downloadオプションが設定されていません", fg="yellow"))
    
    # siteidのサイトのリソースを表示。
    # ダウンロードしたものはアイコン＋黄色で表示する。
    for d in data:
        is_downloaded = False
        if download:
            contains_any_of_words_in_grep = any(g in d["title"] for g in grep)
            is_directory = d["url"].split("/")[-1] == ""
            
            if contains_any_of_words_in_grep and not is_directory:
                c.load_contents([d["url"]], save_path=out if out else "")
                is_downloaded = True
            
        click.echo( # ダウンロードした場合に表示
                    "💾: "*is_downloaded + click.style(d["entityTitle"], fg="yellow") if is_downloaded
                   # ダウンロードしなかった場合に表示
                   else click.style(d["entityTitle"], fg="white")
                   # linkオプションがある場合に表示
                   + click.style("\t" + d["url"], fg="bright_black")*link 
                   )


@nuct.command()
def assignment():
    a = NUCT.Assignment()
    data = a.my()
    for d in data:
        click.echo(a.site_id_title[d["context"]] + "\t" + d["entityTitle"])


@click.argument("siteid")
@nuct.command()
def quiz(siteid):
    q = NUCT.Quiz()
    data = q.context(siteid)
    echo_data = {}
    for d in data:
        echo_data.update({d["entityTitle"]:datetime.datetime.fromtimestamp(d["dueDate"]/1000)})
    echo_data = sorted(echo_data.items(), key=lambda x:x[1])
    
    click.secho(q.site_id_title[data[0]["ownerSiteId"]], bold=True)
    for d in echo_data:
        if d[1] - datetime.timedelta(days=3) < datetime.datetime.now():
            fg = "red"
        elif d[1] - datetime.timedelta(days=7) < datetime.datetime.now():
            fg = "yellow"
        else:
            fg = "green"
        date = datetime.datetime.fromisoformat(str(d[1])).strftime("%Y-%m-%d %H:%M")
        click.echo(click.style(date, fg=fg) + "\t" + d[0])
        
        