# Favicon Information

## Current Favicon Design

The favicon is a security-themed shield with circuit patterns, representing the intersection of cybersecurity and technology/AI.

### Design Elements:
- **Shield Shape**: Represents security and protection
- **Circuit Pattern**: Represents technology, AI, and interconnected systems
- **Lock Icon**: Central security focus
- **Blue Color Scheme**: Professional, trustworthy, tech-oriented

### Files:
- `favicon.svg` - Scalable vector format (works in modern browsers)
- `favicon.ico` - Legacy format (needs to be generated from SVG)

## How to Generate favicon.ico

Since the SVG has been created, you need to convert it to ICO format:

### Option 1: Command Line (Recommended)
```bash
# Install ImageMagick if not already installed
sudo apt-get install imagemagick

# Convert SVG to ICO with multiple sizes
convert favicon.svg -resize 16x16 favicon-16.png
convert favicon.svg -resize 32x32 favicon-32.png
convert favicon.svg -resize 48x48 favicon-48.png
convert favicon-16.png favicon-32.png favicon-48.png favicon.ico

# Clean up temporary files
rm favicon-16.png favicon-32.png favicon-48.png
```

### Option 2: Python Script
```bash
# Install dependencies
pip install cairosvg Pillow

# Run the generate_favicons.py script
python generate_favicons.py
```

### Option 3: Online Converter
1. Go to https://convertio.co/svg-ico/
2. Upload `favicon.svg`
3. Download the converted `favicon.ico`
4. Replace the placeholder file

## Additional Icon Formats (Optional)

For comprehensive browser support, you might also want:

```html
<!-- In base.njk -->
<link rel="icon" type="image/svg+xml" href="/assets/images/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/images/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

## Color Reference
- Primary Blue: #1e40af
- Light Blue: #3b82f6
- Accent Blue: #60a5fa
- Dark Accent: #1e3a8a
- Light Accent: #dbeafe

This design effectively represents your focus on security engineering while incorporating the tech/AI elements that are central to your work.