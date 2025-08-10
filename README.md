# 🏀 DDS70 - Basketball Object Detection System

A comprehensive basketball analytics project using computer vision and object detection to analyze basketball performance and player movements.

## 🚀 Quick Start

### Option 1: Web Interface (Recommended for Demos)
```bash
# Install dependencies
pip install -r requirements.txt

# Start the web server
python app.py

# Open browser to http://localhost:8080
```

### Option 2: Real-time Webcam Demo
```bash
# Install dependencies
pip install -r requirements.txt

# Run webcam demo
python demo.py
```

## 📁 Project Structure

### Core Applications
- **`app.py`** - Modern Flask web application for image upload and detection
- **`demo.py`** - Real-time webcam detection demo (perfect for interviews)
- **`index.html`** - Beautiful, responsive web interface with drag-and-drop
- **`requirements.txt`** - All project dependencies

### Research & Development
- **`quickstart.ipynb`** - Google Drive API setup and authentication
- **`googledrive.ipynb`** - Complete Google Drive integration for data management
- **`kaggle1.ipynb`** - NBA tracking implementation based on YOLOv8
- **`real_time_tracking.ipynb`** - Webcam object detection experiments
- **`object_detector.ipynb`** - Original Flask backend development
- **`sandbox.ipynb`** - Initial model training experiments with Roboflow

### Model & Training Results
- **`trainon10kdataset/`** - Custom YOLOv8 model trained on basketball dataset
  - **Performance**: 74.1% mAP50-95 on validation set
  - **Classes**: Basketball courts, ball, made shots, person, rim, shoot
  - **Dataset**: 10k images from [Roboflow](https://universe.roboflow.com/test-datset/player_detect-0spfb/dataset/1#)

## 🛠️ Technical Stack

- **Object Detection**: YOLOv8 (Nano, Small, Medium variants)
- **Computer Vision**: OpenCV for real-time processing
- **Web Framework**: Flask with Waitress server
- **Frontend**: Modern HTML5/CSS3/JavaScript with drag-and-drop
- **Dataset Management**: Roboflow (10k image limit)
- **Data Storage**: Google Drive API integration
- **Languages**: Python, JavaScript, HTML/CSS

## ✅ Features Implemented

- [x] **Real-time object detection** via webcam
- [x] **Custom model training** on basketball-specific datasets  
- [x] **Web interface** for image upload and analysis
- [x] **Google Drive integration** for data management
- [x] **Video processing** capabilities (MP4 to GIF conversion)
- [x] **Professional UI/UX** with modern design
- [x] **Model performance metrics** and visualizations

## 🎯 Future Enhancements

- [ ] **Advanced video analysis** with shot tracking
- [ ] **iOS/Mobile app** integration
- [ ] **LLM integration** for analysis and feedback
- [ ] **Player performance statistics**
- [ ] **Shot accuracy analytics**

## 🎬 Demo Instructions

### For Interviews/Presentations:

1. **Quick Web Demo**: Run `python app.py` and show image upload
2. **Real-time Demo**: Run `python demo.py` and point camera at basketball content
3. **Show Training Results**: Display the model performance graphs in `trainon10kdataset/`

## 📊 Model Performance

- **Model**: YOLOv8n custom trained
- **Training**: 25 epochs on 10k basketball images
- **Final Performance**: 74.1% mAP50-95
- **Classes Detected**: Basketball courts, balls, players, rims, shots
