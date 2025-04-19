# Image Usage Guide

This guide explains how to use images effectively in your website content, taking advantage of the built-in image optimization system.

## Table of Contents

1. [Adding Images to Blog Posts](#adding-images-to-blog-posts)
2. [Image Optimization](#image-optimization)
3. [Using the Image Shortcode](#using-the-image-shortcode)
4. [Responsive Images](#responsive-images)
5. [Image Best Practices](#image-best-practices)

## Adding Images to Blog Posts

### File Location

All blog images should be stored in the `assets/images/blog/` directory:

- General blog images: `assets/images/blog/`
- Topic-specific images: `assets/images/blog/topics/`

### Image Naming

Use descriptive, kebab-case filenames that reflect the content of the image:

```
good-example-image-name.jpg    ✅
bad_example_name.jpg           ❌
IMG_20230615_123456.jpg        ❌
```

### Referencing Images in Blog Posts

In your Markdown content, use the image shortcode to include images:

```njk
{% image "blog/your-image.jpg", "Descriptive alt text about the image", "100vw" %}
```

## Image Optimization

The website includes an automated image optimization process that:

1. Creates multiple sizes of each image
2. Converts images to modern formats (WebP)
3. Compresses images for better performance
4. Maintains image metadata for responsive usage

### Running Image Optimization

To optimize all blog images:

```bash
npm run optimize:images:blog
```

To optimize a specific image:

```bash
./scripts/bin/media.sh optimize-image path/to/your/image.jpg
```

### What Gets Optimized

The optimizer creates:

- Multiple sizes of each image (320px, 640px, 768px, 1024px, 1280px)
- WebP versions for modern browsers
- JPEG versions for fallback support

Optimized images are stored in `assets/images/optimized/` subdirectories while preserving the original images.

## Using the Image Shortcode

The built-in `image` shortcode automatically uses optimized versions when available:

```njk
{% image "path/to/image.jpg", "Alt text", "100vw" %}
```

Parameters:

1. **src**: Path to the image (relative to the assets/images directory)
2. **alt**: Alternative text for the image (required for accessibility)
3. **sizes**: How the image appears at different viewport sizes (default: "100vw")

### Example Usage

```njk
{# Basic usage #}
{% image "blog/coding-example.jpg", "Code example showing HTML structure", "100vw" %}

{# With specific sizes attribute #}
{% image "blog/diagram.jpg", "Architecture diagram", "(min-width: 1024px) 50vw, 100vw" %}
```

## Responsive Images

The image shortcode automatically generates responsive HTML that:

1. Loads the appropriate image size based on the viewport
2. Uses modern formats like WebP when supported
3. Falls back to JPEG/PNG for older browsers
4. Includes width and height attributes to prevent layout shifts

### Generated HTML Example

For a simple image call like:

```njk
{% image "blog/example.jpg", "Example image", "100vw" %}
```

The shortcode generates:

```html
<picture>
  <source
    type="image/webp"
    srcset="
      /assets/images/optimized/blog/example-xs.webp  320w,
      /assets/images/optimized/blog/example-sm.webp  640w,
      /assets/images/optimized/blog/example-md.webp  768w,
      /assets/images/optimized/blog/example-lg.webp 1024w,
      /assets/images/optimized/blog/example-xl.webp 1280w
    "
    sizes="100vw"
  />
  <source
    type="image/jpeg"
    srcset="
      /assets/images/optimized/blog/example-xs.jpeg  320w,
      /assets/images/optimized/blog/example-sm.jpeg  640w,
      /assets/images/optimized/blog/example-md.jpeg  768w,
      /assets/images/optimized/blog/example-lg.jpeg 1024w,
      /assets/images/optimized/blog/example-xl.jpeg 1280w
    "
    sizes="100vw"
  />
  <img
    src="/assets/images/optimized/blog/example-xs.jpeg"
    alt="Example image"
    class="w-full h-auto object-cover"
    loading="lazy"
    decoding="async"
    width="1600"
    height="900"
  />
</picture>
```

## Image Best Practices

1. **Always provide alt text** - Describe what the image shows for accessibility
2. **Use appropriate sizes** - Blog post images should be 1600px wide (16:9 ratio)
3. **Optimize before uploading** - Run images through the optimizer
4. **Use descriptive filenames** - Names should reflect the content
5. **Set appropriate sizes attribute** - Use "100vw" for full-width images or more specific sizes for contained images
6. **Keep file sizes reasonable** - Aim for under 250KB per original image
7. **Prefer modern formats** - Use JPG/PNG initially, the optimizer will create WebP versions
8. **Use topic-specific images** - For general topics, use the pre-made topic images in `assets/images/blog/topics/`

### Image Formats

- **JPG**: Photographs and images with gradients
- **PNG**: Graphics, diagrams, images with transparency
- **WebP**: Modern format that combines advantages of both (automatically created by the optimizer)

### Recommended Image Dimensions

| Usage           | Dimensions | Aspect Ratio |
| --------------- | ---------- | ------------ |
| Blog header     | 1600×900px | 16:9         |
| General content | 1200×675px | 16:9         |
| Topic icon      | 512×512px  | 1:1          |
| Thumbnail       | 400×225px  | 16:9         |

## Further Resources

- [Web.dev Guide to Images](https://web.dev/learn/images/)
- [MDN Guide to Responsive Images](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images)
- [Free Image Sources](https://unsplash.com/) (remember to credit the author)
