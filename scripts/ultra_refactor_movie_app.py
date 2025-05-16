import os
import shutil

ROOT_DIR = os.path.abspath(".")
APP_DIR = os.path.join(ROOT_DIR, "app")
GUI_DIR = os.path.join(APP_DIR, "gui")
DATA_DIR = os.path.join(ROOT_DIR, "data")
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
TESTS_DIR = os.path.join(ROOT_DIR, "tests")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")

# 必要なフォルダを作成
def create_structure():
    print("📦 ディレクトリ作成")
    for d in [APP_DIR, GUI_DIR, DATA_DIR, SCRIPTS_DIR, TESTS_DIR, DOCS_DIR]:
        os.makedirs(d, exist_ok=True)

    # __init__.py も自動で入れる（パッケージ化）
    for d in [APP_DIR, GUI_DIR, TESTS_DIR]:
        init_file = os.path.join(d, "__init__.py")
        if not os.path.exists(init_file):
            open(init_file, "w").close()

# データファイル判定
def is_data_file(file):
    return file.endswith((".db", ".csv", ".json"))

# ファイル分類ルール（超シンプルルール）
def classify(file):
    if is_data_file(file):
        return DATA_DIR
    elif "streamlit" in file or "dash" in file:
        return GUI_DIR
    elif "test" in file or "check" in file:
        return TESTS_DIR
    elif "README" in file:
        return ROOT_DIR
    elif "config" in file:
        return APP_DIR
    elif file.endswith(".py"):
        return APP_DIR
    else:
        return SCRIPTS_DIR

def safe_move(src, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, os.path.basename(src))
    print(f"🔄 移動: {src} -> {dst}")
    shutil.move(src, dst)

def execute_ultra_refactor():
    create_structure()

    for file in os.listdir(ROOT_DIR):
        if os.path.isfile(file) and not file.startswith("ultra_refactor"):
            target_dir = classify(file)
            safe_move(file, target_dir)

    # __pycache__ も掃除
    pycache = os.path.join(ROOT_DIR, "__pycache__")
    if os.path.exists(pycache):
        shutil.rmtree(pycache)
        print("🧹 __pycache__ を削除")

    # 最強 .gitignore も追加
    gitignore = os.path.join(ROOT_DIR, ".gitignore")
    if not os.path.exists(gitignore):
        with open(gitignore, "w") as f:
            f.write("__pycache__/\n*.db\n*.csv\n.env\n")
        print("✅ .gitignore 作成")

    # requirements.txt もひな形作成
    req = os.path.join(ROOT_DIR, "requirements.txt")
    if not os.path.exists(req):
        with open(req, "w") as f:
            f.write("streamlit\ndash\nrequests\npandas\nplotly\n")
        print("✅ requirements.txt 作成")

    print("\n🎉 Ultraリファクタ完了！ importは自分で確認しよう")

if __name__ == "__main__":
    execute_ultra_refactor()

