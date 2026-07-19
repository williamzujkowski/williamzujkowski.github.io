/**
 * Calculate reading time from text content.
 */
export function getReadingTime(body: string): number {
  const words = body.split(/\s+/).length;
  return Math.ceil(words / 225);
}
