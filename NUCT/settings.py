import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = Path().cwd().parent / ".env"
load_dotenv(dotenv_path)

MFA_CAS_URL = "https://auth-mfa.nagoya-u.ac.jp/cas/login?service=https%3A%2F%2Fct.nagoya-u.ac.jp%2Fsakai-login-tool%2Fcontainer"
NUCT_ROOT = "https://ct.nagoya-u.ac.jp/"
MEIDAI_ID = os.environ.get("MEIDAI_ID")
MEIDAI_PWD = os.environ.get("MEIDAI_PWD")
SEED = os.environ.get("SEED")
