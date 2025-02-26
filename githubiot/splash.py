import time
import os

def show_splash():
    """Tampilkan splash screen dan prompt sambutan."""
    print("""
    ====================================
    Welcome to GitHubIoT App!
    ====================================
    """)
    time.sleep(1)
    print("Available commands:")
    print("  - githubiot --name <app_name> --url-json <url> --icon <icon_path> --status <run/build>")
    print("  - githubiot --help")
    time.sleep(1)
