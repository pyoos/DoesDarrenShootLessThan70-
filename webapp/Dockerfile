# Use Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies for OpenCV and YOLO
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libfontconfig1 \
    libglu1-mesa \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxcursor1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxinerama1 \
    libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set environment variables for headless operation
ENV OPENCV_IO_ENABLE_OPENEXR=0
ENV OPENCV_IO_ENABLE_JASPER=0
ENV QT_QPA_PLATFORM=offscreen
ENV DISPLAY=:99
ENV OPENCV_VIDEOIO_PRIORITY_MSMF=0
ENV OPENCV_VIDEOIO_DEBUG=0
ENV MPLBACKEND=Agg
ENV PYTHONUNBUFFERED=1

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir opencv-python-headless==4.8.1.78 && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set the default command
CMD ["python", "app.py"] 