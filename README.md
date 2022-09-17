# [WIP]NUCT_api_wrapper

名古屋大学のLMSであるNUCTのAPIのラッパーです．

完全なAPIのラッパーというわけではなく，使えそうなエンドポイントのみに対応します．また，あると便利なショートカット（例：ある授業のリソースを全てダウンロードする）も追加します．

# 注意！

このプログラムには名大ID, パスワード, 多要素認証のシード値を読み取って，それをインターネット上に流すプログラムが含まれています．プログラムの安全性は全くの無保証です．自分でコードを見て安全だと判断できる人が安全な方法でプログラムを使うようにしてください．
万が一，パスワードやシード値を安全ではない方法で使ってしまった場合，直ちにそれらを破棄し新しいものに変えてください．

# 使い方
```bash
$ git clone git@github.com:nac-39/NUCT_api_wrapper.git
$ cd NUCT_api_wrapper

# 仮想環境を有効にする場合
$ python -m venv .venv
$ source .venv/bin/activate

# .envファイルにIDとパスワード，シード値を登録する
$ cat << EOF > .env
MEIDAI_ID=
MEIDAI_PWD=
SEED=
EOF

# 必要なパッケージをインストール
$ pip install -r ./nuctpy/requirements.txt

# NUCTパッケージをインストールする
$ pip install -e .

# [WIP]nuct-cliを使う
$ nuct-cli
$ nuct-cli --help
```
