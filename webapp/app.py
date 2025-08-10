"""
Basketball Object Detection Web App
Production-ready Flask application for pyoo website integration
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import os
import io
import base64
import logging
import json
from datetime import datetime
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS for your website integration
CORS(app, origins=[
    "https://pyoo.dev",
    "https://www.pyoo.dev", 
    "http://localhost:3000",  # For local development
    "http://localhost:8080"
])

# Global model variable
model = None
model_info = {
    "loaded": False,
    "model_type": None,
    "classes": [],
    "load_time": None,
    "error": None
}

def load_model():
    """Load the YOLO model with comprehensive error handling"""
    global model, model_info
    start_time = datetime.now()
    
    try:
        # Try to load custom trained model first
        custom_model_path = "../trainon10kdataset/weights/best.pt"
        if os.path.exists(custom_model_path):
            logger.info(f"Loading custom basketball model: {custom_model_path}")
            model = YOLO(custom_model_path)
            model_info.update({
                "loaded": True,
                "model_type": "Custom Basketball Model",
                "classes": list(model.names.values()),
                "load_time": (datetime.now() - start_time).total_seconds(),
                "error": None
            })
            logger.info(f"Custom model loaded successfully with classes: {model.names}")
            return True
        else:
            # Fallback to pre-trained model
            logger.info("Custom model not found, loading pre-trained YOLOv8n")
            model = YOLO("yolov8n.pt")
            model_info.update({
                "loaded": True,
                "model_type": "YOLOv8n Pre-trained",
                "classes": list(model.names.values()),
                "load_time": (datetime.now() - start_time).total_seconds(),
                "error": None
            })
            logger.info("Pre-trained model loaded successfully")
            return True
            
    except Exception as e:
        error_msg = f"Error loading model: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        model_info.update({
            "loaded": False,
            "error": error_msg,
            "load_time": (datetime.now() - start_time).total_seconds()
        })
        return False

@app.route("/")
def index():
    """Serve the main basketball detection page"""
    return render_template("basketball_detector.html")

@app.route("/api/health")
def health():
    """Enhanced health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Basketball Object Detection API",
        "timestamp": datetime.now().isoformat(),
        "model": model_info
    })

@app.route("/api/detect", methods=["POST"])
def detect():
    """
    Enhanced detection endpoint with better error handling and response format
    """
    if not model_info["loaded"]:
        return jsonify({
            "success": False,
            "error": "Model not loaded",
            "details": model_info.get("error", "Unknown error")
        }), 500
    
    try:
        # Check for file upload
        if "image" not in request.files:
            return jsonify({
                "success": False,
                "error": "No image file provided"
            }), 400
        
        file = request.files["image"]
        if file.filename == "":
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_ext not in allowed_extensions:
            return jsonify({
                "success": False,
                "error": f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            }), 400
        
        # Process the image
        start_time = datetime.now()
        image = Image.open(file.stream)
        
        # Run detection
        detections = detect_objects_on_image(image)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return jsonify({
            "success": True,
            "detections": detections,
            "count": len(detections),
            "processing_time": round(processing_time, 3),
            "image_size": {
                "width": image.width,
                "height": image.height
            },
            "model": model_info["model_type"],
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in detect endpoint: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"Detection failed: {str(e)}"
        }), 500

@app.route("/api/detect-base64", methods=["POST"])
def detect_base64():
    """
    Alternative endpoint for base64 image detection (useful for frontend uploads)
    """
    if not model_info["loaded"]:
        return jsonify({
            "success": False,
            "error": "Model not loaded"
        }), 500
    
    try:
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({
                "success": False,
                "error": "No base64 image data provided"
            }), 400
        
        # Decode base64 image
        image_data = data["image"]
        if image_data.startswith("data:image"):
            # Remove data URL prefix
            image_data = image_data.split(",")[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Run detection
        start_time = datetime.now()
        detections = detect_objects_on_image(image)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return jsonify({
            "success": True,
            "detections": detections,
            "count": len(detections),
            "processing_time": round(processing_time, 3),
            "image_size": {
                "width": image.width,
                "height": image.height
            },
            "model": model_info["model_type"],
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in base64 detect endpoint: {e}")
        return jsonify({
            "success": False,
            "error": f"Detection failed: {str(e)}"
        }), 500

def detect_objects_on_image(image):
    """
    Enhanced object detection with confidence scoring and metadata
    """
    try:
        # Get confidence threshold from request (default 0.25)
        confidence = float(request.args.get('confidence', 0.25))
        
        results = model.predict(image, conf=confidence, verbose=False)
        result = results[0]
        detections = []
        
        for box in result.boxes:
            x1, y1, x2, y2 = [round(float(x)) for x in box.xyxy[0].tolist()]
            class_id = int(box.cls[0].item())
            confidence_score = round(float(box.conf[0].item()), 3)
            class_name = result.names[class_id]
            
            detection = {
                "bbox": {
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "width": x2 - x1,
                    "height": y2 - y1,
                    "center_x": (x1 + x2) // 2,
                    "center_y": (y1 + y2) // 2
                },
                "class": class_name,
                "class_id": class_id,
                "confidence": confidence_score,
                "area": (x2 - x1) * (y2 - y1)
            }
            detections.append(detection)
        
        # Sort by confidence (highest first)
        detections.sort(key=lambda x: x["confidence"], reverse=True)
        
        logger.info(f"Detected {len(detections)} objects")
        return detections
    
    except Exception as e:
        logger.error(f"Error in object detection: {e}")
        return []

@app.route("/api/model-info")
def get_model_info():
    """Get detailed information about the loaded model"""
    return jsonify(model_info)

@app.route("/api/classes")
def get_classes():
    """Get available detection classes"""
    if model_info["loaded"]:
        return jsonify({
            "success": True,
            "classes": model_info["classes"],
            "count": len(model_info["classes"])
        })
    else:
        return jsonify({
            "success": False,
            "error": "Model not loaded"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "available_endpoints": [
            "/api/health",
            "/api/detect",
            "/api/detect-base64",
            "/api/model-info",
            "/api/classes"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == "__main__":
    print("🏀 Basketball Detection API for pyoo.dev")
    print("=" * 50)
    
    # Load the model
    if not load_model():
        print("❌ Failed to load model. Starting with limited functionality.")
    else:
        print(f"✅ Model loaded: {model_info['model_type']}")
        print(f"📊 Classes: {len(model_info['classes'])}")
        print(f"⏱️  Load time: {model_info['load_time']:.2f}s")
    
    print("🌐 Starting API server...")
    print("📡 CORS enabled for pyoo.dev integration")
    
    # Run the development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,  # Set to False for production
        threaded=True
    ) 