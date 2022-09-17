from NUCT import Quiz


def test_quiz_context():
    q = Quiz()
    assert type(q.context("")) == list, "リクエストの送信がうまくいっていない"
