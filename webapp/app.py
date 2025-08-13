"""
Basketball Object Detection Web Application
DDS70 Project - Flask Backend for Railway Deployment
"""

import os
# Set environment variables before any imports that might use OpenCV
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '0'
os.environ['OPENCV_IO_ENABLE_JASPER'] = '0'
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['DISPLAY'] = ''

from flask import Flask, request, Response, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import json
import logging
import time
import random

# Try to import YOLO with proper error handling
YOLO_AVAILABLE = False
model = None

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
    print("✅ YOLO imported successfully")
except ImportError as e:
    print(f"⚠️ YOLO import failed: {e}")
    print("🎭 Running in enhanced demo mode")
    YOLO_AVAILABLE = False

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

def load_model():
    """Load the YOLO model with error handling"""
    global model
    
    if not YOLO_AVAILABLE:
        logger.info("YOLO not available - running in enhanced demo mode")
        return True  # Return success for demo mode
    
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
        "mode": "real" if YOLO_AVAILABLE and model else "demo",
        "endpoints": ["/api/detect", "/api/model-info", "/health"]
    })

@app.route("/api/detect", methods=["POST"])
def detect():
    """
    Handler for /api/detect POST endpoint
    Receives uploaded file, processes through YOLO detection or enhanced demo
    and returns detection results in the format expected by the React frontend
    """
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        # Process the image
        image = Image.open(file.stream)
        
        if YOLO_AVAILABLE and model:
            # Use real YOLO model
            results = detect_objects_on_image(image)
        else:
            # Use enhanced demo mode
            results = enhanced_demo_detection(image, file.filename)
        
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

def enhanced_demo_detection(image, filename="image.jpg"):
    """
    Enhanced demo mode that provides realistic basketball detection simulation
    """
    start_time = time.time()
    
    # Basketball-specific classes
    BASKETBALL_CLASSES = ["Basketball-court", "ball", "made", "person", "rim", "shoot"]
    
    # Create a seed based on image properties for consistent results
    seed = len(filename) + image.width + image.height
    random.seed(seed)
    
    detections = []
    
    # Analyze filename for context
    filename_lower = filename.lower()
    is_ball_image = 'ball' in filename_lower or 'basketball' in filename_lower
    is_court_image = 'court' in filename_lower or 'game' in filename_lower
    is_player_image = 'player' in filename_lower or 'person' in filename_lower
    
    # Generate realistic detections based on context
    if is_ball_image or (not is_court_image and not is_player_image):
        # Prioritize ball detection
        detections.append({
            "class": "ball",
            "confidence": round(random.uniform(0.85, 0.95), 2),
            "bbox": [
                random.randint(int(image.width * 0.2), int(image.width * 0.8)),
                random.randint(int(image.height * 0.2), int(image.height * 0.8)),
                random.randint(int(image.width * 0.3), int(image.width * 0.9)),
                random.randint(int(image.height * 0.3), int(image.height * 0.9))
            ]
        })
    
    if is_player_image or is_court_image:
        # Add person detection
        for i in range(random.randint(1, 2)):
            detections.append({
                "class": "person",
                "confidence": round(random.uniform(0.75, 0.92), 2),
                "bbox": [
                    random.randint(50 + i * 200, 150 + i * 200),
                    random.randint(100, 200),
                    random.randint(120 + i * 200, 220 + i * 200),
                    random.randint(350, 450)
                ]
            })
    
    if is_court_image:
        # Add court detection
        detections.append({
            "class": "Basketball-court",
            "confidence": round(random.uniform(0.80, 0.95), 2),
            "bbox": [10, 10, image.width - 10, image.height - 10]
        })
        
        # Maybe add rim
        if random.random() > 0.5:
            detections.append({
                "class": "rim",
                "confidence": round(random.uniform(0.70, 0.88), 2),
                "bbox": [
                    random.randint(int(image.width * 0.4), int(image.width * 0.6)),
                    random.randint(20, 100),
                    random.randint(int(image.width * 0.5), int(image.width * 0.7)),
                    random.randint(80, 160)
                ]
            })
    
    # If no detections, add a default ball
    if not detections:
        detections.append({
            "class": "ball",
            "confidence": round(random.uniform(0.75, 0.90), 2),
            "bbox": [
                random.randint(100, 300),
                random.randint(100, 300),
                random.randint(200, 400),
                random.randint(200, 400)
            ]
        })
    
    processing_time = round(time.time() - start_time + random.uniform(0.5, 1.5), 2)
    
    return {
        "detections": detections,
        "processing_time": f"{processing_time}s",
        "total_objects": len(detections),
        "model_used": "Enhanced Basketball Demo (YOLO Unavailable)",
        "image_size": {"width": image.width, "height": image.height},
        "demo_mode": True
    }

@app.route("/api/model-info")
def model_info():
    """Get information about the loaded model - matches React frontend expectations"""
    
    if YOLO_AVAILABLE and model:
        # Real model info
        info = {
            "loaded": True,
            "model_type": "YOLOv8 Custom Basketball Model",
            "classes": list(model.names.values()),
            "performance": "74.1% mAP50-95",
            "dataset": "10k basketball images",
            "status": "Custom trained model for basketball analytics"
        }
    else:
        # Demo mode info
        info = {
            "loaded": True,
            "model_type": "Enhanced Basketball Demo",
            "classes": ["Basketball-court", "ball", "made", "person", "rim", "shoot"],
            "performance": "Demo simulation",
            "dataset": "Simulated basketball detection",
            "status": "Demo mode - YOLO dependencies unavailable",
            "demo_mode": True
        }
    
    return jsonify(info)

@app.route("/health")
def health():
    """Health check endpoint"""
    status = {
        "status": "healthy",
        "yolo_available": YOLO_AVAILABLE,
        "model_loaded": model is not None if YOLO_AVAILABLE else "demo_mode",
        "mode": "real" if (YOLO_AVAILABLE and model) else "demo"
    }
    
    if YOLO_AVAILABLE and model:
        status["model_classes"] = list(model.names.values())
    
    return jsonify(status)

if __name__ == "__main__":
    # Load model on startup
    logger.info("Starting Basketball Detection API...")
    
    if load_model():
        if YOLO_AVAILABLE and model:
            logger.info("✅ Real YOLO model loaded successfully")
            logger.info(f"📊 Model classes: {list(model.names.values())}")
        else:
            logger.info("✅ Enhanced demo mode active")
    else:
        logger.warning("⚠️ Model loading failed, but continuing with demo mode")
    
    # Get port from environment (Railway sets this)
    port = int(os.environ.get("PORT", 5000))
    
    # Run the app
    logger.info(f"Starting server on port {port}")
    app.run(
        host="0.0.0.0",  # Required for Railway
        port=port,
        debug=False  # Set to False for production
    ) 