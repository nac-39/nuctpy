import nuctpy


def test_lecture():
    ct = nuctpy.NUCT(use_old_cookie=False)

    print(nuctpy.get_lectures(ct))
