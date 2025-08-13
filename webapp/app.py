"""
Basketball Object Detection Web Application
DDS70 Project - Flask Backend for Railway Deployment
"""

from ultralytics import YOLO
from flask import Flask, request, Response, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS for website integration
CORS(app, origins=[
    "https://pyoo.info",
    "https://www.pyoo.info", 
    "http://localhost:3000",  # For local development
    "http://localhost:8080",
    "https://*.railway.app",  # Railway deployments
    "https://*.up.railway.app"
])

# Global model variable
model = None

def load_model():
    """Load the YOLO model with error handling"""
    global model
    try:
        # Try to load custom trained model first
        model_path = "trainon10kdataset/weights/best.pt"
        if os.path.exists(model_path):
            model = YOLO(model_path)
            logger.info(f"Loaded custom basketball model from {model_path}")
            logger.info(f"Model classes: {list(model.names.values())}")
            return True
        else:
            # Fallback to pre-trained model
            model = YOLO("yolov8n.pt")
            logger.info("Loaded pre-trained YOLOv8n model")
            logger.info(f"Model classes: {list(model.names.values())}")
            return True
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

@app.route("/")
def root():
    """Serve the main page"""
    return jsonify({
        "message": "Basketball Detection API",
        "status": "running",
        "endpoints": ["/api/detect", "/api/model-info", "/health"]
    })

@app.route("/api/detect", methods=["POST"])
def detect():
    """
    Handler for /api/detect POST endpoint
    Receives uploaded file, processes through YOLO detection
    and returns detection results in the format expected by the React frontend
    """
    if not model:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        # Process the image
        image = Image.open(file.stream)
        results = detect_objects_on_image(image)
        
        return jsonify(results)
    
    except Exception as e:
        logger.error(f"Error in detect endpoint: {e}")
        return jsonify({"error": f"Detection failed: {str(e)}"}), 500

def detect_objects_on_image(image):
    """
    Function receives an image,
    passes it through YOLO neural network
    and returns detection results in the format expected by React frontend
    """
    try:
        import time
        start_time = time.time()
        
        results = model.predict(image, conf=0.25)  # Lower confidence threshold
        result = results[0]
        
        detections = []
        for box in result.boxes:
            x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
            class_id = box.cls[0].item()
            confidence = round(box.conf[0].item(), 2)
            class_name = result.names[class_id]
            
            detections.append({
                "class": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2]
            })
        
        processing_time = round(time.time() - start_time, 2)
        
        # Return in the format expected by React frontend
        return {
            "detections": detections,
            "processing_time": f"{processing_time}s",
            "total_objects": len(detections),
            "model_used": "YOLOv8 Custom Basketball Model",
            "image_size": {"width": image.width, "height": image.height}
        }
    
    except Exception as e:
        logger.error(f"Error in object detection: {e}")
        return {
            "detections": [],
            "processing_time": "0s",
            "total_objects": 0,
            "error": str(e)
        }

@app.route("/api/model-info")
def model_info():
    """Get information about the loaded model - matches React frontend expectations"""
    if not model:
        return jsonify({"error": "Model not loaded"}), 500
    
    info = {
        "loaded": True,
        "model_type": "YOLOv8 Custom Basketball Model",
        "classes": list(model.names.values()),
        "performance": "74.1% mAP50-95",
        "dataset": "10k basketball images",
        "status": "Custom trained model for basketball analytics"
    }
    return jsonify(info)

@app.route("/health")
def health():
    """Health check endpoint"""
    status = {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_classes": list(model.names.values()) if model else None
    }
    return jsonify(status)

if __name__ == "__main__":
    # Load model on startup
    logger.info("Starting Basketball Detection API...")
    if not load_model():
        logger.error("Failed to load model. Exiting.")
        exit(1)
    
    logger.info("✅ Model loaded successfully")
    logger.info(f"📊 Model classes: {list(model.names.values())}")
    
    # Get port from environment (Railway sets this)
    port = int(os.environ.get("PORT", 5000))
    
    # Run the app
    logger.info(f"Starting server on port {port}")
    app.run(
        host="0.0.0.0",  # Required for Railway
        port=port,
        debug=False  # Set to False for production
    ) 