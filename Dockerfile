# Use Python 3.11 slim image
FROM python:3.11-slim

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
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
ENV LIBGL_ALWAYS_SOFTWARE=1

# Copy application files
COPY webapp/ ./webapp/
COPY trainon10kdataset/ ./trainon10kdataset/

# Set working directory to webapp
WORKDIR /app/webapp

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir opencv-python-headless==4.8.1.78 && \
    pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"] 