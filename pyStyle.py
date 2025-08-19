import tkinter as tk
from tkinter import ttk


headerFont = ("Bahnschrift", 18, "bold")
bodyFont = ("Sylfaen", 12)
buttonFont = ("Lucida Console", 12)
optionFont = ("Corbel", 10)

treeviewList : list = []

class StyleFactory:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style(root)
        self.style.theme_use('alt') #'winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'

    def _configure_styles(self, colors):
        self.style.configure(
            '.',
            font=bodyFont,
            background=colors[0],
            foreground=colors[3]
        )
        self.style.configure(
            'TButton',
            font=buttonFont,
            padding=6,
            relief='raised',
            background=colors[0],
            foreground=colors[3],
        )
        self.style.map(
            'TButton',
            background=[('active', colors[1]), ('pressed', colors[0])],
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
        )
        self.style.configure(
            'TCheckbutton',
            font=buttonFont,
            background=colors[0],
            foreground=colors[3],
            indicatorcolor=colors[0]
        )
        self.style.map(
            'TCheckbutton',
            background=[('active', colors[1]), ('pressed', colors[0])]
        )
        self.style.configure(
            'TCombobox',
            background=colors[0],
            fieldbackground=colors[1],
            font=optionFont,
            padding=5
        )
        self.style.map(
            'TCombobox',
            fieldbackground=[('readonly', colors[1])]
        )
        self.style.configure(
            'TEntry',
            background=colors[0],
            fieldbackground=colors[1],
            font=bodyFont
        )
        self.style.map(
            'TEntry',
            background=[('active', colors[1])]
        )
        self.style.configure(
            'TFrame',
            background=colors[0]
        )
        self.style.configure(
            'TLabel',
            font=bodyFont
        )
        self.style.configure(
            'TLabelFrame',
            font=bodyFont
        )
        self.style.configure(
            'TLabelFrame.Label',
            font=bodyFont
        )
        self.style.configure(
            'TMenubutton',
            font=optionFont
        )
        self.style.map(
            'TMenubutton',
            background=[('active', colors[1]), ('pressed', colors[0])]
        )
        self.style.configure(
            'TNotebook',
            font=headerFont
        )
        self.style.configure(
            'TNotebook.Tab',
            font=optionFont,
            padding=[10,5]
        )
        self.style.map(
            'TNotebook.Tab',
            background=[('active', colors[1]), ('!active', colors[0])]
        )
        self.style.configure(
            'TProgressbar',
            background=colors[2],
            troughcolor=colors[0]
        )
        self.style.configure(
            'TRadiobutton',
            font=buttonFont,
            background=colors[0]
        )
        self.style.map(
            'TRadiobutton',
            background=[('active', colors[1]), ('pressed', colors[0])]
        )
        self.style.configure(
            'TScale',
            background=colors[0],
        )
        self.style.configure(
            'TScrollBar',
            arrowsize=15
        )
        self.style.configure(
            'Treeview',
            font=optionFont,
            rowheight=25,
            foreground=colors[3],
            background=colors[1],
            fieldbackground=colors[1]
        )
        self.style.configure(
            'Treeview.Heading', 
            foreground=colors[3],
            background=colors[1],
            fieldbackground=colors[1],
            font=buttonFont
        )
        
    
    def update_styles(self, root, colors):
        self._configure_styles(colors)
        self.refresh_widgets(root)

    def refresh_widgets(self, root):
        for widget in root.winfo_children():
                    if isinstance(widget, (ttk.Button, ttk.Checkbutton, ttk.Combobox, ttk.Frame, ttk.Label, ttk.Labelframe, ttk.Menubutton, 
                                          ttk.Notebook, ttk.Progressbar, ttk.Radiobutton, ttk.Scale, ttk.Scrollbar, ttk.Treeview)):
                        try:
                            current_style = widget['style'] if 'style' in widget.configure() else ''
                            if current_style:
                                widget.configure(style='')
                                widget.configure(style=current_style)
                        except Exception as e:
                            print(f"Error refreshing widget: {e}")



    def add_treeview(widget):
        treeviewList.append(widget)
        
    def treeview_static(event):
        for widget in treeviewList:
            if widget.identify_region(event.x, event.y) == "separator":
                return "break"



    def update_children(self, parent):
        for child in parent.winfo_children():
            try:
                if isinstance(child, (ttk.Button, ttk.Checkbutton, ttk.Combobox, ttk.Frame, ttk.Label, ttk.Labelframe, ttk.Menubutton, 
                                     ttk.Notebook, ttk.Progressbar, ttk.Radiobutton, ttk.Scale, ttk.Scrollbar, ttk.Treeview)):
                     current_style = child['style'] if 'style' in child.configure() else ''
                     if current_style:
                          child.configure(style='')
                          child.configure(style=current_style)
            except Exception as e:
                print(f"Error refreshing child widget: {e}")
            if child.winfo_children():
                 self.update_children

    def _darken_color(self, hex_color, factor = 0.8): 
        rgb=tuple(int(hex_color[i,i+2], 16) for i in (1, 3, 5))
        darkened=tuple(max(0, min(255, int(c*factor))) for c in rgb)
        return "#{:02x}{:02x}{:02x}".format(*darkened)
