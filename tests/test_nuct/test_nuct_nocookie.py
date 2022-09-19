from nuctpy import NUCT


def test_no_cache():
    ct = NUCT(use_old_cookie=False)
    print(ct.site_data)
    assert len(ct.site_data) > 0, "サイトデータが取得できていない"


def test_yes_cache():
    ct = NUCT(use_old_cookie=True)
    assert len(ct.site_data) > 0, "サイトデータが取得できていない"
