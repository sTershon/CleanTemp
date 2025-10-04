import os
import shutil
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

CLEAN_PATHS = [
    tempfile.gettempdir(),
    os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch'),
    os.path.join(os.environ.get('SystemDrive', 'C:'), "$Recycle.Bin")
]

def human_size(size):
    for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} ТБ"

def folder_size(path):
    total = 0
    for root, _, files in os.walk(path, topdown=True):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except: pass
    return total

def total_size():
    return sum(folder_size(p) for p in CLEAN_PATHS if os.path.exists(p))

def clean_temp():
    progress.start()
    root.after(200, perform_clean)

def perform_clean():
    deleted = 0
    for path in CLEAN_PATHS:
        if os.path.exists(path):
            for root_dir, dirs, files in os.walk(path, topdown=False):
                for f in files:
                    try:
                        os.remove(os.path.join(root_dir, f))
                        deleted += 1
                    except: pass
                for d in dirs:
                    shutil.rmtree(os.path.join(root_dir, d), ignore_errors=True)
    progress.stop()
    log_clean()
    messagebox.showinfo("✅ Готово", f"Удалено файлов: {deleted}\nОчистка завершена.")
    refresh_size()

def refresh_size():
    size = total_size()
    size_label.config(text=f"Можно освободить: {human_size(size)}")

def log_clean():
    with open("clean_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Очистка завершена\n")

# ---- UI ----
root = tk.Tk()
root.title("🧹 CleanTemp by TershonPC")
root.geometry("420x320")
root.configure(bg="#202020")
 # добавим иконку (можно поменять)

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=8, font=("Segoe UI", 11), background="#3a3a3a", foreground="white")
style.configure("TLabel", background="#202020", foreground="white")

ttk.Label(root, text="CleanTemp", font=("Segoe UI", 16, "bold"), foreground="#00bfff").pack(pady=10)
ttk.Label(root, text="Очистка временных файлов Windows", font=("Segoe UI", 10)).pack(pady=5)

size_label = ttk.Label(root, text="Подсчёт размера...")
size_label.pack(pady=5)

progress = ttk.Progressbar(root, mode="indeterminate", length=260)
progress.pack(pady=15)

ttk.Button(root, text="🧹 Очистить систему", command=clean_temp).pack(pady=5)
ttk.Button(root, text="🔄 Обновить размер", command=refresh_size).pack(pady=5)

ttk.Label(root, text="⚠️ Запускайте от имени администратора", font=("Segoe UI", 8), foreground="#aaaaaa").pack(side="bottom", pady=8)

refresh_size()
root.mainloop()
