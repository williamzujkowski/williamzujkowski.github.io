import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../src/posts' }),
  schema: z
    .object({
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
    })
    .passthrough(),
});

// The `projects` collection was orphaned — nothing ever called
// getCollection('projects'), so its markdown never rendered (the /projects
// page is hand-authored in pages/projects.astro). Removed with its 10 source
// files (#360) to kill the stale-data trap; the hand-written page is the
// single source of truth.
export const collections = { posts };
