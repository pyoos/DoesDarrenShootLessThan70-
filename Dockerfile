# Use Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies for OpenCV (minimal set)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set environment variables for headless operation
ENV OPENCV_IO_ENABLE_OPENEXR=0
ENV OPENCV_IO_ENABLE_JASPER=0
ENV QT_QPA_PLATFORM=offscreen
ENV DISPLAY=
ENV OPENCV_VIDEOIO_PRIORITY_MSMF=0
ENV OPENCV_VIDEOIO_DEBUG=0
ENV MPLBACKEND=Agg

# Copy webapp directory
COPY webapp/ ./webapp/

# Change to webapp directory and install dependencies
WORKDIR /app/webapp

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir opencv-python-headless==4.8.1.78 && \
    pip install --no-cache-dir -r requirements.txt

# Copy trained model if it exists
COPY trainon10kdataset/ ./trainon10kdataset/

# Expose port
EXPOSE 5000

# Set the default command
CMD ["python", "app.py"] 