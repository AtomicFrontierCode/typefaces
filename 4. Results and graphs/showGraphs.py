import os
import csv
import difflib
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.gridspec as gridspec
import tkinter as tk

# === USER SETTINGS ===
loading = "Bending"
show = "A"
dataSource = r"normalisedResults.txt"
imageFolder = r"allProfilesSmall"

# === CONSTANTS ===
VALID_LOADS = ["bending", "buckling", "torsion"]
ALPHABET_ORDER = [
    "A", "B", "C", "D", "E", "F",
    "G", "H", "H_rot", "I", "J", "K",
    "L", "M", "N", "O", "P", "Q",
    "R", "S", "T", "U", "V", "W"
]

# === DATA LOADING ===
def load_data(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['mass'] = float(row['mass'])
            for load in VALID_LOADS:
                row[load] = float(row[load])
            data.append(row)
    return data

def normalize_loading(value):
    value = value.strip().lower()
    return difflib.get_close_matches(value, VALID_LOADS, n=1, cutoff=0.6)[0]

def normalize_show(value):
    value = value.strip().upper()
    if value == "H_ROT":
        return "H_rot"
    return value

# === IMAGE WINDOW ===
class ImageWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Beam Profile")
        self.label = tk.Label(self)
        self.label.pack()
        self.tk_image = None

    def show(self, path, rotate=False):
        if os.path.exists(path):
            img = Image.open(path)
            if rotate:
                img = img.rotate(90, expand=True)
            self.tk_image = ImageTk.PhotoImage(img)
            self.label.configure(image=self.tk_image)

# === PLOT HELPERS ===
def get_image_path(font, char):
    return os.path.join(imageFolder, f"{font}_{char}.png")

def setup_hover(fig, ax, points, labels, paths, image_win, rotate_flags):
    tooltip = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                          bbox=dict(boxstyle="round", fc="white"),
                          arrowprops=dict(arrowstyle="->"))
    tooltip.set_visible(False)

    def on_move(event):
        vis = False
        for i, pt in enumerate(points):
            cont, _ = pt.contains(event)
            if cont:
                x, y = pt.get_xdata()[0], pt.get_ydata()[0]
                tooltip.xy = (x, y)
                tooltip.set_text(labels[i])
                tooltip.set_visible(True)
                image_win.show(paths[i], rotate=rotate_flags[i])
                vis = True
                break
        if not vis:
            tooltip.set_visible(False)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", on_move)

def plot_single_letter(data, letter, load, image_win):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(f"Glyph: {letter}")
    ax.set_xlabel("Mass (Normalized)")
    ax.set_ylabel(f"{load.capitalize()} Load (Normalized)")
    ax.grid(True)

    filled = next((d for d in data if d["fontName"] == "filled"), None)
    control = next((d for d in data if d["fontName"].lower().startswith("control")), None)

    if filled:
        ax.plot([0, filled['mass']], [0, filled[load]], color='black', lw=2)
    if load == 'bending' and control:
        slope = control[load] / control['mass']
        ax.plot([0, 1], [0, slope], color='orange', lw=2)

    points, labels, paths, rotates = [], [], [], []

    for row in data:
        match = (row['letter'].upper() == letter.upper()) or \
                (letter == "H_rot" and row['letter'].upper() == "H")
        if match or row['fontName'] in ["filled", "ControlIPE100"]:
            x, y = row['mass'], row[load]

            if row['fontName'] == "filled":
                pt, = ax.plot(x, y, 'o', color='black', alpha=1.0, markersize=7)
            elif row['fontName'].lower().startswith("control"):
                pt, = ax.plot(x, y, 'o', color='orange', alpha=0.8, markersize=7)
            else:
                pt, = ax.plot(x, y, 'o', color='black', alpha=0.5, markersize=6)

            points.append(pt)
            labels.append(row['fontName'])
            paths.append(get_image_path(row['fontName'], row['letter']))
            rotates.append(letter == "H_rot")

    setup_hover(fig, ax, points, labels, paths, image_win, rotates)
    plt.show()


# === RUN ===
data = load_data(dataSource)
loading = normalize_loading(loading)
show = normalize_show(show)

# Create the GUI window and call plotting inside it
app = ImageWindow()

def start_plot():
    plot_single_letter(data, show, loading, app)

app.after(100, start_plot)
app.mainloop()


