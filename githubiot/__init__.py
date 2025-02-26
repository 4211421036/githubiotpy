import os
import sys
import json
import subprocess
from .app_manager import create_app, update_config, run_app, build_app

__version__ = "1.0.0"

def start(name=None, url_json=None, icon=None, status="run"):
    """
    Start the GitHubIoT application
    
    Args:
        name (str, optional): Application name
        url_json (str, optional): JSON URL for data
        icon (str, optional): Path to icon file
        status (str, optional): 'run' or 'build'
    """
    # Create app if it doesn't exist
    if not os.path.exists('main.py'):
        create_app()
    
    # Update config if parameters provided
    if name:
        update_config('app_name', name)
    
    if url_json:
        update_config('url', url_json)
    
    # Download icon if specified
    if icon and icon.startswith(('http://', 'https://')):
        try:
            import requests
            response = requests.get(icon)
            with open('icon.ico', 'wb') as f:
                f.write(response.content)
            print(f"✅ Downloaded icon from {icon}")
        except Exception as e:
            print(f"❌ Error downloading icon: {e}")
    
    # Run or build based on status
    if status.lower() == "build":
        build_app()
        # Find the executable in the dist directory
        try:
            app_name = json.load(open('config.json'))['app_name']
            exe_path = os.path.join('dist', f"{app_name}.exe")
            if os.path.exists(exe_path):
                subprocess.Popen(exe_path)
                print(f"🚀 Launched {app_name}.exe")
        except Exception as e:
            print(f"❌ Error launching executable: {e}")
    else:
        run_app()
