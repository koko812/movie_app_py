import os
import shutil

# プロジェクトのルート（ここに合わせて使う）
ROOT_DIR = os.path.abspath(".")
APP_DIR = os.path.join(ROOT_DIR, "app")
GUI_DIR = os.path.join(APP_DIR, "gui")
DATA_DIR = os.path.join(ROOT_DIR, "data")
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
TESTS_DIR = os.path.join(ROOT_DIR, "tests")

# ファイル分類辞書
file_map = {
    "db.py": os.path.join(APP_DIR, "db_utils.py"),
    "insert_movies.py": os.path.join(SCRIPTS_DIR, "insert_movies_once.py"),
    "insert_genres.py": os.path.join(SCRIPTS_DIR, "insert_genres_once.py"),
    "sample.py": os.path.join(SCRIPTS_DIR, "sample_test.py"),
    "fetch_movies.py": os.path.join(APP_DIR, "data_loader.py"),
    "movie_utils.py": os.path.join(APP_DIR, "analysis_tools.py"),
    "gui.py": os.path.join(APP_DIR, "gui", "old_gui.py"),
    "streamlit_app.py": os.path.join(APP_DIR, "gui", "streamlit_app.py"),
    "dash_app.py": os.path.join(APP_DIR, "gui", "dash_app.py")
}

def safe_move(src, dst):
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        print(f"🔄 移動: {src} -> {dst}")
        shutil.move(src, dst)
    else:
        print(f"⚠️ 見つからない: {src}")

def create_basic_structure():
    print("📦 基本ディレクトリ作成")
    for d in [APP_DIR, GUI_DIR, DATA_DIR, SCRIPTS_DIR, TESTS_DIR]:
        os.makedirs(d, exist_ok=True)

def execute_refactor():
    create_basic_structure()
    for src, dst in file_map.items():
        safe_move(src, dst)

    # パスチェック用 config.py も自動生成（なければ）
    config_path = os.path.join(APP_DIR, "config.py")
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            f.write(
                "import os\n"
                "BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n"
                "DB_PATH = os.path.join(BASE_DIR, 'data', 'movies.db')\n"
            )
        print(f"✅ config.py を作成: {config_path}")
    else:
        print(f"✅ config.py は既に存在")

if __name__ == "__main__":
    execute_refactor()
    print("\n🎉 リファクタ完了！必要なら import 書き換えを手動で確認してね")

