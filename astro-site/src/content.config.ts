import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const imageObjectSchema = z.object({
  url: z.string().optional(),
  src: z.string().optional(),
  alt: z.string().optional(),
  caption: z.string().optional(),
  width: z.number().optional(),
  height: z.number().optional(),
}).passthrough();

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../src/posts' }),
  schema: z
    .object({
      title: z.string(),
      date: z.coerce.date(),
      description: z.string().optional().default(''),
      tags: z.array(z.string()).optional().default([]),
      image: z.union([z.string(), imageObjectSchema]).optional(),
      imageAlt: z.string().optional(),
      images: z
        .object({
          hero: imageObjectSchema.optional(),
          inline: z.union([z.array(imageObjectSchema), z.array(z.never())]).optional(),
          og: imageObjectSchema.optional(),
        })
        .optional(),
      author: z.string().optional().default('William Zujkowski'),
      lastUpdate: z.coerce.date().optional(),
      draft: z.boolean().optional().default(false),
      post_type: z.string().optional(),
    })
    .passthrough(),
});

export const collections = { posts };
