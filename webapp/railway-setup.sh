#!/bin/bash

# Railway setup script for DDS70 Basketball Detection
echo "🏀 Setting up DDS70 Basketball Detection for Railway..."

# Set environment variables for headless OpenCV operation
export OPENCV_IO_ENABLE_OPENEXR=0
export OPENCV_IO_ENABLE_JASPER=0
export QT_QPA_PLATFORM=offscreen
export DISPLAY=
export OPENCV_VIDEOIO_PRIORITY_MSMF=0
export OPENCV_VIDEOIO_DEBUG=0
export MPLBACKEND=Agg

# Install OpenCV headless first to avoid conflicts
echo "📦 Installing OpenCV headless..."
pip install --no-cache-dir opencv-python-headless==4.8.1.78

# Install other dependencies
echo "📦 Installing other dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "✅ Setup complete! Starting application..."
python app.py 