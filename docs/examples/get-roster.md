# nuctpy.Roster()を使って受講者の一覧を取得する。

次のコードの`<site_id>`を自分が受講している講義のサイトIDに置き換えて実行してみてください。

!!! note
    サイトIDはNUCTで授業のページを見ている時のURLの`<site_id>`の部分です。
    ```url
    https://ct.nagoya-u.ac.jp/portal/site/<site_id>/tool/xxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

```python
import nuctpy

roster = nuctpy.Roster()

SITE_ID = "<site_id>"
print(roster.site(SITE_ID))


```

実行結果の例

```python
 [{
    'displayName': 'MEIDAI Taro 名大 太郎', 
    'imageUrl': 'https://ct.nagoya-u.ac.jp/direct/profile/hogehoge/image/', 
    'entityReference': '/roster', 
    'entityURL': 'https://ct.nagoya-u.ac.jp/direct/roster'
},
以下略
```
