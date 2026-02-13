import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const blog = defineCollection({
  // Load Markdown and MDX files in the `src/content/blog/` directory.
  loader: glob({ base: "./src/content/blog", pattern: "**/*.{md,mdx}" }),
  // Type-check frontmatter using a schema
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string(),
      // Transform string to Date object
      pubDate: z.coerce.date(),
      updatedDate: z.coerce.date().optional(),
      heroImage: image().optional(),
      tags: z.array(z.string()).default([]),
      categories: z.array(z.string()).default([]),
    }),
  slug: ({ id, defaultSlug }) => {
    const parts = id.split("/");

    // 末尾が index.mdx / index.md でディレクトリ付きの場合は、その一つ前を slug にする
    if (parts.length >= 2 && /^index\.mdx?$/.test(parts[parts.length - 1])) {
      return parts[parts.length - 2]; // "a7f98074dcf416" など
    }

    // それ以外（blog 直下の using-mdx.mdx など）は Astro のデフォルト slug を使う
    return defaultSlug;
  },
});

const study = defineCollection({
  loader: glob({ base: "./src/content/study", pattern: "**/*.{md,mdx}" }),
  schema: () =>
    z.object({
      title: z.string(),
      pubDate: z.coerce.date(),
      tags: z.array(z.string()).default([]),
      categories: z.array(z.string()).default([]),
    }),
  slug: ({ id, defaultSlug }) => {
    if (/\/index\.mdx?$/.test(id)) {
      return id.replace(/\/index\.mdx?$/, "");
    }
    return defaultSlug;
  },
});

export const collections = { blog, study };
