# DDS70 Basketball Detection - Website Integration Guide

This guide shows you the **best ways to integrate** the basketball object detection system into your existing pyoo.info/dds70 page.

## 🎯 Integration Options (Choose One)

### Option 1: Simple JavaScript Widget (Recommended)
**Best for: Existing websites, minimal changes required**

1. Upload `dds70-widget.js` to your website
2. Add two lines to your existing HTML:

```html
<!-- In your pyoo.info/dds70 page -->
<div id="dds70-detector"></div>
<script src="path/to/dds70-widget.js"></script>
```

**That's it!** The widget will automatically initialize and work.

### Option 2: Self-Contained HTML Embed
**Best for: Maximum control, custom styling**

1. Use the content from `dds70-embed.html`
2. Copy the entire widget div into your existing page:

```html
<!-- Copy this into your pyoo.info/dds70 page -->
<div class="dds70-widget">
    <!-- Widget content goes here -->
</div>
```

### Option 3: iframe Embed
**Best for: Quick integration, isolation from existing styles**

```html
<!-- Simple iframe embed -->
<iframe 
    src="https://your-domain.com/dds70-embed.html" 
    width="100%" 
    height="800" 
    frameborder="0"
    style="border-radius: 12px;">
</iframe>
```

## 🔧 Setup Steps

### 1. Deploy the API Backend

Choose your deployment method:

**Option A: Quick Cloud Deploy**
```bash
# Railway, Vercel, or similar
git push origin main  # Auto-deploys from your repo
```

**Option B: Docker Deploy**
```bash
cd webapp
docker build -t dds70-api .
docker run -p 5000:5000 dds70-api
```

**Option C: Traditional Server**
```bash
cd webapp
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:5000 app:app
```

### 2. Update API Configuration

In `dds70-widget.js`, update the API URL:
```javascript
const DDS70_CONFIG = {
    apiUrl: 'https://your-api-domain.com', // Update this!
    containerId: 'dds70-detector',
    // ... rest of config
};
```

### 3. Integration Examples

#### For WordPress/PHP Sites:
```php
<!-- In your page template -->
<div class="basketball-detection-section">
    <h2>Basketball Object Detection Demo</h2>
    <div id="dds70-detector"></div>
    <script src="<?php echo get_template_directory_uri(); ?>/js/dds70-widget.js"></script>
</div>
```

#### For Static HTML Sites:
```html
<!DOCTYPE html>
<html>
<head>
    <title>DDS70 - Basketball Analytics</title>
</head>
<body>
    <div class="container">
        <h1>Basketball Object Detection</h1>
        
        <!-- Basketball Detection Widget -->
        <div id="dds70-detector"></div>
        <script src="./js/dds70-widget.js"></script>
        
        <!-- Rest of your content -->
    </div>
</body>
</html>
```

#### For React/Next.js Sites:
```tsx
// components/BasketballDetection.tsx
import { useEffect } from 'react';

export default function BasketballDetection() {
  useEffect(() => {
    // Load the widget script
    const script = document.createElement('script');
    script.src = '/js/dds70-widget.js';
    document.body.appendChild(script);
    
    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <div className="basketball-section">
      <h2>Basketball Object Detection</h2>
      <div id="dds70-detector"></div>
    </div>
  );
}
```

## 🎨 Customization

### Match Your Website's Design

Update the theme in `dds70-widget.js`:
```javascript
theme: {
    primary: '#your-brand-color',      // Main button color
    primaryHover: '#darker-shade',     // Hover state
    background: '#ffffff',             // Widget background
    border: '#e5e7eb',                // Border color
    text: '#111827',                   // Text color
    textSecondary: '#6b7280'          // Secondary text
}
```

### Custom CSS Override
```css
/* Add to your existing CSS */
.dds70-container {
    border: 2px solid #your-brand-color !important;
    border-radius: 8px !important;
}

.dds70-header {
    background: linear-gradient(135deg, #your-primary, #your-secondary) !important;
}
```

## 📁 File Structure for Integration

```
your-website/
├── index.html (or your existing page)
├── js/
│   └── dds70-widget.js          ← Upload this
├── css/
│   └── your-styles.css          ← Add custom overrides here
└── api/                         ← Deploy separately
    ├── app.py
    ├── requirements.txt
    └── ...
```

## 🌐 Deployment Recommendations

### For pyoo.info specifically:

1. **Frontend Integration**: Use Option 1 (JavaScript Widget)
2. **API Deployment**: 
   - Railway (easiest): Connect GitHub repo
   - Vercel (if Next.js): Add `vercel.json` 
   - DigitalOcean App Platform: Balanced option
   - Your existing server: Traditional deployment

3. **Domain Setup**:
   - API: `https://api.pyoo.info` or `https://dds70-api.pyoo.info`
   - Widget: Embedded directly in `https://pyoo.info/dds70`

## 🚀 Quick Start (5 Minutes)

1. **Upload Files**:
   ```bash
   # Copy widget to your website
   cp integration/dds70-widget.js /path/to/your/website/js/
   ```

2. **Deploy API**:
   ```bash
   # Quick Railway deploy
   cd webapp
   git init && git add . && git commit -m "Initial commit"
   # Connect to Railway and deploy
   ```

3. **Update Your Page**:
   ```html
   <!-- Add anywhere in your pyoo.info/dds70 page -->
   <section id="basketball-detection">
       <h2>Try Our Basketball Detection System</h2>
       <div id="dds70-detector"></div>
       <script src="/js/dds70-widget.js"></script>
   </section>
   ```

4. **Configure**:
   - Update API URL in `dds70-widget.js`
   - Test with a basketball image
   - Done! 🎉

## 🔍 Testing

Test your integration:

1. **Check API Health**: Visit `https://your-api-url.com/api/health`
2. **Test Widget**: Upload a basketball image
3. **Check Console**: Look for any JavaScript errors
4. **Mobile Test**: Verify responsive design works

## 🛠️ Troubleshooting

### Common Issues:

**Widget doesn't appear:**
- Check if `#dds70-detector` div exists
- Verify JavaScript file loads correctly
- Check browser console for errors

**API connection fails:**
- Verify API URL in config
- Check CORS settings in API
- Ensure API is deployed and accessible

**Images don't upload:**
- Check file size limits
- Verify supported formats (JPG, PNG, GIF, WebP)
- Check browser network tab for errors

## 📊 Performance

- **Widget Load Time**: ~50KB JavaScript + CSS
- **API Response Time**: 200-500ms per image
- **Memory Usage**: Minimal (images processed server-side)
- **Mobile Friendly**: Fully responsive design

## 🔐 Security

- **File Validation**: Only image files accepted
- **CORS Protection**: Configured for your domains
- **No Data Storage**: Images processed in memory only
- **Rate Limiting**: Can be added if needed

## 🎯 Live Example

After integration, your pyoo.info/dds70 page will have:

1. **Professional UI** that matches your site
2. **Drag-and-drop** image upload
3. **Real-time analysis** with confidence scores
4. **Detailed results** showing detected objects
5. **Mobile responsive** design
6. **Error handling** and loading states

The basketball detection system will be seamlessly integrated into your existing website with minimal code changes!

---

**Need help?** Check the troubleshooting section or review the example files in this integration folder. 