# [WIP] nuctpy

名古屋大学の LMS である NUCT の API のラッパーです．

完全な API のラッパーというわけではなく，使えそうなエンドポイントのみに対応します．また，あると便利なショートカット（例：ある授業のリソースを全てダウンロードする）も追加します。

## ドキュメント

[https://nac-39.github.io/nuctpy/](https://nac-39.github.io/nuctpy/)

## 注意！

このプログラムには名大 ID, パスワード, 多要素認証のシード値を読み取って，それをインターネット上に流すプログラムが含まれています．プログラムの安全性は全くの無保証です．自分でコードを見て安全だと判断できる人が安全な方法でプログラムを使うようにしてください．
万が一，パスワードやシード値を安全ではない方法で使ってしまった場合，直ちにそれらを破棄し新しいものに変えてください．

## Quick Start

```bash
# pip
$ pip install git+https://github.com/nac-39/nuctpy.git#main

# or poetry
$ poetry add git+https://github.com/nac-39/nuctpy.git#main

# .envファイルにIDとパスワード，シード値を登録する
$ cat << EOF > .env
MEIDAI_ID=
MEIDAI_PWD=
SEED=
EOF

# [wip] コマンドラインでnuctpyを使う
$ nuct
$ nuct --help
```
