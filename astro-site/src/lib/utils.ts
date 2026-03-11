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
 * Calculate reading time from text content.
 */
export function getReadingTime(body: string): number {
  const words = body.split(/\s+/).length;
  return Math.ceil(words / 225);
}
