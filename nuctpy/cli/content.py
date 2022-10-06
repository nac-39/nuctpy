import click

import nuctpy
from nuctpy.content import HOME_DIR

from .nuct import nuct


@click.option(
    "--out",
    "-o",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    default=None,
    help="ファイルの保存先ディレクトリを指定します",
)
@click.option("--grep", "-g", multiple=True, default=[], help="リソースの名前の一部を指定します")
@click.option("--download", "-d", default=False, is_flag=True, help="コンテンツを全てダウンロードします")
@click.option("--link", "-l", default=False, is_flag=True, help="URLを表示します")
@click.argument("siteid")
@nuct.command()
def content(siteid, link, download, grep, out):
    """ある授業のリソースの一覧を表示."""
    c = nuctpy.Content()
    data = c.site(siteid)
    dir_t = "├──"
    dir_stick = "│  "
    dir_end = "└──"
    # downloadオプションがないのにgrep, outがあっても無駄なので警告する。
    if (not download) and (len(grep) or out):
        click.echo(
            click.style(
                "Warning: --grep " * bool(grep)
                + "--out" * bool(out)
                + "が設定されていますが、"
                + "--downloadオプションが設定されていません",
                fg="yellow",
            )
        )

    click.echo(".")
    # siteidのサイトのリソースを表示。

    def tree_print(data):
        if len(data) == 0:
            return
        d = data[0]
        is_downloaded = False
        contains_any_of_words_in_grep = any(g in d["title"] for g in grep)
        is_directory = d["type"] == "collection"
        dir_count = len(d["container"].split("/")) - 4
        try:
            if is_directory:
                d_is_last = False
            elif len(data) == 1:
                d_is_last = True
            else:
                d_is_last = not bool(data[0]["container"] == data[1]["container"])
        except IndexError:
            d_is_last = True

        # ダウンロードする
        if download and (
            ((not grep) or (grep and contains_any_of_words_in_grep))
            and (not is_directory)
        ):
            c.load_contents(d["url"], save_path=out if out else HOME_DIR)
            is_downloaded = True

        dir_tree = str(dir_stick * dir_count + (dir_end if d_is_last else dir_t))
        click.echo(
            # ディレクトリのツリー
            dir_tree
            + str(
                # ダウンロードした場合に表示
                "💾: " * is_downloaded + click.style(d["title"], fg="yellow")
                if is_downloaded
                # ダウンロードしなかった場合に表示
                else click.style(d["title"], fg="white") +
                # linkオプションがある場合に表示
                click.style("\t" + d["url"], fg="bright_black") * link
            )
        )

        tree_print(data[1:])

    tree_print(data)
