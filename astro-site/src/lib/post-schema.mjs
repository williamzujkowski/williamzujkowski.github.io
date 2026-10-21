import { z } from 'astro/zod';
import { RETIRED_TAGS, TAG_SLUG } from './tag-taxonomy.mjs';

// A retired tag would rebuild a /tags/<old>/ page on top of its redirect and
// re-split the archive it was merged out of; name the replacement instead.
const tag = z.string()
  .regex(TAG_SLUG, { error: 'tags are lowercase kebab-case slugs' })
  .refine((value) => !Object.hasOwn(RETIRED_TAGS, value), {
    error: (issue) => {
      const target = RETIRED_TAGS[issue.input];
      return `tag "${issue.input}" is retired; use ${target === null ? 'a canonical tag' : `"${target}"`} (src/lib/tag-taxonomy.mjs)`;
    },
  });

// Keep legacy metadata such as reading_time and readingTime. Fields used by
// publication are validated here; moving the schema must not tighten coercion.
export const postSchema = z.looseObject({
  title: z.string(),
  date: z.coerce.date(),
  description: z.string().optional(),
  tags: z.array(tag).optional().default([]),
  author: z.string().optional().default('William Zujkowski'),
  lastUpdate: z.coerce.date().optional(),
  draft: z.boolean().optional().default(false),
  post_type: z.string().optional(),
  series: z.string().optional(),
  seriesOrder: z.number().optional(),
});
