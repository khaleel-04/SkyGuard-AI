<p align="center">
  <img src="assets/banner.png" width="900">
</p>

<h1 align="center">🚁 SKYGUARD AI</h1>

<h3 align="center">
Real-Time Aerial Object Detection & Monitoring using YOLOv8
</h3>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red)
![Computer Vision](https://img.shields.io/badge/Computer-Vision-green)
![OpenCV](https://img.shields.io/badge/OpenCV-blue?logo=opencv)
![Deep Learning](https://img.shields.io/badge/Deep-Learning-orange)
![MIT License](https://img.shields.io/badge/License-MIT-yellow)

</p>

---

# 📌 Project Overview

**SKYGUARD AI** is an AI-powered real-time aerial object detection and monitoring system built using **YOLOv8** and **Computer Vision**.

The application detects and classifies aerial objects from **live webcam feeds, images, and videos** into multiple categories including **Drone, Airplane, Helicopter, Jet, and Bird**.

The project was developed during an AI internship to demonstrate the practical application of **Deep Learning, Computer Vision, and Real-Time Object Detection** for intelligent airspace monitoring.

---

# 🎯 Objectives

* Detect aerial objects in real time.
* Improve intelligent airspace monitoring.
* Distinguish drones and aircraft from birds.
* Reduce false detections using a custom dataset.
* Demonstrate practical implementation of YOLOv8 for Computer Vision applications.

---

# ✨ Features

* 🚁 Drone Detection
* ✈️ Airplane Detection
* 🚁 Helicopter Detection
* 🛩️ Jet Detection
* 🐦 Bird Detection
* 🎥 Live Webcam Detection
* 🖼️ Image Detection
* 🎬 Video Detection
* 📦 YOLOv8 Object Detection
* 📊 Bounding Box Visualization
* ⚡ Real-Time Inference
* 🎯 High Detection Accuracy

---

# 🧠 AI Model

| Component            | Technology  |
| -------------------- | ----------- |
| Object Detection     | YOLOv8      |
| Framework            | Ultralytics |
| Computer Vision      | OpenCV      |
| Programming Language | Python      |

---

# 📊 Custom Dataset

Unlike many object detection projects that rely solely on publicly available datasets, **SKYGUARD AI** was trained using a custom-built dataset created by combining multiple image sources.

## Detection Classes

* ✈️ Airplane
* 🚁 Helicopter
* 🚁 Drone
* 🛩️ Jet
* 🐦 Bird

## Dataset Highlights

* Custom toy airplane images
* Custom toy helicopter images
* Custom toy drone images
* Jet aircraft images
* Real bird images included as a negative class
* Manual annotation using YOLO format
* Dataset organized into Train, Validation and Test sets

The inclusion of bird images improves the model's ability to distinguish drones and aircraft from naturally occurring flying objects, thereby reducing false positives.

---

# 🛠 Technologies Used

* Python
* YOLOv8 (Ultralytics)
* OpenCV
* NumPy
* Pandas
* Matplotlib
* Streamlit

---

# 🏗️ System Architecture

The SKYGUARD AI detection pipeline consists of four major layers:

* Input Layer
* Preprocessing Layer
* Detection & Intelligence Layer
* Output Layer

<p align="center">
<img src="assets/architecture.png" width="700">
</p>

---

# 🔄 Project Workflow

The overall workflow followed during project development.

<p align="center">
<img src="assets/workflow.png" width="550">
</p>

---

# ⚙️ Methodology

The project implementation followed a structured five-phase development process.

<p align="center">
<img src="assets/methodology.png" width="500">
</p>

---

# 📊 Model Performance

### Confusion Matrix

<p align="center">
<img src="assets/confusion_matrix.png" width="700">
</p>

### Precision-Confidence Curve

<p align="center">
<img src="assets/precision_curve.png" width="700">
</p>

---

# 🎯 Detection Results

### 🚁 Drone Detection

<p align="center">
<img src="assets/drone_detection.png" width="850">
</p>

---

### ✈️ Airplane Detection

<p align="center">
<img src="assets/airplane_detection.png" width="850">
</p>

---

### 🚁 Helicopter Detection

<p align="center">
<img src="assets/helicopter_detection.png" width="850">
</p>

---

# 📂 Project Structure

```text
skyguard-ai-yolov8/
│
├── app.py
├── data.yaml
├── README.md
├── requirements.txt
├── .gitignore
│
├── assets/
│   ├── banner.png
│   ├── workflow.png
│   ├── architecture.png
│   ├── methodology.png
│   ├── confusion_matrix.png
│   ├── precision_curve.png
│   ├── drone_detection.png
│   ├── airplane_detection.png
│   └── helicopter_detection.png
│
├── notebooks/
│   └── drone.ipynb
│
├── dataset/        (Ignored in Git)
├── runs/           (Ignored in Git)
└── yolov8n.pt      (Ignored in Git)
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/RayyanAhamed05/skyguard-ai-yolov8.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

# 📈 Training Summary

* YOLOv8n Pre-trained Model
* Transfer Learning
* Custom Dataset
* Data Augmentation
* Real-Time Object Detection
* Live Webcam Integration

---

# 🚀 Future Enhancements

* Night Vision Detection
* Infrared Camera Support
* Drone Tracking
* Multiple Object Tracking
* Edge AI Deployment
* CCTV Camera Integration
* Threat Alert System
* Cloud-Based Monitoring Dashboard

---

# 👨‍💻 Author

**Rayyan Ahamed**

Computer Science & Engineering Graduate

Artificial Intelligence • Machine Learning • Computer Vision

---

# ⭐ Acknowledgement

This project was developed as part of an AI internship to demonstrate the practical application of **Computer Vision, Deep Learning, and YOLOv8** for intelligent aerial object detection and monitoring.
