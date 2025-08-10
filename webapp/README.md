# Basketball Detection API for pyoo.dev

A production-ready Flask API for basketball object detection that can be integrated into your pyoo.dev website.

## 🚀 Quick Deploy

### Option 1: Docker (Recommended)

```bash
# Build the Docker image
docker build -t basketball-api .

# Run the container
docker run -p 5000:5000 \
  -v $(pwd)/../trainon10kdataset:/app/trainon10kdataset \
  basketball-api
```

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Copy your trained model (if available)
cp ../trainon10kdataset/weights/best.pt trainon10kdataset/weights/

# Run the development server
python app.py
```

### Option 3: Production with Gunicorn

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app
```

## 🌐 Integration with pyoo.dev

### 1. Environment Variables

Set the API URL in your Next.js environment:

```env
# .env.local
NEXT_PUBLIC_BASKETBALL_API_URL=https://your-api-domain.com
```

### 2. React Component Integration

```tsx
// pages/basketball-detection.tsx or app/basketball-detection/page.tsx
import BasketballDetector from '../components/BasketballDetector'

export default function BasketballDetectionPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <BasketballDetector />
    </div>
  )
}
```

### 3. Install Required Dependencies

```bash
# For the React component
npm install lucide-react
# If using TypeScript
npm install --save-dev @types/node
```

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

### Model Information
```
GET /api/model-info
```

### Object Detection (File Upload)
```
POST /api/detect
Content-Type: multipart/form-data
Body: image file
Query params: ?confidence=0.25
```

### Object Detection (Base64)
```
POST /api/detect-base64
Content-Type: application/json
Body: {"image": "base64_image_data"}
```

### Available Classes
```
GET /api/classes
```

## 🔧 Configuration

### CORS Settings

The API is pre-configured for pyoo.dev domains. Update the CORS origins in `app.py`:

```python
CORS(app, origins=[
    "https://pyoo.dev",
    "https://www.pyoo.dev",
    "https://your-custom-domain.com"
])
```

### Model Configuration

The API automatically tries to load models in this order:
1. Custom basketball model: `trainon10kdataset/weights/best.pt`
2. Fallback to YOLOv8n pre-trained model

## 🚢 Deployment Options

### Vercel (Recommended for Next.js integration)

1. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Railway

1. Connect your GitHub repo to Railway
2. Set environment variables
3. Deploy automatically

### DigitalOcean App Platform

1. Create new app from GitHub
2. Configure build settings:
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn --bind 0.0.0.0:$PORT app:app`

### AWS EC2 / GCP Compute

1. Set up instance with Python 3.11+
2. Install dependencies
3. Use systemd service for auto-restart
4. Configure nginx as reverse proxy

## 🔍 Monitoring

### Health Checks

The API includes built-in health checks at `/api/health` that return:
- Service status
- Model loading status
- Timestamp
- Model information

### Logging

The application logs all requests and errors. Configure log level:

```python
logging.basicConfig(level=logging.INFO)  # or DEBUG for development
```

## 🛡️ Security

### Production Checklist

- [ ] Set `debug=False` in Flask app
- [ ] Use environment variables for sensitive config
- [ ] Implement rate limiting (consider Flask-Limiter)
- [ ] Add authentication if needed
- [ ] Configure proper CORS origins
- [ ] Use HTTPS in production
- [ ] Monitor for unusual usage patterns

### File Upload Security

The API includes:
- File type validation
- File size limits (configurable)
- Safe file handling with PIL
- No file persistence (images processed in memory)

## 🎨 Customization for pyoo.dev

### Brand Colors

Update the component colors to match your brand:

```tsx
// In BasketballDetector.tsx
const brandColors = {
  primary: 'bg-blue-600', // Your brand primary
  secondary: 'bg-gray-200', // Your brand secondary
  accent: 'border-blue-500' // Your brand accent
}
```

### Integration with Your Design System

The React component uses Tailwind CSS classes that can be easily customized to match your existing design system.

## 📈 Performance

### Optimization Tips

1. **Model Loading**: Pre-load models on startup
2. **Caching**: Consider Redis for frequent requests
3. **Image Processing**: Resize large images before processing
4. **Workers**: Scale horizontally with multiple Gunicorn workers
5. **CDN**: Use CDN for static assets

### Expected Performance

- **Model Loading**: ~2-5 seconds on startup
- **Image Processing**: 200-500ms per image
- **Memory Usage**: ~1-2GB per worker
- **Throughput**: ~10-50 requests/minute per worker

## 🤝 Support

For issues with integration into pyoo.dev:
1. Check API health endpoint
2. Verify CORS configuration
3. Check network connectivity
4. Review browser console for errors
5. Monitor API logs for debugging

## 📄 License

This basketball detection system is part of the DDS70 project and can be integrated into pyoo.dev under your project's licensing terms. 