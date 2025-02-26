import argparse
import subprocess
import sys
import os
from .app import JSONGraphApp
from .splash import show_splash

def start(name=None, url_json=None, icon=None, status="run"):
    """
    Fungsi utama untuk menjalankan atau membuild aplikasi.
    
    :param name: Nama aplikasi.
    :param url_json: URL JSON data.
    :param icon: Path ke file icon.
    :param status: 'run' untuk menjalankan aplikasi, 'build' untuk membuild aplikasi.
    """
    if status == "run":
        run_app(name, url_json, icon)
    elif status == "build":
        build_app(name, url_json, icon)
        run_app(name, url_json, icon)  # Jalankan setelah build
    else:
        print("Status tidak valid. Gunakan 'run' atau 'build'.")

def run_app(name=None, url_json=None, icon=None):
    """Jalankan aplikasi."""
    from tkinter import Tk
    root = Tk()
    app = JSONGraphApp(root, name, url_json, icon)
    root.mainloop()

def build_app(name=None, url_json=None, icon=None):
    """Build aplikasi ke .exe."""
    try:
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--windowed",
            f"--name={name}" if name else "--name=GitHubIoTApp",
            f"--icon={icon}" if icon else "",
            "githubiot/app.py"
        ], check=True)
        print("🎉 Build berhasil! File .exe ada di folder 'dist/'.")
    except Exception as e:
        print(f"🔥 Build gagal: {e}")

def main():
    """Fungsi utama untuk CLI."""
    show_splash()  # Tampilkan splash screen
    parser = argparse.ArgumentParser(description="GitHubIoT App Manager")
    parser.add_argument("--name", help="Nama aplikasi")
    parser.add_argument("--url-json", help="URL JSON data")
    parser.add_argument("--icon", help="Path ke file icon")
    parser.add_argument("--status", choices=["run", "build"], default="run", help="Jalankan atau build aplikasi")
    args = parser.parse_args()

    start(name=args.name, url_json=args.url_json, icon=args.icon, status=args.status)

if __name__ == "__main__":
    main()
