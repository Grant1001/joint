

# joint

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20arm64-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

A computer vision tool that tracks arm joint angles and estimates biomechanical stress in real-time.

## 🚀 Getting Started

### Prerequisites
* **OS:** Windows 11 (ARM64/x64)
* **Python:** 3.13+
* **Webcam**

### Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/Grant1001/joint.git](https://github.com/Grant1001/joint.git)
    cd joint
    ```

2.  Install dependencies:
    ```bash
    pip install opencv-python mediapipe numpy
    ```

## 🎮 How to Use

1.  Run the tracker:
    ```bash
    python joint_tracker.py
    ```

2.  **Position yourself:** Ensure the camera can see your **Left Arm**.
3.  **Visual Feedback:**
    * **🟩 Green:** Low Stress (Safe)
    * **🟨 Yellow:** Medium Stress (Warning)
    * **🟥 Red:** High Stress (Hyperextension/Flexion)

4.  Press **`q`** to quit.

## 🛠️ Built With
* [MediaPipe](https://developers.google.com/mediapipe) - Skeletal tracking
* [OpenCV](https://opencv.org/) - Computer vision