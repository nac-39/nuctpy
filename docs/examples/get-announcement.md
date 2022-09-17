# nuctpy.Announcement()を使ってお知らせの一覧を取得する。

次のコードの`<site_id>`を自分が受講している講義のサイトIDに置き換えて実行してみてください。

!!! note
    サイトIDはNUCTで授業のページを見ている時のURLの`<site_id>`の部分です。
    ```url
    https://ct.nagoya-u.ac.jp/portal/site/<site_id>/tool/xxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

```python
import nuct

announcement = nuct.Announcement()

SITE_ID = "<site_id>"
print(announcement.site(SITE_ID)) #講義のサイトごと
print(announcement.user()) # ユーザーのお知らせ全て？
print(announcement.motd()) # 今日のお知らせ全て？
```

出力の例は次のようになります。

```python
[
    {
        "announcementId": "hogehoge",
        "attachments": [],
        "body": '<p>html形式のテキスト</p>',
        "channel": "main",
        "createdByDisplayName": "MYOUJI Namae 苗字 名前",
        "createdOn": 1658463007773,
        "id": "<site_id>:hogehoge",
        "siteId": "<site_id>",
        "siteTitle": "講義名(2022年度春２/月４)",
        "title": "タイトル",
        "entityReference": "/announcement/<site_id>:main:hogehoge",
        "entityURL": "https://ct.nagoya-u.ac.jp/direct/announcement/<site_id>:main:hogehoge",
        "entityId": "<site_id>:main:hogehoge",
        "entityTitle": "タイトル",
    },
以下略
```
