// @ts-check

import { defineConfig } from "astro/config";

import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";

import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

import tailwindcss from "@tailwindcss/vite";

import { remarkInlineFootnote } from "./src/utils/remarkInlineFootnote.js";

// https://astro.build/config
export default defineConfig({
  // site は 1 箇所だけにする
  site: "https://kabupen.com",

  integrations: [
    mdx(), // MDX
    sitemap(), // サイトマップ
  ],

  markdown: {
    remarkPlugins: [
      remarkMath, // 数式用
      remarkInlineFootnote, // NOTE: remarkMath より必ず後ろで定義
    ],
    rehypePlugins: [rehypeKatex],
  },

  vite: {
    plugins: [tailwindcss()],
  },
});
