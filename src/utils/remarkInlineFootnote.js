// src/utils/remarkInlineFootnote.js
// @ts-check

import { visit } from "unist-util-visit";

/**
 * インライン脚注:
 *   本文:  線形回帰モデル^[入力変数 $x$ ...]では
 *
 * - 本文中: <sup class="footnote-ref"><a id="fnref-1" href="#fn-1">[1]</a></sup>
 * - 文末: 「脚注」見出し + ordered list
 * - 脚注本文は text / inlineMath などのノード列として保持する
 *   → すでに remark-math 済みの inlineMath ノードも含めてそのままコピーされる
 */
export function remarkInlineFootnote() {
  /**
   * @param {import('mdast').Root} tree
   */
  return (tree) => {
    /** @type {Array<{ id: number; children: import('mdast').PhrasingContent[] }>} */
    const footnotes = [];
    let counter = 0;

    /** 単純なディープコピー */
    const cloneNode = (node) =>
      /** @type {any} */ (JSON.parse(JSON.stringify(node)));

    visit(tree, "paragraph", (paragraph) => {
      /** @type {import('mdast').PhrasingContent[]} */
      const newChildren = [];

      /** 現在脚注の中かどうか */
      let inFootnote = false;
      /** 現在処理中の脚注 ID */
      let currentId = 0;
      /** 現在処理中の脚注本文ノード列 */
      /** @type {import('mdast').PhrasingContent[]} */
      let currentFootnoteNodes = [];

      const children = paragraph.children;

      for (let childIndex = 0; childIndex < children.length; childIndex++) {
        const child = children[childIndex];

        // まだ脚注の外
        if (!inFootnote) {
          if (child.type !== "text") {
            // text 以外はそのまま
            newChildren.push(child);
            continue;
          }

          let text = child.value;
          let pos = 0;

          while (pos < text.length) {
            const start = text.indexOf("^[", pos);
            if (start === -1) {
              // もう脚注は出てこない
              if (pos < text.length) {
                newChildren.push({
                  type: "text",
                  value: text.slice(pos),
                });
              }
              break;
            }

            // ^[ より前の部分は通常テキスト
            if (start > pos) {
              newChildren.push({
                type: "text",
                value: text.slice(pos, start),
              });
            }

            // ここから脚注開始
            inFootnote = true;
            currentId = ++counter;
            currentFootnoteNodes = [];

            // ^[ の直後から続きを見る
            pos = start + 2;
            // 続きに ] が含まれているかもしれないので、inFootnote モードで処理させる
            while (inFootnote && pos <= text.length) {
              const end = text.indexOf("]", pos);
              if (end === -1) {
                // このテキストノードの残りは全部脚注本文
                if (pos < text.length) {
                  currentFootnoteNodes.push({
                    type: "text",
                    value: text.slice(pos),
                  });
                }
                // この child の処理は終わり。次の child に進む
                break;
              } else {
                // pos 〜 end が脚注本文として入る
                if (end > pos) {
                  currentFootnoteNodes.push({
                    type: "text",
                    value: text.slice(pos, end),
                  });
                }

                // ここで脚注終了
                footnotes.push({
                  id: currentId,
                  children: currentFootnoteNodes,
                });

                // 本文側に [n] を挿入
                newChildren.push({
                  type: "html",
                  value: `<sup class="footnote-ref"><a id="fnref-${currentId}" href="#fn-${currentId}">[${currentId}]</a></sup>`,
                });

                // 次は通常モードへ
                inFootnote = false;
                currentId = 0;
                currentFootnoteNodes = [];

                // ] の直後から、また通常テキストとして処理
                pos = end + 1;
                // ループを抜けずに、同じテキスト内にさらに ^[ がある場合にも対応
                break;
              }
            }

            // inFootnote のままなら、この child ではこれ以上処理するものはないので break
            if (inFootnote) {
              break;
            }
          }
        } else {
          // inFootnote === true, つまり脚注の中身を読み取っている状態
          if (child.type === "text") {
            let text = child.value;
            let pos = 0;

            while (pos <= text.length) {
              const end = text.indexOf("]", pos);
              if (end === -1) {
                // すべて脚注本文
                if (pos < text.length) {
                  currentFootnoteNodes.push({
                    type: "text",
                    value: text.slice(pos),
                  });
                }
                break;
              } else {
                // pos〜end が脚注本文
                if (end > pos) {
                  currentFootnoteNodes.push({
                    type: "text",
                    value: text.slice(pos, end),
                  });
                }

                // ここで脚注終了
                footnotes.push({
                  id: currentId,
                  children: currentFootnoteNodes,
                });

                // 本文側の [n]
                newChildren.push({
                  type: "html",
                  value: `<sup class="footnote-ref"><a id="fnref-${currentId}" href="#fn-${currentId}">[${currentId}]</a></sup>`,
                });

                inFootnote = false;
                currentId = 0;
                currentFootnoteNodes = [];

                // ] の後ろに残りがあれば通常テキストとして追加
                if (end + 1 < text.length) {
                  newChildren.push({
                    type: "text",
                    value: text.slice(end + 1),
                  });
                }

                break; // この child の処理は終わり
              }
            }
          } else {
            // text 以外（inlineMath など）は、脚注本文としてそのまま取り込む
            currentFootnoteNodes.push(cloneNode(child));
          }
        }
      }

      // paragraph の最後まで来ても inFootnote が true のままなら、
      // 閉じカッコなしの不完全な脚注なので、そのまま潰さず通常テキスト扱いに戻した方が親切だが、
      // とりあえず今回は「閉じなければ脚注にしない」方針で newChildren に戻さないままにする。

      paragraph.children = newChildren;
    });

    if (footnotes.length === 0) {
      return;
    }

    // 文末に脚注セクションを追加
    tree.children.push({
      type: "thematicBreak",
    });

    tree.children.push({
      type: "paragraph",
      children: [
        {
          type: "strong",
          children: [{ type: "text", value: "脚注" }],
        },
      ],
    });

    tree.children.push({
      type: "list",
      ordered: true,
      spread: false,
      children: footnotes.map(({ id, children }) => ({
        type: "listItem",
        spread: false,
        children: [
          {
            type: "paragraph",
            children: [
              ...children,
              {
                type: "html",
                value: ` <a href="#fnref-${id}" id="fn-${id}" class="footnote-backref">↩︎</a>`,
              },
            ],
          },
        ],
      })),
    });
  };
}
