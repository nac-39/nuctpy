# nuctpy.Content()を利用してリソースを取得する

`nuctpy.Content()`を使うことで、ある授業のリソースの一覧を取得することができます。

次のコードの`<site_id>`を自分が受講している講義のサイトIDに置き換えて実行してみてください。

!!! note
    サイトIDはNUCTで授業のページを見ている時のURLの`<site_id>`の部分です。
    ```url
    https://ct.nagoya-u.ac.jp/portal/site/<site_id>/tool/xxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

```python
import nuctpy

content = nuctpy.Content()

SITE_ID = "<site_id>"
resources_list = content.site(SITE_ID)

print(resources_list)
```

次のような実行結果が得られると思います。（下のテキストは一部加工してあります。）

??? 実行結果
    ```python
    [
        {
            'author': '教務連携',
            'authorId': 'hogehoge', # 多分UUID
            'container': '/content/group/',
            'copyrightAlert': None,
            'description': None,
            'endDate': None,
            'fromDate': None,
            'modifiedDate': '20220311163313642',
            'numChildren': 20,
            'quota': None,
            'size': 20,
            'title': '授業名(2022年度春/木２)',
            'type': 'collection',
            'url': 'https://ct.nagoya-u.ac.jp/access/content/group/<site_id>/',
            'usage': '<8けた数字>',
            'webLinkUrl': None,
            'hidden': False,
            'visible': True,
            'entityReference': '/content',
            'entityURL': 'https://ct.nagoya-u.ac.jp/direct/content',
            'entityTitle': '授業名(2022年度春/木２)'
        }, {
            'author': 'Hoge Fuga 保下 普我',
            'authorId': 'hogehoge',
            'container': '/content/group/<site_id>/',
            'copyrightAlert': None,
            'description': None,
            'endDate': None,
            'fromDate': None,
            'modifiedDate': '20220728034830976',
            'numChildren': 0,
            'quota': None,
            'size': 626160,
            'title': 'hogehoge.pdf',
            'type': 'application/pdf',
            'url': 'https://ct.nagoya-u.ac.jp/access/content/group/<site_id>/hogehoge.pdf',
            'usage': None,
            'webLinkUrl': None,
            'hidden': False,
            'visible': True,
            'entityReference': '/content',
            'entityURL': 'https://ct.nagoya-u.ac.jp/direct/content',
            'entityTitle': 'hogehoge.pdf'
        },
    以下略
    ```

この実行結果の`url`がリソースのURLになっています。

このURLにアクセスすればリソースをダウンロードできるのですが、その際にCAS認証にログインした状態でないと弾かれてしまいます。そこで、`NUCT.Content().load_contents(url)`を利用します。

この関数は認証済みのセッションオブジェクトを用いてGETリクエストを送るため、弾かれることなくリソースを取得することができます。

```python
for resource in resources_list:
    print("title: ", resource["title"])
    print("download url: ", resource["url"])
    content.load_contents(resource["url"])
```

デフォルトではデスクトップに保存されますが、`save_path`を`content.load_contents(url, save_path="~/Downloads")`のように設定することで別のディレクトリにも保存することができます。`save_path`のディレクトリは存在していないとエラーになります。

---

また、リソース一括ダウンロードには次のショートハンドが存在します。

```python
url_list = content.collect_url(SITE_ID)

for url in url_list:
    content.load_contents(url)
```
