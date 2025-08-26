from pystyle import StyleFactory, launch_settings
import tkinter as tk
from tkinter import ttk
import yaml
from pathlib import Path

root = tk.Tk()
root.geometry("200x100")
root.resizable(False, False)

#Required for first initialize
st=StyleFactory(root)
config_path = Path("config.yaml")
def load_config():
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    else:
        return None
colors = []
try:        
    configYAML = load_config()
    colors = configYAML['current colors']
except:
    colors = [
        "#f0f0f0"
        "#d2d2d2"
        '#008000'
        '#000000'
        '#bf7900'
        '#d40000'
    ]
st.update_styles(
    root, configYAML['current colors'])
#-

frame=ttk.Frame(
    root,
    width=200,
    height=100
)
frame.place(
    x=0
)
settingsButton=ttk.Button(
    root,
    text="Open Colors",
    command=lambda: launch_settings(root)
)
settingsButton.place(
    anchor="center",
    relx=0.5,
    rely=0.25
)
uselessButton=ttk.Button(
    root,
    text="I do nothing."
)
uselessButton.place(
    anchor="center",
    relx=0.5,
    rely=0.75
)


root.mainloop()
