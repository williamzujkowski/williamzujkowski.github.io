// Lazy entry for the search dialog: imported by SearchTrigger.astro on first
// use, so this module, the Svelte runtime and Search.svelte's CSS stay out of
// every page's initial load (#661).
import { mount } from 'svelte';
import Search from './Search.svelte';

export interface SearchDialog {
  open: (from?: HTMLElement | null) => Promise<void>;
}

export function mountSearch(target: HTMLElement, trigger: HTMLElement): SearchDialog {
  return mount(Search, { target, props: { trigger } }) as SearchDialog;
}
