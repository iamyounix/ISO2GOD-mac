import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

iso2god_path = resource_path("iso2god-x86_64-macos")

def select_iso_file():
    iso_file = filedialog.askopenfilename(filetypes=[("ISO Files", "*.iso")])
    iso_file_entry.delete(0, tk.END)
    iso_file_entry.insert(0, iso_file)

def select_destination_folder():
    dest_folder = filedialog.askdirectory()
    dest_folder_entry.delete(0, tk.END)
    dest_folder_entry.insert(0, dest_folder)

def run_conversion():
    iso_file = iso_file_entry.get()
    dest_folder = dest_folder_entry.get()
    game_title = game_title_entry.get()
    trim = trim_var.get()
    
    if not iso_file or not dest_folder:
        messagebox.showerror("Error", "Please select both an ISO file and a destination folder.")
        return
    
    command = [iso2god_path, iso_file, dest_folder]

    if game_title:
        command.extend(["--game-title", game_title])
    if trim:
        command.append("--trim")
    
    try:
        progress_bar.start()
        convert_button.config(state=tk.DISABLED)
        
        result = subprocess.run(command, capture_output=True, text=True)

        progress_bar.stop()
        convert_button.config(state=tk.NORMAL)

        if result.returncode == 0:
            messagebox.showinfo("Success", "ISO conversion completed successfully!")
        else:
            messagebox.showerror("Error", f"Conversion failed:\n{result.stderr}")
    except Exception as e:
        progress_bar.stop()
        convert_button.config(state=tk.NORMAL)
        messagebox.showerror("Error", f"An error occurred: {e}")

def convert_iso():
    conversion_thread = threading.Thread(target=run_conversion)
    conversion_thread.start()

root = tk.Tk()
root.title("ISO2GOD Converter")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Select ISO file:").grid(row=0, column=0, sticky="w")
iso_file_entry = tk.Entry(frame, width=40)
iso_file_entry.grid(row=0, column=1)
tk.Button(frame, text="Browse", command=select_iso_file).grid(row=0, column=2)

tk.Label(frame, text="Select destination folder:").grid(row=1, column=0, sticky="w")
dest_folder_entry = tk.Entry(frame, width=40)
dest_folder_entry.grid(row=1, column=1)
tk.Button(frame, text="Browse", command=select_destination_folder).grid(row=1, column=2)

tk.Label(frame, text="Game title (optional):").grid(row=2, column=0, sticky="w")
game_title_entry = tk.Entry(frame, width=40)
game_title_entry.grid(row=2, column=1, columnspan=2)

trim_var = tk.BooleanVar()
trim_checkbox = tk.Checkbutton(frame, text="Trim unused space", variable=trim_var)
trim_checkbox.grid(row=3, column=0, columnspan=3, sticky="w")

progress_bar = ttk.Progressbar(root, mode="indeterminate")
progress_bar.pack(pady=10, fill=tk.X)

convert_button = tk.Button(root, text="Convert ISO", command=convert_iso)
convert_button.pack(pady=10)

root.mainloop()
