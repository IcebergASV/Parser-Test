# Camera Topic ROS2 Bag Parser Script 

## Overview
This script is designed to parse data from ROS2 bags containing webcam data and store the images in PNG format. It extracts the image data from raw messages published on the `/camera/camera/color/image_raw` topic in the bag files, converts the data to images, and saves them as PNG files in a specified directory.

## System Requirements

### Dependencies:
- **Operating System**:
  - Python 3.x
  - OpenCV (for image manipulation and saving)
  - SQLite3 (for database interactions)
  
- **ROS2 Dependencies**:
  - `rosidl_runtime_py` (for ROS2 message handling)
  - `rclpy` (ROS2 Python client library)

- **Other Libraries**:
  - `numpy` (for data array manipulation)

### Installation

To run the script, you need to have the following Python libraries installed:
1. `opencv-python`
2. `sqlite3` (comes pre-installed with Python)
3. `numpy`
4. ROS2 installed (for ROS2 related dependencies)

You can install missing dependencies with pip:
```bash
pip install opencv-python numpy

## Usage
### Initial Setup
Before running the script, make sure you have a directory with `.db3` files (ROS2 bag data) that contain the `/camera/camera/color/image_raw` topic. The script will process these files to extract images.

* **Note: Ensure that the path to the ROS2 bag file and the topic /camera/camera/color/image_raw are correctly specified in the script. If your data is located elsewhere or uses a different topic, you will need to update the relevant path and topic name.**
