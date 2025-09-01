
import tkinter as tk
from tkinter import filedialog

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def on_canvas_click(event):
    # Get the color at the clicked pixel
    x, y = event.x, event.y
    if 0 <= x < PALETTE_WIDTH and 0 <= y < PALETTE_HEIGHT:
        if y < HUE_HEIGHT:
            # Clicked on hue slider - update the square colors
            global current_hue
            current_hue = x / PALETTE_WIDTH
            update_square_colors()
        else:
            # Clicked on the square - get the color
            rgb = palette_image.get(x, y)
            rgb_label.config(text=f"RGB: {rgb}")
            hex_label.config(text=f"Hex: {rgb_to_hex(rgb)}")
            # Update the preview color
            preview_canvas.config(bg=rgb_to_hex(rgb))
            # Store the currently selected color
            global current_color
            current_color = rgb

def update_square_colors():
    # Update the saturation/value square with the current hue
    for x in range(SQUARE_SIZE):
        sat = x / SQUARE_SIZE
        for y in range(SQUARE_SIZE):
            val = 1.0 - (y / SQUARE_SIZE)
            r, g, b = colorsys.hsv_to_rgb(current_hue, sat, val)
            r, g, b = int(r*255), int(g*255), int(b*255)
            palette_image.put("#%02x%02x%02x" % (r, g, b), (x + (PALETTE_WIDTH - SQUARE_SIZE) // 2, y + HUE_HEIGHT))
    # Redraw the canvas
    canvas.delete("all")
    canvas.create_image((0, 0), image=palette_image, anchor=tk.NW)

def save_color():
    if current_color is not None:
        hex_color = rgb_to_hex(current_color)
        rgb_str = f"RGB: {current_color}"
        note = note_entry.get().strip()
        # Add to history list with note
        color_history.append((current_color, hex_color, note))
        # Update the history display
        add_color_to_history(current_color, hex_color, rgb_str, note)
        # Clear the note entry
        note_entry.delete(0, tk.END)

def remove_color(color_frame, rgb, hex_color, note):
    # Remove from the list
    color_history.remove((rgb, hex_color, note))
    # Destroy the frame
    color_frame.destroy()

def add_color_to_history(rgb, hex_color, rgb_str, note):
    # Create a frame for each saved color
    frame = tk.Frame(history_frame, bd=1, relief=tk.SOLID, padx=2, pady=2)
    color_preview = tk.Canvas(frame, width=30, height=20, bg=hex_color, highlightthickness=1, highlightbackground="black")
    color_preview.pack(side=tk.LEFT, padx=(0, 5))
    
    # Create text for the label
    label_text = f"{rgb_str}\n{hex_color}"
    if note:
        label_text += f"\nNote: {note}"
    
    label = tk.Label(frame, text=label_text, anchor="w", justify="left")
    label.pack(side=tk.LEFT)
    # Add remove button
    remove_btn = tk.Button(frame, text="X", command=lambda: remove_color(frame, rgb, hex_color, note), 
                          bg="red", fg="white", width=2, height=1)
    remove_btn.pack(side=tk.RIGHT, padx=(5, 0))
    frame.pack(fill=tk.X, pady=2, padx=2)

def export_colors():
    if not color_history:
        return
    
    # Ask user for file location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Export Colors"
    )
    
    if file_path:
        with open(file_path, 'w') as f:
            f.write("Exported Colors\n")
            f.write("=" * 50 + "\n\n")
            for i, (rgb, hex_color, note) in enumerate(color_history, 1):
                f.write(f"{i}. RGB: {rgb} | Hex: {hex_color}")
                if note:
                    f.write(f" | Note: {note}")
                f.write("\n")

PALETTE_WIDTH = 360
PALETTE_HEIGHT = 200

root = tk.Tk()
root.title("Color Picker Palette")

# Create a PhotoImage for the palette
palette_image = tk.PhotoImage(width=PALETTE_WIDTH, height=PALETTE_HEIGHT)

# Fill the palette with a wide range of colors (HSV to RGB)
import colorsys

# Create a color picker similar to htmlcolorcodes.com
# Top section: Hue slider (full width, small height)
HUE_HEIGHT = 30
SQUARE_SIZE = min(PALETTE_WIDTH, PALETTE_HEIGHT - HUE_HEIGHT)

# Initialize current hue
current_hue = 0.0

# Fill the hue slider at the top
for x in range(PALETTE_WIDTH):
    hue = x / PALETTE_WIDTH
    for y in range(HUE_HEIGHT):
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        r, g, b = int(r*255), int(g*255), int(b*255)
        palette_image.put("#%02x%02x%02x" % (r, g, b), (x, y))

# Fill the saturation/value square below
for x in range(SQUARE_SIZE):
    sat = x / SQUARE_SIZE
    for y in range(SQUARE_SIZE):
        val = 1.0 - (y / SQUARE_SIZE)
        # Use the current hue
        r, g, b = colorsys.hsv_to_rgb(current_hue, sat, val)
        r, g, b = int(r*255), int(g*255), int(b*255)
        palette_image.put("#%02x%02x%02x" % (r, g, b), (x + (PALETTE_WIDTH - SQUARE_SIZE) // 2, y + HUE_HEIGHT))

canvas = tk.Canvas(root, width=PALETTE_WIDTH, height=PALETTE_HEIGHT)
canvas.pack(pady=10)

canvas.create_image((0, 0), image=palette_image, anchor=tk.NW)
canvas.bind("<Button-1>", on_canvas_click)

# Color preview area
preview_canvas = tk.Canvas(root, width=100, height=50, bg="#ffffff", highlightthickness=1, highlightbackground="black")
preview_canvas.pack(pady=5)

rgb_label = tk.Label(root, text="RGB: ")
rgb_label.pack(pady=5)

hex_label = tk.Label(root, text="Hex: ")
hex_label.pack(pady=5)

# Save button
save_button = tk.Button(root, text="Save", command=save_color)
save_button.pack(pady=5)

# Note entry field
note_label = tk.Label(root, text="Add a note (optional):")
note_label.pack(pady=(5, 0))

note_entry = tk.Entry(root, width=40)
note_entry.pack(pady=(0, 5))

# Export button
export_button = tk.Button(root, text="Export Colors", command=export_colors)
export_button.pack(pady=5)

# History label
history_title = tk.Label(root, text="Saved Colors:")
history_title.pack(pady=(10, 0))

# Frame to hold the history of saved colors
history_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
history_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)

# State
current_color = None
color_history = []

root.mainloop()



