import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw
import pandas as pd

# Глобальные переменные
canvas = None
tk_image = None
image = None
display_image = None
img_draw = None
clicks = []
original_size = None
color = "blue"
rad = 3

# Словарь с информацией о каждом цвете
color_info = {
    "blue": {"name": "Obj_1", "count": 0},
    "red": {"name": "Obj_2", "count": 0},
    "green": {"name": "Obj_3", "count": 0},
    "yellow": {"name": "Obj_4", "count": 0},
    "purple": {"name": "Obj_5", "count": 0},
    "lightseagreen": {"name": "Obj_6", "count": 0},
    "pink": {"name": "Obj_7", "count": 0},
}


def load_image():
    global canvas, tk_image, image, img_draw, original_size, display_image, color_info

    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if file_path:
        image = Image.open(file_path)
        img_draw = ImageDraw.Draw(image)

        original_size = image.size

        display_image = image.copy()

        display_image.thumbnail((700, 700))
        tk_image = ImageTk.PhotoImage(display_image)

        canvas.config(width=display_image.width, height=display_image.height)
        canvas.delete("all")

        # Очистка значений словаря после загрузки нового значения
        for color in color_info:
            color_info[color]["count"] = 0

        color_count_label.config(
            text="\n".join(
                [
                    f"{color_info[color]['name']} ({color}): {color_info[color]['count']}"
                    for color in color_info
                ]
            )
        )
        # Очистка значений label
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

        canvas.bind("<Button-1>", click_event)


def set_color(event):
    global color
    color = color_combobox.get()


def click_event(event):
    global clicks, image, img_draw, original_size, display_image, rad

    clicks.append((event.x, event.y))

    canvas.create_oval(
        event.x - rad, event.y - rad, event.x + rad, event.y + rad, fill=color
    )

    scale = original_size[0] / display_image.width
    real_x = int(event.x * scale)
    real_y = int(event.y * scale)

    img_draw.ellipse(
        (
            real_x - rad * scale,
            real_y - rad * scale,
            real_x + rad * scale,
            real_y + rad * scale,
        ),
        fill=color,
        outline="black",
    )
    color_info[color]["count"] += 1
    color_count_label.config(
        text="\n".join(
            [
                f"{color_info[color]['name']} ({color}): {color_info[color]['count']}"
                for color in color_info
            ]
        )
    )


def save_image():
    global image
    save_path = filedialog.asksaveasfilename(
        defaultextension=".png", filetypes=[("PNG files", "*.png")]
    )
    if save_path:
        image.save(save_path)


def save_counts_to_excel():
    df = pd.DataFrame(
        [
            (color_info[color]["name"], color_info[color]["count"])
            for color in color_info
        ],
        columns=["Name", "Count"],
    )
    save_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
    )
    if save_path:
        df.to_excel(save_path, index=False)
        print(f"Counts saved to {save_path}")


# Окно программы
root = tk.Tk()
root.title("Image Editor")

# Фрейм для трех кнопок
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP)

load_button = tk.Button(button_frame, text="Load Image", command=load_image)
load_button.pack(side=tk.LEFT)

save_button = tk.Button(button_frame, text="Save Image", command=save_image)
save_button.pack(side=tk.LEFT)

save_counts_button = tk.Button(
    button_frame, text="Save counts to Excel", command=save_counts_to_excel
)
save_counts_button.pack(side=tk.LEFT)

# Полотно для сжатого изображения
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, padx=10, pady=10)

# Фрейм для количества кликов и комбобокса
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT, padx=5, pady=5)

color_count_label = tk.Label(
    right_frame,
    text="\n".join(
        [f"{color_info[color]['name']} ({color}): 0" for color in color_info]
    ),
    justify=tk.LEFT,
)
color_count_label.pack(side=tk.LEFT)

color_combobox = ttk.Combobox(right_frame, values=list(color_info.keys()), height=7)
color_combobox.current(0)
color_combobox.bind("<<ComboboxSelected>>", set_color)
color_combobox.pack(side=tk.LEFT, padx=5)

root.mainloop()
