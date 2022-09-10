from NUCT import Assignment


def test_assignment_site():
    a = Assignment()
    # 物質情報学1
    assert a.site("2022_1002030")[0]["title"] == "課題5（2022年7月11日出題）"
    # 微積分学の発展
    assert a.site("2022_1001030")[0]["title"] == "第5回課題"
    
def test_assignment_my():
    a = Assignment()
    assert a.my()[0]["title"] == "第5回課題"

