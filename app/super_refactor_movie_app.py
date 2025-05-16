import os
import shutil

ROOT_DIR = os.path.abspath(".")
APP_DIR = os.path.join(ROOT_DIR, "app")
GUI_DIR = os.path.join(APP_DIR, "gui")
DATA_DIR = os.path.join(ROOT_DIR, "data")
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
TESTS_DIR = os.path.join(ROOT_DIR, "tests")

# ファイル名ベースで分類
mapping_rules = {
    "db": APP_DIR,
    "loader": APP_DIR,
    "analysis": APP_DIR,
    "streamlit": GUI_DIR,
    "dash": GUI_DIR,
    "cli": SCRIPTS_DIR,
    "choice": SCRIPTS_DIR,
    "poster": SCRIPTS_DIR,
    "insert": SCRIPTS_DIR,
    "fetch": SCRIPTS_DIR,
    "check": TESTS_DIR,
    "year_rate": SCRIPTS_DIR,
    "visualize": SCRIPTS_DIR,
    "get_movie": SCRIPTS_DIR,
    "interactive": SCRIPTS_DIR,
    "analyse": SCRIPTS_DIR,
    "count_db": SCRIPTS_DIR,
    "update_db": SCRIPTS_DIR
}

# データファイル（拡張子ベース）
data_extensions = [".db", ".csv", ".json"]

def is_data_file(file):
    return any(file.endswith(ext) for ext in data_extensions)

def safe_move(src, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, os.path.basename(src))
    print(f"🔄 移動: {src} -> {dst}")
    shutil.move(src, dst)

def classify_file(file):
    for key, target_dir in mapping_rules.items():
        if key in file:
            return target_dir
    if is_data_file(file):
        return DATA_DIR
    # 該当しないものは scripts にぶち込む
    return SCRIPTS_DIR

def execute_super_refactor():
    print("📦 フォルダ準備")
    for d in [APP_DIR, GUI_DIR, DATA_DIR, SCRIPTS_DIR, TESTS_DIR]:
        os.makedirs(d, exist_ok=True)

    for file in os.listdir(ROOT_DIR):
        if os.path.isfile(file) and not file.startswith("super_refactor"):
            target_dir = classify_file(file)
            safe_move(file, target_dir)

    # __pycache__ もついでに掃除
    pycache = os.path.join(ROOT_DIR, "__pycache__")
    if os.path.exists(pycache):
        shutil.rmtree(pycache)
        print("🧹 __pycache__ を削除")

    print("\n🎉 スーパー整理完了！ importは自分で確認しよう")

if __name__ == "__main__":
    execute_super_refactor()

