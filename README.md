# movie_app_py

映画情報をTMDB APIから取得し、データベースに保存・管理するPythonアプリケーションです。

## 機能

- TMDB APIを使った映画情報の取得
- SQLite（または他のDB）への映画データ保存
- 映画情報の検索・表示機能
- 簡単なCLI操作サポート
- 自動テスト対応（pytest推奨）

## 動作環境

- Python 3.8以上
- 必要なパッケージは `requirements.txt` に記載

## インストール方法

```bash
git clone https://github.com/koko812/movie_app_py
cd movie_app_py
python -m venv venv
source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate`
pip install -r requirements.txt

