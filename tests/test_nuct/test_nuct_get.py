import pytest

from NUCT import NUCT

ct = NUCT()


def test_scheme():
    with pytest.raises(Exception) as e:
        _ = ct.get("file://portal.nagoya-u.ac.jp")
    assert (
        str(e.value)
        == "No connection adapters were found for 'file://portal.nagoya-u.ac.jp'"
    )


def test_domain():
    with pytest.raises(ValueError) as e:
        _ = ct.get("https://example.ac.jp")
    assert str(e.value) == "example.ac.jpは許可されていません．", "名大以外のドメインはダメだよ"

    with pytest.raises(ValueError) as e:
        _ = ct.get("https://hogehoge.example.ac.jp")
    assert str(e.value) == "hogehoge.example.ac.jpは許可されていません．", "名大以外のドメインはダメだよ"


def test_normal_use():
    assert not ct.get("https://ct.nagoya-u.ac.jp/portal") is False, "これはresが帰ってこないとおかしい"
    assert ct.get("https://ct.nagoya-u.ac.jp/portal"), "レスポンスが帰ってきてないよ"
