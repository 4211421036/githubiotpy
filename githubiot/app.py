import tkinter as tk
from tkinter import messagebox, filedialog, Menu
import requests
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import os

# Versi aplikasi
VERSION = "1.0.0"

class JSONGraphApp:
    def __init__(self, root):
        self.root = root
        self.config = self.load_config()
        self.update_title()  # Set judul awal
        self.root.geometry("1000x700")
        self.animation_running = True
        self.create_menu()
        self.create_widgets()
        self.load_data()
        self.setup_animation()
        
        # Tandai aplikasi sedang berjalan
        with open("app.running", "w") as running_file:
            running_file.write("running")
        
        # Periksa pembaruan judul secara berkala
        self.root.after(1000, self.check_for_updates)
    
    def check_for_updates(self):
        """Periksa apakah ada permintaan pembaruan judul"""
        if os.path.exists("app.running"):
            with open("app.running", "r") as running_file:
                content = running_file.read().strip()
                if content == "refresh":
                    self.config = self.load_config()
                    self.update_title()
                    with open("app.running", "w") as running_file:
                        running_file.write("running")  # Reset status
        self.root.after(1000, self.check_for_updates)  # Periksa lagi setelah 1 detik
    
    def update_title(self):
        """Perbarui judul aplikasi"""
        self.root.title(self.config.get("app_name", "GitHubIoT App"))
    
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {"url": "https://api.example.com/data", "app_name": "GitHubIoT App"}
    
    def create_menu(self):
        menubar = Menu(self.root)
        
         # File Menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Graph", command=self.save_graph)
        file_menu.add_command(label="Change Theme", command=self.change_theme)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Options Menu
        options_menu = Menu(menubar, tearoff=0)
        options_menu.add_checkbutton(label="Animation", variable=tk.BooleanVar(value=True), 
                                  command=self.toggle_animation)
        menubar.add_cascade(label="Options", menu=options_menu)
        
        # Help Menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_widgets(self):
        """Create UI widgets"""
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=1)
        
        # Buat toolbar
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Tombol refresh
        self.btn_refresh = tk.Button(
            self.toolbar, 
            text="Refresh", 
            command=self.refresh_data
        )
        self.btn_refresh.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Grafik
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    def load_data(self):
        try:
            response = requests.get(self.config['url'])
            self.data = response.json()
            self.create_graph()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = self.generate_sample_data()
            self.create_graph()
    
    def refresh_data(self):
        self.load_data()
    
    def generate_sample_data(self):
        # Generate sample EM wave data
        x = np.linspace(0, 4 * np.pi, 200)
        return {
            "time": x.tolist(),
            "amplitude": np.sin(x).tolist()
        }
    
    def create_graph(self):
        """Create initial graph"""
        self.ax.clear()
        self.ax.set_title("EM Wave Visualization", fontsize=12, pad=10)
        self.ax.set_xlabel("Time", fontsize=10)
        self.ax.set_ylabel("Amplitude", fontsize=10)
        self.line, = self.ax.plot([], [], lw=2, label="Wave")
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.legend(loc='upper right')
        
        # Sesuaikan warna teks sumbu dan judul
        for spine in self.ax.spines.values():
            spine.set_edgecolor('gray')
        self.ax.title.set_color('black' if plt.style.available[-1] != 'dark_background' else 'white')
        self.ax.xaxis.label.set_color('black' if plt.style.available[-1] != 'dark_background' else 'white')
        self.ax.yaxis.label.set_color('black' if plt.style.available[-1] != 'dark_background' else 'white')
        self.ax.tick_params(axis='x', colors='black' if plt.style.available[-1] != 'dark_background' else 'white')
        self.ax.tick_params(axis='y', colors='black' if plt.style.available[-1] != 'dark_background' else 'white')
    
    def setup_animation(self):
        self.ani = animation.FuncAnimation(
            self.fig, self.animate, 
            frames=200, interval=50, 
            blit=True
        )
    
    def animate(self, i):
        if self.animation_running:
            x = np.array(self.data["time"])
            y = np.array(self.data["amplitude"])
            self.line.set_data(x[:i], y[:i])
            self.ax.relim()
            self.ax.autoscale_view()
        return self.line,
    
    def toggle_animation(self):
        self.animation_running = not self.animation_running
        if self.animation_running:
            self.ani.event_source.start()
        else:
            self.ani.event_source.stop()
    
    def save_graph(self):
        filetypes = [('PNG files', '*.png'), ('All files', '*.*')]
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes)
        if filename:
            self.fig.savefig(filename)
            messagebox.showinfo("Info", f"Graph saved to {filename}")
    
    def change_theme(self):
        """Change graph theme"""
        themes = [
            'default', 'classic', 'dark_background', 'ggplot', 'seaborn',
            'Solarize_Light2', 'bmh', 'tableau-colorblind10', 'fivethirtyeight'
        ]
        
        # Dapatkan tema yang sedang aktif
        current_theme = plt.style.available[-1] if plt.style.available else 'default'
        
        # Cari indeks tema saat ini dan pilih tema berikutnya
        if current_theme in themes:
            current_index = themes.index(current_theme)
            new_theme = themes[(current_index + 1) % len(themes)]
        else:
            new_theme = themes[0]  # Default ke tema pertama jika tema saat ini tidak ditemukan
        
        # Terapkan tema baru
        plt.style.use(new_theme)
        self.apply_theme_to_ui(new_theme)  # Sesuaikan tema UI
        self.create_graph()
        self.canvas.draw()

    def apply_theme_to_ui(self, theme):
        """Sesuaikan tema aplikasi (UI) berdasarkan tema grafik"""
        if theme in ['dark_background', 'Solarize_Light2']:
            # Tema gelap
            self.root.configure(bg='#2E2E2E')
            self.frame.configure(bg='#2E2E2E')
            if hasattr(self, 'toolbar'):  # Pastikan toolbar sudah diinisialisasi
                self.toolbar.configure(bg='#2E2E2E')
            if hasattr(self, 'btn_refresh'):  # Pastikan tombol refresh sudah diinisialisasi
                self.btn_refresh.configure(bg='#4E4E4E', fg='white')
        else:
            # Tema terang
            self.root.configure(bg='#F0F0F0')
            self.frame.configure(bg='#F0F0F0')
            if hasattr(self, 'toolbar'):  # Pastikan toolbar sudah diinisialisasi
                self.toolbar.configure(bg='#F0F0F0')
            if hasattr(self, 'btn_refresh'):  # Pastikan tombol refresh sudah diinisialisasi
                self.btn_refresh.configure(bg='#E0E0E0', fg='black')

    def add_custom_theme(self):
        """Tambahkan tema kustom"""
        custom_theme = {
            'axes.facecolor': '#F5F5F5',
            'axes.edgecolor': '#333333',
            'axes.labelcolor': '#333333',
            'xtick.color': '#333333',
            'ytick.color': '#333333',
            'text.color': '#333333',
            'grid.color': '#CCCCCC',
            'figure.facecolor': '#FFFFFF',
            'figure.edgecolor': '#FFFFFF',
        }
        plt.style.use(custom_theme)
    
    def show_about(self):
        VERSION = "1.0.0"
        about_info = f"""
        {self.config.get("app_name", "GitHubIoT App")}
        Version: {VERSION}
        Author: GALIH RIDHO UTOMO, Fionita Fahra Azzahra
        License: MIT
        """
        messagebox.showinfo("About", about_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = JSONGraphApp(root)
    root.mainloop()
