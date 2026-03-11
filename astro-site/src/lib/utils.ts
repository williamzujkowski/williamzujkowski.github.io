import { existsSync } from 'node:fs';
import { resolve, join } from 'node:path';

/**
 * Extract image URL from post data.
 * Handles both string images and object images (with url property).
 */
export function getImageUrl(
  image: string | { url?: string; src?: string } | undefined
): string | undefined {
  if (!image) return undefined;
  if (typeof image === 'string') return image;
  return image.url ?? image.src;
}

/**
 * Check if a local image path exists in the public directory.
 * External URLs (http/https) are assumed valid.
 * Returns the URL if valid, undefined if the local file is missing.
 * This runs at build time in Astro's Node.js context.
 */
export function getValidImageUrl(
  image: string | { url?: string; src?: string } | undefined
): string | undefined {
  const url = getImageUrl(image);
  if (!url) return undefined;
  // External URLs are assumed valid
  if (url.startsWith('http://') || url.startsWith('https://')) return url;
  // Local paths: check if file exists in public directory at build time
  // Guard against path traversal (e.g., ../../etc/passwd)
  try {
    const publicDir = resolve(process.cwd(), 'public');
    const filePath = resolve(publicDir, url.replace(/^\//, ''));
    if (!filePath.startsWith(publicDir)) return undefined;
    if (existsSync(filePath)) return url;
  } catch {
    return undefined;
  }
  return undefined;
}

/**
 * Calculate reading time from text content.
 */
export function getReadingTime(body: string): number {
  const words = body.split(/\s+/).length;
  return Math.ceil(words / 225);
}
