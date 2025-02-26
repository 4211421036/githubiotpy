import argparse
import os
import subprocess
import sys
import json

VERSION = "1.0.0"
TEMPLATE_FILES = {
    'main.py': '''import tkinter as tk
import requests
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GitHub IoT:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Data Graph")
        self.root.geometry("800x600")
        
        self.load_config()
        self.create_widgets()
        self.load_data()
    
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {"url": "https://api.example.com/data"}
    
    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=1)
        
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.btn_refresh = tk.Button(
            self.toolbar, 
            text="Refresh", 
            command=self.refresh_data
        )
        self.btn_refresh.pack(side=tk.LEFT, padx=2, pady=2)
    
    def load_data(self):
        try:
            response = requests.get(self.config['url'])
            data = response.json()
            self.create_graph(data)
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def create_graph(self, data):
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
        
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Customize this based on your JSON structure
        if isinstance(data, list):
            ax.plot(data)
        elif isinstance(data, dict):
            ax.bar(data.keys(), data.values())
        
        self.canvas = FigureCanvasTkAgg(fig, self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    def refresh_data(self):
        self.load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHub IoT(root)
    root.mainloop()
''',
    
    'config.json': '''{
    "url": "https://api.example.com/data"
}''',
    
    'requirements.txt': '''requests>=2.26.0
matplotlib>=3.5.0
numpy>=1.21.0
pyinstaller>=5.0.0''',
    
    '.gitignore': '''__pycache__/
dist/
build/
*.spec
*.exe
'''
}
TEMPLATE_FILES['config.json'] = '''{
    "url": "https://api.example.com/data",
    "app_name": "GitHub IoT"
}'''

def update_config(key, value):
    """Update config.json dengan key dan value baru"""
    try:
        with open('config.json', 'r+') as f:
            config = json.load(f)
            config[key] = value
            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()
        print(f"✅ Updated {key} to {value}")
    except Exception as e:
        print(f"❌ Error updating config: {e}")

def set_json_url():
    if not os.path.exists('config.json'):
        print("❌ config.json not found. Run 'githubiot --create-app' first.")
        return
    
    current_url = json.load(open('config.json'))['url']
    print(f"\nCurrent JSON URL: {current_url}")
    new_url = input("Enter new JSON URL: ").strip()
    
    if not new_url.startswith(('http://', 'https://')):
        print("⚠️  Warning: URL format seems invalid")
    
    update_config('url', new_url)


def set_app_name():
    if not os.path.exists('config.json'):
        print("❌ config.json not found. Run 'githubiot --create-app' first.")
        return
    
    current_name = json.load(open('config.json'))['app_name']
    print(f"\nCurrent App Name: {current_name}")
    new_name = input("Enter new application name: ").strip()
    
    if not new_name:
        print("❌ Application name cannot be empty!")
        return
    
    update_config('app_name', new_name)

def create_app():
    for filename, content in TEMPLATE_FILES.items():
        if os.path.exists(filename):
            print(f"⚠️  {filename} already exists. Skipping.")
            continue
        try:
            with open(filename, 'w') as f:
                f.write(content)
            print(f"✅ Created {filename}")
        except Exception as e:
            print(f"❌ Error creating {filename}: {str(e)}")
    
    if not os.path.exists('icon.ico'):
        try:
            with open('icon.ico', 'wb') as f:
                pass
            print("✅ Created placeholder icon.ico (replace with your icon)")
        except Exception as e:
            print(f"❌ Error creating icon.ico: {str(e)}")

def build_app():
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found. Run 'githubiot --create-app' first.")
        return
    
    icon_args = ['--icon=icon.ico'] if os.path.exists('icon.ico') else []
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        app_name = config['app_name']
        subprocess.run([
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name=' + app_name,
            '--clean',
            *icon_args,
            'main.py'
        ], check=True)
        print("\n🎉 Build successful! EXE available in dist/ directory")
    except Exception as e:
        print(f"\n🔥 Build failed: {str(e)}")
        app_name = "GitHub IoT"

def run_app():
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found. Run 'githubiot --create-app' first.")
        return
    
    try:
        subprocess.run([sys.executable, 'main.py'], check=True)
    except Exception as e:
        print(f"❌ Error running app: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='GitHubIoT App Manager',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--create-app', action='store_true', 
                       help='Create new application template')
    parser.add_argument('--json-url', action='store_true',
                       help='Set custom JSON URL')
    parser.add_argument('--name', action='store_true',
                       help='Set custom application name')
    parser.add_argument('--build', action='store_true',
                       help='Build application to EXE')
    parser.add_argument('--run', action='store_true',
                       help='Run application')
    parser.add_argument('-v', '--version', action='store_true',
                       help='Show version')

    args = parser.parse_args()

    if args.version:
        print(f"GitHubIoT CLI Version {VERSION}")
    elif args.create_app:
        print("\n🛠️  Creating new application template...")
        create_app()
    elif args.build:
        print("\n🔨 Building application...")
        build_app()
    elif args.json_url:
        print("\n🌐 Setting JSON URL...")
        set_json_url()
    elif args.name:
        print("\n🏷️  Setting application name...")
        set_app_name()
    elif args.run:
        print("\n🚀 Launching application...")
        run_app()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()