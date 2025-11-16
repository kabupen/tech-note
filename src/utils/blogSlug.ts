// src/utils/blogSlug.ts

/**
 * Content entry の id から URL 用 slug を取り出す
 *
 * id の例:
 *  - "a7f98074dcf416/index.mdx"
 *  - "2024/12/a7f98074dcf416/index.mdx"
 *  - "a7f98074dcf416"
 *  - "2024/12/a7f98074dcf416"
 */
export function getBlogSlugFromId(id: string): string {
  const parts = id.split("/").filter(Boolean); // 空要素除去
  if (parts.length === 0) return id;

  const last = parts[parts.length - 1];

  // 拡張子を落とす
  const withoutExt = last.replace(/\.(md|mdx)$/i, "");

  // フォルダ/index.mdx → フォルダ名を slug にする
  if (withoutExt === "index" && parts.length > 1) {
    return parts[parts.length - 2];
  }

  return withoutExt || id;
}
