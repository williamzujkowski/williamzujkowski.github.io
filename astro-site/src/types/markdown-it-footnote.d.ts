// markdown-it-footnote ships no type declarations. It is a plain markdown-it
// plugin, so the only shape we need is "something you can pass to .use()".
declare module 'markdown-it-footnote' {
  import type MarkdownIt from 'markdown-it';
  const footnotePlugin: MarkdownIt.PluginSimple;
  export default footnotePlugin;
}
