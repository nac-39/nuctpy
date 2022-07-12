from NUCT import Assignment

def test_assignment_site():
    a = Assignment()
    a.my()
    assert type(a.site("2022_1002030")) is list
    a.site("hgoehoge")
    a.item("")