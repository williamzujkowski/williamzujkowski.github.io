import { test } from 'node:test';
import assert from 'node:assert/strict';
import { renderPostForFeed } from '../../astro-site/src/lib/feedContent.ts';

const site = 'https://example.org/';
const render = (body) => renderPostForFeed(body, site);

test('feed diagrams expose layer labels and separate adjacent chips without CSS', () => {
  const html = render(`<figure class="arch-fig">
<div class="arch" aria-label="Vault architecture">
<section class="arch-tier" data-label="Client &amp; Access"><span class="arch-chip"><b>Web</b><i>browser</i></span><span class="arch-chip">Mobile</span></section>
<section class="arch-tier" data-label="Storage">Direct tier text<span class="arch-chip">Database</span></section>
</div>
<figcaption>Clients enter through the edge.</figcaption>
</figure>`);
  assert.match(html, /<figure>/);
  assert.match(html, /<strong>Client &amp; Access<\/strong>/);
  assert.match(html, /<div><b>Web<\/b> <i>browser<\/i><\/div><div>Mobile<\/div>/);
  assert.match(html, /<strong>Storage<\/strong>[\s\S]*Direct tier text[\s\S]*Database/);
  assert.match(html, /<figcaption>Clients enter through the edge\.<\/figcaption>/);
  assert.doesNotMatch(html, /&lt;(?:div|section)|data-|class=|style=/);
});

test('feed flow branches keep labels, nesting and source order', () => {
  const html = render(`<div class="flow">
<div class="flow-node">Scan</div>
<div class="flow-parallel" aria-label="Runs in parallel"><div class="flow-node">OSV</div><div class="flow-node">Trivy</div></div>
<div class="flow-branch"><div class="flow-leg" data-branch="Pass"><div class="flow-node">Deploy</div></div><div class="flow-leg" data-branch="Fail"><div class="flow-node">Block</div></div></div>
</div>`);
  assert.match(html, /Scan[\s\S]*Runs in parallel[\s\S]*OSV[\s\S]*Trivy[\s\S]*<strong>Pass<\/strong>[\s\S]*Deploy[\s\S]*<strong>Fail<\/strong>[\s\S]*Block/);
});

test('feed sequence actors remain separated from their messages', () => {
  const html = render('<ol class="seq"><li class="seq-step"><b>Client &rarr; Server</b><span>Request</span></li><li class="seq-label">Else</li></ol>');
  assert.match(html, /<b>Client → Server<\/b> <span>Request<\/span>/);
  assert.match(html, /<li>Else<\/li>/);
});

test('feed drops decorative CSS doodles while retaining captions', () => {
  const html = render('<div class="zine-doodle" aria-hidden="true" style="background:url(/art.png)"></div>\n<p class="hand-note">A temperamental API.</p>');
  assert.doesNotMatch(html, /<div|style|art\.png|zine-doodle/);
  assert.match(html, /<p>A temperamental API\.<\/p>/);
});

test('feed keeps fenced and inline HTML examples literal', () => {
  const source = '<div class="arch-tier" data-label="Example">literal</div>';
  const html = render('```html\n' + source + '\n```\n\n`' + source + '`');
  assert.match(html, /<pre><code>&lt;div class="arch-tier" data-label="Example"&gt;literal&lt;\/div&gt;\n<\/code><\/pre>/);
  assert.match(html, /<p><code>&lt;div/);
  assert.doesNotMatch(html, /<strong>Example|<div/);
});

test('feed sanitizes active HTML, attributes and unsafe URLs after rendering', () => {
  const html = render(`<script>alert('script')</script>
<style>body { display:none }</style>
<iframe src="https://evil.example/">embed</iframe>
<svg><a href="javascript:alert(1)">SVG</a></svg>
<p onclick="alert(1)" style="color:red"><a href="jav&#x61;script:alert(1)">unsafe</a><a href="https://example.net/?a=1&amp;b=2">safe</a></p>
<img src="data:text/html,boom" onerror="alert(1)">
<img src="/image.png" alt="Example" onload="alert(1)">`);
  assert.doesNotMatch(html, /<(?:script|style|iframe|svg)\b|\s(?:on\w+|style)=|(?:href|src)="(?:javascript|data):|alert\(/);
  assert.match(html, /href="https:\/\/example\.net\/\?a=1&amp;b=2"/);
  assert.match(html, /src="https:\/\/example\.org\/image\.png" alt="Example"/);
});

test('diagram labels are escaped text, including entities and tag-shaped payloads', () => {
  const html = render('<section class="arch-tier" data-label="&lt;img src=x onerror=boom&gt; &amp; &quot;quoted&quot;">Keep me</section>');
  assert.match(html, /<strong>&lt;img src=x onerror=boom&gt; &amp; "quoted"<\/strong>/);
  assert.match(html, /Keep me/);
  assert.doesNotMatch(html, /<img|data-feed/);
});

test('feed retains citations, footnote targets and absolute site links', () => {
  const html = render('See [post](/posts/example/) and evidence[^source].\n\n[^source]: [Study](https://example.net/study).');
  assert.match(html, /href="https:\/\/example\.org\/posts\/example\/"/);
  assert.match(html, /href="#fn1"/);
  assert.match(html, /id="fn1"/);
  assert.match(html, /href="#fnref1"/);
  assert.match(html, /id="fnref1"/);
  assert.match(html, /href="https:\/\/example\.net\/study"/);
  assert.doesNotMatch(html, /\[\^source\]/);
});


test('feed absolutizes parsed attributes without rewriting literal URL examples', () => {
  const example = '<a href="/posts/example/">post</a><img src="/image.png">';
  const html = render('```html\n' + example + '\n```\n\n' + example);
  const code = html.match(/<code>([\s\S]*?)<\/code>/)[1];
  assert.match(code, /href="\/posts\/example\/"/);
  assert.match(code, /src="\/image\.png"/);
  assert.doesNotMatch(code, /example\.org/);
  assert.match(html, /<a href="https:\/\/example\.org\/posts\/example\/">post<\/a>/);
  assert.match(html, /<img src="https:\/\/example\.org\/image\.png"/);
});

test('feed label normalization handles HTML attribute syntax and ignores forged markers', () => {
  const html = render(`<SECTION CLASS='arch-tier is-stack' DATA-LABEL='Layer &amp; one'>First</SECTION>
<div class=flow-leg data-branch=Pass>Second</div>
<div data-feed-label="Forged">Third</div>
<div class="flow-leg" data-branch="&amp;lt;script&amp;gt;literal&amp;lt;/script&amp;gt;">Fourth</div>`);
  assert.match(html, /<strong>Layer &amp; one<\/strong>[\s\S]*First/);
  assert.match(html, /<strong>Pass<\/strong>[\s\S]*Second/);
  assert.match(html, /<div>Third<\/div>/);
  assert.match(html, /<strong>&amp;lt;script&amp;gt;literal&amp;lt;\/script&amp;gt;<\/strong>/);
  assert.doesNotMatch(html, /Forged|data-feed-label|<script/);
});


test('feed diagram spacing leaves ordinary inline prose unchanged', () => {
  const html = render('The word <b>micro</b><i>services</i> stays whole.\n\n<div class="flow-node"><b>Scan</b><i>dependencies</i></div>\n\n<b>news</b><span>paper</span>');
  assert.match(html, /<b>micro<\/b><i>services<\/i>/);
  assert.match(html, /<b>Scan<\/b> <i>dependencies<\/i>/);
  assert.match(html, /<b>news<\/b><span>paper<\/span>/);
  assert.doesNotMatch(html, /data-feed-detail/);
});


test('removing a doodle preserves following sibling closing tags and text', () => {
  assert.equal(render('<div class="zine-doodle"></div>\n<h2>Heading</h2>\n<p>Normal paragraph</p>'), '\n<h2>Heading</h2>\n<p>Normal paragraph</p>');
  assert.equal(render('<div><div class="zine-doodle"><span>Hidden decoration</span></div><b>Bold</b><i>Italic</i></div>'), '<div><b>Bold</b><i>Italic</i></div>');
  assert.equal(render('<div data-feed-doodle="true">Keep ordinary content</div>'), '<div>Keep ordinary content</div>');
});
