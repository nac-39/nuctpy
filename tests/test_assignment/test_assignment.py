from NUCT import Assignment


def test_assignment_site():
    a = Assignment()
    assert type(a.site("2022_1001025")) == list


def test_assignment_my():
    a = Assignment()
    assert type(a.site("2022_1001025")) == list
