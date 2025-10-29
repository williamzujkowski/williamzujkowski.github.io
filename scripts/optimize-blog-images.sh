#!/bin/bash

# Blog Image Optimization Script
# Optimizes images and creates responsive variants

echo "🚀 Blog Image Optimization Script"
echo "=================================="

# Check for required tools
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        echo "   Install with: $2"
        return 1
    fi
    return 0
}

# Check for ImageMagick
if ! check_tool "convert" "apt-get install imagemagick"; then
    echo "Installing fallback optimization..."
fi

# Check for jpegoptim
if ! check_tool "jpegoptim" "apt-get install jpegoptim"; then
    echo "Skipping JPEG optimization..."
fi

# Check for optipng
if ! check_tool "optipng" "apt-get install optipng"; then
    echo "Skipping PNG optimization..."
fi

# Navigate to images directory
cd src/assets/images/blog || exit 1

echo ""
echo "📊 Current image statistics:"
echo "----------------------------"
find . -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -exec du -ch {} + | tail -1

# Create responsive image sizes
echo ""
echo "📐 Creating responsive variants..."
echo "----------------------------------"

# Process hero images (original files only, not variants)
for img in hero/*.jpg; do
    if [ -f "$img" ]; then
        # Skip if file already has size suffix (-400, -800, -thumb, -og)
        if [[ "$img" =~ -[0-9]+\.jpg$ ]] || [[ "$img" =~ -(thumb|og)\.jpg$ ]]; then
            echo "  ⏭️  Skipping $img (variant file)"
            continue
        fi

        basename="${img%.*}"

        # Skip if variants already exist
        if [ -f "${basename}-800.jpg" ]; then
            echo "  ⏭️  Skipping $img (variants exist)"
            continue
        fi
        
        echo "  📸 Processing $img..."
        
        # Create responsive sizes if ImageMagick is available
        if command -v convert &> /dev/null; then
            # Medium size (800px wide)
            convert "$img" -resize 800x -quality 85 "${basename}-800.jpg" 2>/dev/null
            
            # Small size (400px wide)
            convert "$img" -resize 400x -quality 85 "${basename}-400.jpg" 2>/dev/null
            
            # Thumbnail (200px wide)
            convert "$img" -resize 200x -quality 85 "${basename}-thumb.jpg" 2>/dev/null
            
            echo "     ✅ Created responsive variants"
        fi
    fi
done

# Optimize images
echo ""
echo "🔧 Optimizing images..."
echo "-----------------------"

# Optimize JPEGs
if command -v jpegoptim &> /dev/null; then
    echo "  📦 Optimizing JPEG images..."
    find . -name "*.jpg" -o -name "*.jpeg" | while read img; do
        original_size=$(du -h "$img" | cut -f1)
        jpegoptim --max=85 --strip-all --preserve --quiet "$img"
        new_size=$(du -h "$img" | cut -f1)
        echo "     ✅ $img: $original_size → $new_size"
    done
fi

# Optimize PNGs
if command -v optipng &> /dev/null; then
    echo "  📦 Optimizing PNG images..."
    find . -name "*.png" | while read img; do
        original_size=$(du -h "$img" | cut -f1)
        optipng -quiet -o2 "$img"
        new_size=$(du -h "$img" | cut -f1)
        echo "     ✅ $img: $original_size → $new_size"
    done
fi

# Create WebP versions (if cwebp is available)
if command -v cwebp &> /dev/null; then
    echo ""
    echo "🎨 Creating WebP versions..."
    echo "----------------------------"
    
    for img in hero/*.jpg; do
        if [ -f "$img" ]; then
            # Skip variant files for WebP generation too
            if [[ "$img" =~ -[0-9]+\.jpg$ ]] || [[ "$img" =~ -(thumb|og)\.jpg$ ]]; then
                continue
            fi

            webp_file="${img%.*}.webp"

            # Skip if WebP already exists
            if [ -f "$webp_file" ]; then
                echo "  ⏭️  Skipping $img (WebP exists)"
                continue
            fi
            
            cwebp -q 85 "$img" -o "$webp_file" 2>/dev/null
            
            if [ -f "$webp_file" ]; then
                echo "  ✅ Created $webp_file"
            fi
        fi
    done
else
    echo ""
    echo "ℹ️  Install webp tools for WebP support:"
    echo "   apt-get install webp"
fi

echo ""
echo "📊 Final image statistics:"
echo "-------------------------"
find . -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.webp" \) -exec du -ch {} + | tail -1

echo ""
echo "✨ Image optimization complete!"
echo ""
echo "📋 Summary:"
echo "-----------"
echo "• Hero images: $(ls hero/*.jpg 2>/dev/null | wc -l)"
echo "• Responsive variants: $(ls hero/*-800.jpg 2>/dev/null | wc -l)"
echo "• WebP versions: $(ls hero/*.webp 2>/dev/null | wc -l)"
echo ""
echo "🎯 Next steps:"
echo "1. Test image loading performance"
echo "2. Implement lazy loading"
echo "3. Set up image CDN if needed"
echo "4. Monitor Core Web Vitals"