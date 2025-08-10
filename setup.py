#!/usr/bin/env python3
"""
DDS70 Setup Script
Automated setup and testing for the Basketball Object Detection project
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Need Python 3.8+")
        return False

def check_system_requirements():
    """Check system requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check if we're on macOS (M1/M2 might need special handling)
    system = platform.system()
    print(f"📱 Operating System: {system}")
    
    if system == "Darwin":
        machine = platform.machine()
        print(f"🖥️  Architecture: {machine}")
        if machine == "arm64":
            print("💡 Detected Apple Silicon (M1/M2) - optimizations available")
    
    return True

def install_dependencies():
    """Install project dependencies"""
    print("📦 Installing dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if os.path.exists("requirements.txt"):
        if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements"):
            return False
    else:
        print("⚠️  requirements.txt not found, installing core dependencies...")
        core_deps = [
            "ultralytics>=8.0.207",
            "opencv-python>=4.8.0",
            "flask>=2.3.0",
            "waitress>=2.1.0",
            "Pillow>=9.4.0"
        ]
        
        for dep in core_deps:
            if not run_command(f"{sys.executable} -m pip install {dep}", f"Installing {dep}"):
                return False
    
    return True

def test_installation():
    """Test if all components work"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        print("📋 Testing imports...")
        import cv2
        print(f"  ✅ OpenCV {cv2.__version__}")
        
        from ultralytics import YOLO
        print("  ✅ Ultralytics YOLO")
        
        import flask
        print(f"  ✅ Flask {flask.__version__}")
        
        from PIL import Image
        print("  ✅ Pillow")
        
        # Test model loading
        print("🤖 Testing model loading...")
        try:
            model = YOLO("yolov8n.pt")
            print("  ✅ YOLOv8n model loaded successfully")
        except Exception as e:
            print(f"  ⚠️  YOLOv8n model loading issue: {e}")
        
        # Check for custom model
        custom_model_path = "trainon10kdataset/weights/best.pt"
        if os.path.exists(custom_model_path):
            try:
                custom_model = YOLO(custom_model_path)
                print("  ✅ Custom basketball model loaded successfully")
            except Exception as e:
                print(f"  ⚠️  Custom model loading issue: {e}")
        else:
            print("  ℹ️  Custom model not found (will use pre-trained)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def show_usage_instructions():
    """Show how to use the project"""
    print("\n" + "="*60)
    print("🎉 Setup completed successfully!")
    print("="*60)
    print("\n🚀 How to run the project:")
    print("\n1. Web Interface (Recommended for demos):")
    print("   python app.py")
    print("   Then open: http://localhost:8080")
    
    print("\n2. Real-time Webcam Demo:")
    print("   python demo.py")
    
    print("\n3. Jupyter Notebooks:")
    print("   jupyter notebook")
    print("   Open any .ipynb file")
    
    print("\n📊 Model Performance:")
    print("   - Custom model: 74.1% mAP50-95")
    print("   - Classes: Basketball courts, balls, players, rims, shots")
    
    print("\n💡 Tips for interviews:")
    print("   - Use 'python demo.py' for real-time demonstration")
    print("   - Show training results in trainon10kdataset/ folder")
    print("   - Upload basketball images via web interface")
    
    print("\n🔧 Troubleshooting:")
    print("   - If webcam doesn't work, check camera permissions")
    print("   - If model loading fails, ensure stable internet connection")
    print("   - For M1/M2 Macs, some dependencies might need Rosetta")

def main():
    """Main setup function"""
    print("🏀 DDS70 Basketball Object Detection Setup")
    print("=" * 50)
    
    # Check system requirements
    if not check_system_requirements():
        print("❌ System requirements not met")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        print("💡 Try running: pip install -r requirements.txt")
        sys.exit(1)
    
    # Show usage instructions
    show_usage_instructions()

if __name__ == "__main__":
    main() 