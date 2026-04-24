# app.py - Lossy Compression Demo (Tkinter Version)
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import io

class ImageCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lossy Compression Visualization")
        self.root.geometry("900x550")

        self.original_image = None
        self.compressed_image = None

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left control panel
        control_frame = tk.Frame(main_frame, width=250)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.pack_propagate(False)

        tk.Button(control_frame, text="1. Select Image", command=self.select_image, height=2).pack(fill=tk.X, pady=(0, 10))

        tk.Label(control_frame, text="2. Compression Format:").pack(anchor=tk.W)
        self.format_var = tk.StringVar(value="JPEG")
        format_options = ["JPEG", "WebP", "GIF"]
        format_menu = ttk.Combobox(control_frame, textvariable=self.format_var, values=format_options, state="readonly")
        format_menu.pack(fill=tk.X, pady=(0, 10))
        format_menu.bind("<<ComboboxSelected>>", self.on_format_change)

        tk.Label(control_frame, text="3. Compression Parameter:").pack(anchor=tk.W)
        self.slider_label = tk.Label(control_frame, text="Quality (JPEG/WebP)")
        self.slider_label.pack(anchor=tk.W)
        self.param_slider = tk.Scale(control_frame, from_=1, to=100, orient=tk.HORIZONTAL, command=self.update_compressed_image)
        self.param_slider.set(80)
        self.param_slider.pack(fill=tk.X, pady=(0, 10))


        self.info_text = tk.StringVar()
        tk.Label(control_frame, textvariable=self.info_text, fg="blue", justify=tk.LEFT).pack(fill=tk.X)

        # Right display panel
        display_frame = tk.Frame(main_frame)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(display_frame, text="No image selected", bg="#f0f0f0")
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.on_format_change()

    def on_format_change(self, event=None):
        fmt = self.format_var.get()
        if fmt in ["JPEG", "WebP"]:
            self.param_slider.config(from_=1, to=100)
            self.param_slider.set(80)
            self.slider_label.config(text="Quality (JPEG/WebP)")
        elif fmt == "GIF":
            self.param_slider.config(from_=2, to=256)
            self.param_slider.set(128)
            self.slider_label.config(text="Number of Colors (GIF)")
        self.update_compressed_image()

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.update_compressed_image()

    def compress_image(self, img, fmt, param):
        buffer = io.BytesIO()
        if fmt == 'GIF':
            img_rgb = img.convert('RGB')
            img_quantized = img_rgb.quantize(colors=param)
            img_quantized.save(buffer, format='GIF', optimize=True)
            compressed = Image.open(buffer)
            size = buffer.tell()
            return compressed, size
        else:
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            if fmt == 'JPEG':
                img.save(buffer, format='JPEG', quality=param)
            elif fmt == 'WebP':
                img.save(buffer, format='WebP', quality=param)
            size = buffer.tell()
            buffer.seek(0)
            compressed = Image.open(buffer)
            return compressed, size

    def update_compressed_image(self, event=None):
        if self.original_image is None:
            self.image_label.config(image='', text="No image selected")
            self.info_text.set("")
            return

        fmt = self.format_var.get()
        param = self.param_slider.get()

        try:
            self.compressed_image, compressed_size = self.compress_image(self.original_image, fmt, param)

            img_bytes = io.BytesIO()
            self.original_image.save(img_bytes, format='PNG')
            original_size = img_bytes.tell()

            compression_ratio = (1 - compressed_size / original_size) * 100
            info_str = f"Original: {original_size / 1024:.1f} KB\n"
            info_str += f"Compressed: {compressed_size / 1024:.1f} KB\n"
            info_str += f"Reduction: {compression_ratio:.1f}%"
            self.info_text.set(info_str)

            self.display_side_by_side(self.original_image, self.compressed_image)

        except Exception as e:
            self.image_label.config(image='', text=f"Compression Error: {e}")

    def display_side_by_side(self, img1, img2):
        label_width = self.image_label.winfo_width()
        label_height = self.image_label.winfo_height()

        if label_width <= 1:
            label_width = 600
        if label_height <= 1:
            label_height = 400

        single_img_width = (label_width - 30) // 2
        single_img_height = label_height - 40

        img1_resized = self.resize_image(img1, single_img_width, single_img_height)
        img2_resized = self.resize_image(img2, single_img_width, single_img_height)

        combined_img = Image.new('RGB', (label_width, label_height), color='#f0f0f0')
        combined_img.paste(img1_resized, (10, 20))
        combined_img.paste(img2_resized, (single_img_width + 20, 20))

        self.tk_image = ImageTk.PhotoImage(combined_img)
        self.image_label.config(image=self.tk_image, text="")

    def resize_image(self, img, max_width, max_height):
        img_copy = img.copy()
        img_copy.thumbnail((max_width, max_height), Image.LANCZOS)
        return img_copy

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCompressorApp(root)
    root.mainloop()