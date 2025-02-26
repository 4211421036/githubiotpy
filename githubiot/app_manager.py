# githubiot/app_manager.py
import argparse
import os
import subprocess
import sys
import json
import time
import pkgutil
import tempfile

VERSION = "1.0.0"

def get_template_content(template_name):
    """Get template content from the templates directory"""
    template_path = f"templates/{template_name}"
    data = pkgutil.get_data("githubiot", template_path)
    if data:
        return data.decode('utf-8')
    return ""

def update_config(key, value):
    """Update config.json with key and value"""
    try:
        with open('config.json', 'r+') as f:
            config = json.load(f)
            config[key] = value
            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()
        print(f"✅ Updated {key} to {value}")
        
        # If app is running, update title
        if key == "app_name" and os.path.exists("app.running"):
            try:
                with open("app.running", "w") as running_file:
                    running_file.write("refresh")
                time.sleep(0.5)
            except Exception as e:
                print(f"⚠️  Could not update running app title: {e}")
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
    templates = {
        'main.py': get_template_content('main.py'),
        'config.json': get_template_content('config.json'),
        'requirements.txt': get_template_content('requirements.txt'),
        '.gitignore': get_template_content('.gitignore')
    }
    
    for filename, content in templates.items():
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
    
    # Open folder in code editor if possible
    try:
        cwd = os.getcwd()
        if sys.platform.startswith('win'):
            # Try to open with VS Code, then with Notepad if VS Code is not available
            try:
                subprocess.Popen(['code', cwd])
            except:
                subprocess.Popen(['explorer', cwd])
        elif sys.platform.startswith('darwin'):  # macOS
            subprocess.Popen(['open', cwd])
        else:  # Linux
            try:
                subprocess.Popen(['code', cwd])
            except:
                subprocess.Popen(['xdg-open', cwd])
    except Exception as e:
        print(f"⚠️  Could not open folder in editor: {e}")

def build_app():
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found. Run 'githubiot --create-app' first.")
        return
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        app_name = config['app_name']
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        app_name = "JSONGraphApp"
    
    icon_args = ['--icon=icon.ico'] if os.path.exists('icon.ico') else []
    
    try:
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

def run_app():
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found. Run 'githubiot --create-app' first.")
        return
    
    try:
        subprocess.run([sys.executable, 'main.py'], check=True)
    except Exception as e:
        print(f"❌ Error running app: {str(e)}")

def display_splash():
    """Display splash screen when CLI is invoked"""
    splash = f"""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║   ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗██████╗ ██╗ ██████╗ ████████╗ ║
    ║  ██╔════╝ ██║╚══██╔══╝██║  ██║██║   ██║██╔══██╗██║██╔═══██╗╚══██╔══╝ ║
    ║  ██║  ███╗██║   ██║   ███████║██║   ██║██████╔╝██║██║   ██║   ██║    ║
    ║  ██║   ██║██║   ██║   ██╔══██║██║   ██║██╔══██╗██║██║   ██║   ██║    ║
    ║  ╚██████╔╝██║   ██║   ██║  ██║╚██████╔╝██████╔╝██║╚██████╔╝   ██║    ║
    ║   ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝    ╚═╝    ║
    ║                                                                      ║
    ║                   IoT Visualization Toolkit                          ║
    ║                                                                      ║
    ║                        Version {VERSION}                             ║
    ║             Created by GALIH RIDHO UTOMO & Fionita                   ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    
    Welcome to GitHubIoT! 🚀
    
    Available commands:
      githubiot --create-app  : Create new application template
      githubiot --build       : Build application to EXE
      githubiot --run         : Run application
      githubiot --json-url    : Set custom JSON URL
      githubiot --name        : Set custom application name
      githubiot -v, --version : Show version
      
    For more information, run: githubiot --help
    """
    print(splash)

def main():
    # Display splash screen first
    display_splash()
    
    parser = argparse.ArgumentParser(
        description='GitHubIoT App Manager',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--create-app', action='store_true', 
                       help='Create new application template')
    parser.add_argument('--build', action='store_true',
                       help='Build application to EXE')
    parser.add_argument('--run', action='store_true',
                       help='Run application')
    parser.add_argument('-v', '--version', action='store_true',
                       help='Show version')
    parser.add_argument('--json-url', action='store_true',
                       help='Set custom JSON URL')
    parser.add_argument('--name', action='store_true',
                       help='Set custom application name')
    
    args = parser.parse_args()

    if args.version:
        print(f"GitHubIoT CLI Version {VERSION}")
    elif args.create_app:
        print("\n🛠️  Creating new application template...")
        create_app()
    elif args.build:
        print("\n🔨 Building application...")
        build_app()
    elif args.run:
        print("\n🚀 Launching application...")
        run_app()
    elif args.json_url:
        print("\n🌐 Setting JSON URL...")
        set_json_url()
    elif args.name:
        print("\n🏷️  Setting application name...")
        set_app_name()
    else:
        # If no arguments provided, we already showed the splash
        pass
