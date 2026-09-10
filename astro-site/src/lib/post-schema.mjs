import { z } from 'astro/zod';

// Keep legacy metadata such as reading_time and readingTime. Fields used by
// publication are validated here; moving the schema must not tighten coercion.
export const postSchema = z.looseObject({
  title: z.string(),
  date: z.coerce.date(),
  description: z.string().optional(),
  tags: z.array(z.string()).optional().default([]),
  author: z.string().optional().default('William Zujkowski'),
  lastUpdate: z.coerce.date().optional(),
  draft: z.boolean().optional().default(false),
  post_type: z.string().optional(),
  series: z.string().optional(),
  seriesOrder: z.number().optional(),
});
