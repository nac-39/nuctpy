# nuctpy.Quiz()を使って小テストの一覧を取得する。

次のコードの`<site_id>`を自分が受講している講義のサイトIDに置き換えて実行してみてください。

!!! note
    サイトIDはNUCTで授業のページを見ている時のURLの`<site_id>`の部分です。
    ```url
    https://ct.nagoya-u.ac.jp/portal/site/<site_id>/tool/xxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

```python
import nuctpy

quiz = nuctpy.Quiz()

SITE_ID = "<site_id>"
print(quiz.context(SITE_ID))

```
