import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

root = tk.Tk()
root.title("ポスター表示テスト")

def show_poster(poster_path):
    url = f"https://image.tmdb.org/t/p/w500{poster_path}"
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((200, 300))  # サイズ調整
    photo = ImageTk.PhotoImage(img)
    
    label.config(image=photo)
    label.image = photo  # 参照を保持！

# ここを映画の poster_path に変更
sample_path = "/qJ2tW6WMUDux911r6m7haRef0WH.jpg"
label = tk.Label(root)
label.pack(pady=20)

show_button = tk.Button(root, text="ポスター表示", command=lambda: show_poster(sample_path))
show_button.pack()

root.mainloop()

