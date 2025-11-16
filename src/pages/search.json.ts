// src/pages/search.json.ts
import type { APIRoute } from "astro";
import { getCollection } from "astro:content";

export const GET: APIRoute = async () => {
  const posts = await getCollection("blog", ({ data }) => !data.draft);

  const docs = posts.map((post) => {
    const rawId = post.id as string; // 例: "my-post.md" / "blog/my-post.md" など
    const last = rawId.split("/").at(-1) ?? rawId;
    let slug = last.replace(/\.(md|mdx)$/i, "");

    return {
    url: `/blog/${slug}/`,
    title: post.data.title,
    description: post.data.description ?? "",
    body: post.body,
    }
  });

  return new Response(JSON.stringify(docs), {
    status: 200,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
    },
  });
};
