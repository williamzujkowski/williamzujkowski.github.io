# Optimized CSS Structure

This directory contains the optimized CSS structure for the website. The CSS has been modularized for better maintenance and performance.

## Files Structure

- **main.css**: The main entry point that imports all other CSS files
- **theme.css**: Contains all theme variables and color definitions
- **base.css**: Contains base element styles and typography
- **components.css**: Contains all UI component styles
- **utilities.css**: Contains utility classes
- **mobile.css**: Contains responsive overrides for mobile devices

## How to Use

Instead of importing the old CSS files, import the main.css file which will import all the necessary components:

```html
<link rel="stylesheet" href="/css/optimized/main.css">
```

## Benefits

- **Modular**: Each file has a specific purpose
- **Maintainable**: Easier to find and update specific styles
- **Performant**: Better organization leads to fewer specificity conflicts
- **Consistent**: Similar components use consistent styling patterns

## Legacy Files

The original CSS files are still available in the parent directory for reference. Once the optimized structure is working correctly, the legacy files can be removed.
