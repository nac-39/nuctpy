if __name__ == "__main__":
    from .assignment import Assignment
    from .content import Content
    # a = Assignment()
    # または sessionオブジェクトを作って使い回す
    # ContentクラスもAssignmentクラスも使う場合は使い回すの推奨
    session = Assignment.create_session()
    a = Assignment(session)
    c = Content(session)
    print(a.site_data)
    print(a.site("2022_1002030"))
    # ↓エンドポイントが404になってしまう
    #print(a.item("a7edf711-0c4a-4749-829d-efe55a7a56ad"))
    print(c.site("2022_1002030"))
    print(a.my())
    