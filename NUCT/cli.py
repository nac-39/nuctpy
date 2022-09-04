import click
import json
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
    _data = nuct.site_data  # 授業一覧のjsonを読み込む
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


@click.option("--out", "-o", type=click.Path(exists=True, dir_okay=True, file_okay=False), default=None, help="ファイルの保存先ディレクトリを指定します")
@click.option("--grep", "-g", multiple=True, default=[], help="リソースの名前の一部を指定します")
@click.option("--download", "-d", default=False, is_flag=True, help="コンテンツを全てダウンロードします")
@click.option("--link", "-l", default=False, is_flag=True, help="URLを表示します")
@click.argument("siteid")
@nuct.command()
def content(siteid, link, download, grep, out):
    c = NUCT.Content()
    data = c.site(siteid)
    dir_t = "├──"
    dir_stick = "│  "
    dir_end = "└──"
    # downloadオプションがないのにgrep, outがあっても無駄なので警告する。
    if (not download) and (len(grep) or out):
        click.echo(click.style("Warning: --grep " * bool(grep) + "--out" * bool(out) + "が設定されていますが、" +
                               "--downloadオプションが設定されていません", fg="yellow"))

    click.echo(".")
    # siteidのサイトのリソースを表示。
    # ダウンロードしたものはアイコン＋黄色で表示する。
    def treePrint(data):
        if len(data) == 0:
            return
        d = data[0]
        is_downloaded = False
        contains_any_of_words_in_grep = any(g in d["title"] for g in grep) or any(g in d[""])
        is_directory = d["type"] == "collection"
        dir_count = len(d["container"].split("/")) - 4
        try:
            if is_directory:
                d_is_last = False
            elif len(data)==1:
                d_is_last = True
            else:
                d_is_last = not bool(data[0]["container"] == data[1]["container"])
        except IndexError:
            d_is_last = True

        # ダウンロードする
        if download and (contains_any_of_words_in_grep and not is_directory):
            c.load_contents([d["url"]], save_path=out if out else "")
            is_downloaded = True

        dir_tree = str(dir_stick * dir_count + (dir_end if d_is_last else dir_t))
        click.echo(
            # ディレクトリのツリー
            dir_tree +
            str(
                # ダウンロードした場合に表示
                "💾: " * is_downloaded + click.style(d["title"], fg="yellow") if is_downloaded
                # ダウンロードしなかった場合に表示
                else click.style(d["title"], fg="white")
                # linkオプションがある場合に表示
                + click.style("\t" + d["url"], fg="bright_black") * link
            )
        )
        
        treePrint(data[1:])

    treePrint(data)


@nuct.command()
def assignment():
    a = NUCT.Assignment()
    data = a.my()
    for d in data:
        click.echo(a.site_id_title[d["context"]] + "\t" + d["entityTitle"])
