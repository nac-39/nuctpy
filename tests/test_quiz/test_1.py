from NUCT import Quiz

def test_quiz_context():
    q = Quiz()
    assert q.context("2022_1001025")[0]["title"] == "20220706 課題"