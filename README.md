1. Project Overview

This project delivers a standalone desktop application designed to help students intuitively understand lossy image compression. By allowing users to upload an image, select a compression format (JPEG, WebP, or GIF), and adjust a quality/color parameter via a slider, the tool provides an immediate side-by-side visual comparison of the original and compressed images, along with file size statistics.

The final deliverable is a single, portable .exe file that runs instantly on any Windows computer without requiring Python or any additional software—ideal for classroom demonstrations and student self-exploration.

2. Key Features

- Image Upload: Supports common formats: PNG, JPEG, BMP, TIFF.
- Format Selection: Choose between JPEG (classic DCT-based), WebP (modern predictive coding), or GIF (palette quantization).
- Parameter Adjustment: For JPEG/WebP: quality slider (1–100). For GIF: color count slider (2–256).
- Real‑time Preview: Side-by-side display updates instantly when the slider is moved.
- File Size Comparison: Shows original vs. compressed size and percentage reduction.
- Portable Executable: Packaged as a single .exe (approx. 20 MB) that launches in seconds.

3. Technical Implementation

- GUI Framework: tkinter – Python's built-in library, chosen for its simplicity and packaging reliability.
- Image Processing: Pillow (PIL fork) for reading, converting, and compressing images.
- Packaging Tool: Nuitka – compiles Python code into a native Windows executable, resulting in a smaller file size and faster startup compared to PyInstaller.
