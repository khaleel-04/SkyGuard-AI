import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ultralytics import YOLO
import cv2
import os
from PIL import Image, ImageTk
import numpy as np

# ------------------------- CONFIG -------------------------

# Path to your trained YOLO weights (update this to your new 5-class model if needed)
MODEL_PATH = r"C:\Users\rayya\OneDrive\Desktop\drone_final\runs\detect\train3\weights\best.pt"

# Path to your SKYGUARD AI logo image (PNG/JPG)
LOGO_PATH = r"C:\Users\rayya\OneDrive\Desktop\drone_final\assets\banner.png"  # <-- your logo
LOGO_MAX_HEIGHT = 80  # increase this to make logo larger (e.g., 90, 100)

# ---------------------------------------------------------

# Global variables
model = None
detection_thread = None
stop_detection_flag = False
current_tk_image = None  # to keep reference of displayed image in Image tab


def load_model():
    """Load YOLO model once, when the app starts."""
    global model
    try:
        model = YOLO(MODEL_PATH)
        print("Model loaded successfully.")
    except Exception as e:
        print("Error loading model:", e)
        messagebox.showerror("Error", f"Failed to load model:\n{e}")


def run_detection(source, window_title="SKYGUARD AI - Detection"):
    """
    Run YOLO detection on the given source.
    source can be:
        - 0 for webcam
        - video file path for video
    """
    global stop_detection_flag, model

    if model is None:
        messagebox.showerror("Error", "Model not loaded.")
        return

    stop_detection_flag = False

    try:
        # stream=True to avoid RAM accumulation
        results = model.predict(source=source, conf=0.5, show=False, stream=True)

        for r in results:
            if stop_detection_flag:
                break

            # Get annotated frame
            annotated_frame = r.plot()

            # Show frame in OpenCV window
            cv2.imshow(window_title, annotated_frame)

            # Press 'q' in the OpenCV window to quit as well
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print("Error during detection:", e)
        messagebox.showerror("Error", f"Detection error:\n{e}")
    finally:
        cv2.destroyAllWindows()
        print("Detection stopped.")


def start_thread_for_detection(source, title):
    """
    Start detection in a separate thread so that Tkinter UI doesn't freeze.
    """
    global detection_thread

    if detection_thread is not None and detection_thread.is_alive():
        messagebox.showinfo("Info", "Detection is already running.")
        return

    detection_thread = threading.Thread(
        target=run_detection,
        args=(source, title),
        daemon=True
    )
    detection_thread.start()


def start_webcam_detection():
    """Callback for Webcam Detection button."""
    start_thread_for_detection(0, "SKYGUARD AI - Webcam Detection")


def start_video_detection():
    """Callback for Video Detection button: open file dialog and run detection."""
    video_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All Files", "*.*")]
    )

    if not video_path:
        return  # User cancelled

    if not os.path.isfile(video_path):
        messagebox.showerror("Error", "Selected video file does not exist.")
        return

    start_thread_for_detection(video_path, "SKYGUARD AI - Video Detection")


def stop_detection():
    """Set flag to stop detection loop."""
    global stop_detection_flag
    stop_detection_flag = True
    print("Stop signal sent to detection thread.")


def detect_on_image():
    """
    Open file dialog, run detection on a single image,
    and display the annotated result inside the Tkinter window.
    """
    global model, current_tk_image

    if model is None:
        messagebox.showerror("Error", "Model not loaded.")
        return

    img_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp"), ("All Files", "*.*")]
    )

    if not img_path:
        return  # user cancelled

    if not os.path.isfile(img_path):
        messagebox.showerror("Error", "Selected image file does not exist.")
        return

    try:
        # Predict on the image
        results = model.predict(source=img_path, conf=0.5, show=False)
        r = results[0]

        # Annotated image (BGR)
        annotated_frame = r.plot()

        # Convert BGR to RGB for PIL
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

        # Convert to PIL image and resize to fit nicely
        pil_img = Image.fromarray(annotated_frame)
        pil_img.thumbnail((500, 400))  # keep aspect ratio

        current_tk_image = ImageTk.PhotoImage(pil_img)
        image_display_label.config(image=current_tk_image)
        image_display_label.image = current_tk_image

        # Prepare detection summary text
        classes = r.boxes.cls.cpu().numpy() if r.boxes is not None else []
        scores = r.boxes.conf.cpu().numpy() if r.boxes is not None else []

        if len(classes) == 0:
            detected_text = "No objects detected."
        else:
            detected_text = "Detections:\n"
            names = model.names  # class names dict
            # Count per class
            class_counts = {}

            for c, s in zip(classes, scores):
                class_id = int(c)
                class_name = names.get(class_id, str(class_id))
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
                detected_text += f"- {class_name} ({s*100:.1f}% confidence)\n"

            detected_text += "\nSummary:\n"
            for cname, cnt in class_counts.items():
                detected_text += f"  • {cname}: {cnt}\n"

        detection_result_var.set(detected_text)

    except Exception as e:
        print("Error during image detection:", e)
        messagebox.showerror("Error", f"Image detection error:\n{e}")


def on_close():
    """Handle app closing: stop detection and destroy window."""
    global stop_detection_flag
    stop_detection_flag = True
    cv2.destroyAllWindows()
    root.destroy()


# ------------------------- TKINTER UI -------------------------

root = tk.Tk()
root.title("SKYGUARD AI - Air / Drone Detection (YOLOv8)")

# Slightly bigger window for image tab
root.geometry("780x540")
root.resizable(False, False)
root.configure(bg="#141414")

style = ttk.Style()
style.theme_use("clam")

# Notebook (tabs) styling
style.configure("TNotebook", background="#141414", borderwidth=0)
style.configure("TNotebook.Tab", padding=[10, 5], font=("Segoe UI", 10, "bold"))
style.map("TNotebook.Tab", background=[("selected", "#2b2b2b")])

# Frames styling
frame_bg = "#1f1f1f"
text_fg = "#ffffff"
accent_color = "#00bcd4"

# ---------- Header ----------
header_frame = tk.Frame(root, bg="#141414")
header_frame.pack(fill="x", pady=(8, 4), padx=5)

# Try to load logo if LOGO_PATH is set
if LOGO_PATH and os.path.isfile(LOGO_PATH):
    try:
        logo_img = Image.open(LOGO_PATH).convert("RGBA")
        w, h = logo_img.size

        # keep aspect ratio, limit by LOGO_MAX_HEIGHT
        scale = LOGO_MAX_HEIGHT / float(h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        logo_img = logo_img.resize((new_w, new_h), Image.LANCZOS)

        # add a subtle dark background + padding so logo is clearer
        pad = 8
        bg_w, bg_h = new_w + 2 * pad, new_h + 2 * pad
        bg = Image.new("RGBA", (bg_w, bg_h), (20, 20, 20, 255))
        bg.paste(logo_img, (pad, pad), logo_img)
        logo_img = bg

        logo_tk = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(header_frame, image=logo_tk, bg="#141414")
        logo_label.image = logo_tk
        logo_label.pack(side="left", padx=(8, 16), pady=4)
    except Exception as e:
        print("Error loading logo:", e)

title_subframe = tk.Frame(header_frame, bg="#141414")
title_subframe.pack(side="left", padx=5)

title_label = tk.Label(
    title_subframe,
    text="SKYGUARD AI",
    font=("Segoe UI", 24, "bold"),
    fg=accent_color,
    bg="#141414"
)
title_label.pack(anchor="w")

subtitle_label = tk.Label(
    title_subframe,
    text="Real-Time Air / Drone / Helicopter / Jet / Bird Detection (YOLOv8)",
    font=("Segoe UI", 10),
    fg="#cccccc",
    bg="#141414"
)
subtitle_label.pack(anchor="w")

# Notebook
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# ---------------- Webcam Tab ----------------
webcam_frame = tk.Frame(notebook, bg=frame_bg)
notebook.add(webcam_frame, text="Webcam")

webcam_info = tk.Label(
    webcam_frame,
    text="Use your device's webcam for live SKYGUARD AI detection.",
    font=("Segoe UI", 10),
    fg=text_fg,
    bg=frame_bg
)
webcam_info.pack(pady=20)

btn_webcam = tk.Button(
    webcam_frame,
    text="Start Webcam Detection",
    font=("Segoe UI", 12, "bold"),
    command=start_webcam_detection,
    width=25,
    bg=accent_color,
    fg="black",
    relief="flat",
    activebackground="#06a5bb"
)
btn_webcam.pack(pady=10)

btn_stop1 = tk.Button(
    webcam_frame,
    text="Stop Detection",
    font=("Segoe UI", 11),
    command=stop_detection,
    width=20,
    bg="#444444",
    fg="white",
    relief="flat",
    activebackground="#555555"
)
btn_stop1.pack(pady=5)

# ---------------- Video Tab ----------------
video_frame = tk.Frame(notebook, bg=frame_bg)
notebook.add(video_frame, text="Video")

video_info = tk.Label(
    video_frame,
    text="Select a video file (.mp4, .avi, etc.) to run SKYGUARD AI detection.",
    font=("Segoe UI", 10),
    fg=text_fg,
    bg=frame_bg
)
video_info.pack(pady=20)

btn_video = tk.Button(
    video_frame,
    text="Select Video & Detect",
    font=("Segoe UI", 12, "bold"),
    command=start_video_detection,
    width=25,
    bg=accent_color,
    fg="black",
    relief="flat",
    activebackground="#06a5bb"
)
btn_video.pack(pady=10)

btn_stop2 = tk.Button(
    video_frame,
    text="Stop Detection",
    font=("Segoe UI", 11),
    command=stop_detection,
    width=20,
    bg="#444444",
    fg="white",
    relief="flat",
    activebackground="#555555"
)
btn_stop2.pack(pady=5)

# ---------------- Image Tab ----------------
image_frame = tk.Frame(notebook, bg=frame_bg)
notebook.add(image_frame, text="Image")

image_info = tk.Label(
    image_frame,
    text="Upload an image to detect airplanes / drones / helicopters / jets / birds.",
    font=("Segoe UI", 10),
    fg=text_fg,
    bg=frame_bg
)
image_info.pack(pady=10)

btn_select_image = tk.Button(
    image_frame,
    text="Select Image & Detect",
    font=("Segoe UI", 10, "bold"),
    command=detect_on_image,
    bg=accent_color,
    fg="black",
    relief="flat",
    activebackground="#06a5bb"
)
btn_select_image.pack(pady=5)

# Image display area
image_display_label = tk.Label(image_frame, bg=frame_bg)
image_display_label.pack(pady=10)

# Detection result text
detection_result_var = tk.StringVar(value="No image selected.")
result_label = tk.Label(
    image_frame,
    textvariable=detection_result_var,
    justify="center",
    font=("Segoe UI", 11),
    fg=text_fg,
    bg=frame_bg
)
result_label.pack(pady=5)

# When closing the window
root.protocol("WM_DELETE_WINDOW", on_close)

# Load the model once at start
load_model()

# Start the Tkinter loop
root.mainloop()
