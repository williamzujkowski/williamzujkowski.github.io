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

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../src/projects' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    url: z.string(),
    category: z.enum(['ai', 'security', 'infrastructure', 'tools']),
    tags: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    status: z.enum(['active', 'experimental', 'archived']).default('active'),
    order: z.number().default(99),
  }),
});

export const collections = { posts, projects };
