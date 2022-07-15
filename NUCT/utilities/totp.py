# https://qiita.com/nardtree/items/f81a75bb603f88ee0b1b
# こちらの記事のを使わせていただきました


import hmac, base64, struct, hashlib, time

def get_hotp_token(secret: str, intervals_no: int) -> str:
    # まずシークレットキーをデコード
    key = base64.b32decode(secret, True)
    # PythonのデータをCの構造体に変換
    msg = struct.pack(">Q", intervals_no)
    # ハッシュ値を計算
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return str(h)

def get_totp_token(secret):
    # unix時間を30で割った整数をいれている
    x = get_hotp_token(secret=secret, intervals_no=int(time.time())//30)
    # 6桁に満たない場合は6桁になるまでパディング
    while len(x)!=6:
        x+='0'
    return x