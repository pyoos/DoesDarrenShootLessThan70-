"""
Basketball Object Detection Web Application
DDS70 Project - Flask Backend
"""

from ultralytics import YOLO
from flask import Flask, request, Response, jsonify, send_from_directory
from waitress import serve
from PIL import Image
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

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
            logger.info(f"Loaded custom model from {model_path}")
            return True
        else:
            # Fallback to pre-trained model
            model = YOLO("yolov8n.pt")
            logger.info("Loaded pre-trained YOLOv8n model")
            return True
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

@app.route("/")
def root():
    """Serve the main page"""
    try:
        return send_from_directory(".", "index.html")
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return "<h1>Error: index.html not found</h1>", 404

@app.route("/detect", methods=["POST"])
def detect():
    """
    Handler for /detect POST endpoint
    Receives uploaded file with name "image_file", 
    passes it through YOLO object detection 
    and returns an array of bounding boxes.
    """
    if not model:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        if "image_file" not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files["image_file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        # Process the image
        image = Image.open(file.stream)
        boxes = detect_objects_on_image(image)
        
        return Response(
            json.dumps(boxes),  
            mimetype='application/json'
        )
    
    except Exception as e:
        logger.error(f"Error in detect endpoint: {e}")
        return jsonify({"error": f"Detection failed: {str(e)}"}), 500

def detect_objects_on_image(image):
    """
    Function receives an image,
    passes it through YOLO neural network
    and returns an array of detected objects
    and their bounding boxes
    """
    try:
        results = model.predict(image, conf=0.25)  # Lower confidence threshold
        result = results[0]
        output = []
        
        for box in result.boxes:
            x1, y1, x2, y2 = [
                round(x) for x in box.xyxy[0].tolist()
            ]
            class_id = box.cls[0].item()
            prob = round(box.conf[0].item(), 2)
            
            output.append([
                x1, y1, x2, y2, result.names[class_id], prob
            ])
        
        logger.info(f"Detected {len(output)} objects")
        return output
    
    except Exception as e:
        logger.error(f"Error in object detection: {e}")
        return []

@app.route("/health")
def health():
    """Health check endpoint"""
    status = {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_classes": list(model.names.values()) if model else None
    }
    return jsonify(status)

@app.route("/model-info")
def model_info():
    """Get information about the loaded model"""
    if not model:
        return jsonify({"error": "Model not loaded"}), 500
    
    info = {
        "model_type": "YOLOv8",
        "classes": list(model.names.values()),
        "num_classes": len(model.names)
    }
    return jsonify(info)

if __name__ == "__main__":
    print("🏀 Starting Basketball Object Detection Server...")
    
    # Load the model
    if not load_model():
        print("❌ Failed to load model. Exiting.")
        exit(1)
    
    print(f"✅ Model loaded successfully")
    print(f"📊 Model classes: {list(model.names.values())}")
    print("🌐 Starting server on http://localhost:8080")
    print("📱 Open your browser and navigate to http://localhost:8080")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Start the server
    try:
        serve(app, host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}") 