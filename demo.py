"""
Real-time Basketball Object Detection Demo
DDS70 Project - Webcam Demo

This script demonstrates the real-time object detection capabilities
using your webcam. Perfect for interviews and demonstrations.
"""

import cv2
import math
from ultralytics import YOLO
import os
import sys

def load_model():
    """Load the best available model"""
    # Try custom model first
    custom_model_path = "trainon10kdataset/weights/best.pt"
    if os.path.exists(custom_model_path):
        print(f"🎯 Loading custom basketball model: {custom_model_path}")
        model = YOLO(custom_model_path)
        class_names = ["Basketball-court", "ball", "made", "person", "rim", "shoot"]
        print(f"📊 Custom model classes: {class_names}")
        return model, class_names
    else:
        print("🔄 Custom model not found, using pre-trained YOLOv8n")
        model = YOLO("yolov8n.pt")
        class_names = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                      "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                      "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                      "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                      "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                      "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                      "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                      "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                      "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                      "teddy bear", "hair drier", "toothbrush"]
        print(f"📊 Pre-trained model loaded with {len(class_names)} classes")
        return model, class_names

def run_demo():
    """Run the real-time detection demo"""
    print("🏀 Basketball Object Detection Demo")
    print("=" * 50)
    
    # Load model
    try:
        model, class_names = load_model()
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False
    
    # Initialize webcam
    print("📹 Initializing webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam")
        return False
    
    # Set webcam properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("✅ Webcam initialized successfully!")
    print("\n🎮 Controls:")
    print("  - Press 'q' to quit")
    print("  - Press 's' to save screenshot")
    print("  - Press 'i' to show/hide info")
    print("\n🚀 Starting detection...")
    
    frame_count = 0
    show_info = True
    
    try:
        while True:
            success, img = cap.read()
            if not success:
                print("❌ Failed to read from webcam")
                break
            
            frame_count += 1
            
            # Run detection
            results = model(img, stream=True, conf=0.3, verbose=False)
            
            # Process results
            for r in results:
                boxes = r.boxes
                
                for box in boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    # Get confidence and class
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    
                    if cls < len(class_names):
                        class_name = class_names[cls]
                        
                        # Choose color based on confidence
                        if confidence > 0.7:
                            color = (0, 255, 0)  # Green for high confidence
                        elif confidence > 0.5:
                            color = (0, 255, 255)  # Yellow for medium confidence
                        else:
                            color = (0, 0, 255)  # Red for low confidence
                        
                        # Draw bounding box
                        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                        
                        # Create label
                        label = f"{class_name}: {confidence:.2f}"
                        
                        # Get text size for background
                        (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                        
                        # Draw background for text
                        cv2.rectangle(img, (x1, y1 - text_height - 10), (x1 + text_width, y1), color, -1)
                        
                        # Draw text
                        cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Add info overlay
            if show_info:
                info_text = [
                    f"Frame: {frame_count}",
                    f"Model: {'Custom Basketball' if 'best.pt' in str(model.ckpt_path) else 'YOLOv8n'}",
                    "Press 'q' to quit, 's' to save, 'i' to toggle info"
                ]
                
                for i, text in enumerate(info_text):
                    y_pos = 30 + (i * 25)
                    cv2.putText(img, text, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    cv2.putText(img, text, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
            
            # Display the frame
            cv2.imshow('🏀 Basketball Object Detection - DDS70', img)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("👋 Quitting demo...")
                break
            elif key == ord('s'):
                filename = f"detection_screenshot_{frame_count}.jpg"
                cv2.imwrite(filename, img)
                print(f"📸 Screenshot saved as {filename}")
            elif key == ord('i'):
                show_info = not show_info
                print(f"ℹ️  Info overlay: {'ON' if show_info else 'OFF'}")
    
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        
        # Force close any remaining windows
        for i in range(5):
            cv2.waitKey(1)
        
        print("✅ Demo completed successfully!")
        return True

if __name__ == "__main__":
    print("🎬 Starting DDS70 Basketball Detection Demo")
    print("💡 Make sure you have a webcam connected!")
    
    try:
        success = run_demo()
        if success:
            print("🎉 Demo finished successfully!")
        else:
            print("⚠️  Demo encountered issues")
            sys.exit(1)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1) 