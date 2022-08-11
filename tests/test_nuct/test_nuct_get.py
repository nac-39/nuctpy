from NUCT import NUCT

ct = NUCT()

assert ct.get("ht://example.com"), "dame"
assert ct.get("https://ct.nagoya-u.ac.jp/portal"), "false"