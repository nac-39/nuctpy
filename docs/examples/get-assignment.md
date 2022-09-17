# nuctpy.Assignment()を使って課題を取得する

次のコードの`<site_id>`を自分が受講している講義のサイトIDに置き換えて実行してみてください。

!!! note
    サイトIDはNUCTで授業のページを見ている時のURLの`<site_id>`の部分です。
    ```url
    https://ct.nagoya-u.ac.jp/portal/site/<site_id>/tool/xxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

```python
import nuctpy

assignment = nuctpy.Assignment()

SITE_ID = "<site_id>"
print(assignment.site(SITE_ID))
print(assignment.my())
```

??? info "出力の例"
    ```python
    [
        {
            'access': 'SITE', 
            'allPurposeItemText': None, 
            'attachments': [], 
            'author': 'hogehoge', 
            'authorLastModified': None, 
            'closeTime': {
                'epochSecond': 1665500100, 
                'nano': 0
            }, 
            'closeTimeString': '2022-10-11T14:55:00Z', 
            'content': None, 
            'context': 'hogehoge', 
            'creator': None, 
            'dropDeadTime': {
                'epochSecond': 1665500100, 
                'nano': 0
            }, 
            'dropDeadTimeString': '2022-10-11T14:55:00Z', 
            'dueTime': {
                'epochSecond': 1665500100, 
                'nano': 0
            }, 
            'dueTimeString': '2022-10-11T14:55:00Z', 
            'gradeScale': 'UNGRADED_GRADE_TYPE', 
            'gradeScaleMaxPoints': None, 
            'gradebookItemId': None, 
            'gradebookItemName': None, 
            'groups': [], 
            'id': 'hogehoge', 
            'instructions': '<p>ほげほげ</p>', 
            'modelAnswerText': None, 
            'openTime': {
                'epochSecond': 1662450000, 
                'nano': 0
            }, 
            'openTimeString': '2022-09-06T07:40:00Z', 
            'position': 0, 
            'privateNoteText': None, 
            'section': '', 
            'status': 'OPEN', 
            'submissionType': 'ATTACHMENT_ONLY_ASSIGNMENT_SUBMISSION', 
            'timeCreated': {
                'epochSecond': 1662442420, 
                'nano': 0
            }, 
            'timeLastModified': {
                'epochSecond': 1662449690, 
                'nano': 0
            }, 
            'title': 'タイトルほげほげ', 
            'allowResubmission': True, 
            'draft': False, 
            'entityReference': '/assignment/hogehoge', 
            'entityURL': 'https://ct.nagoya-u.ac.jp/direct/assignment/hogehoge', 
            'entityId': 'hogehoge', 
            'entityTitle': 'タイトルほげほげ'
        }
    ]
    ```

また、`nuctpy.Assignment().my()`を用いて、提出前の課題の一覧（？）を取得することができます。

```python
import nuctpy

assignment = nuctpy.Assignment()

print(assignment.my())
```
