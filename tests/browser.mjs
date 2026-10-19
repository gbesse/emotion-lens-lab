import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import assert from 'node:assert/strict';
import { mkdir, readFile } from 'node:fs/promises';
const port = 18771,
  base = `http://127.0.0.1:${port}`,
  server = spawn(process.env.PYTHON || 'python3', ['-m', 'emotion_lens', 'serve', String(port)], {
    stdio: ['ignore', 'pipe', 'inherit'],
  });
let browser;
try {
  for (let i = 0; i < 100; i++) {
    try {
      if ((await fetch(base)).ok) break;
    } catch {}
    if (server.exitCode !== null) throw Error('server exited');
    if (i === 99) throw Error('server timeout');
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1400, height: 1200 } }),
    errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  for (const lang of ['fr', 'en', 'es']) {
    await page.goto(`${base}/?lang=${lang}`);
    await page.locator('#demo').click();
    await page.waitForFunction(() => document.getElementById('readers').textContent === '2');
    assert.equal(await page.locator('html').getAttribute('lang'), lang);
    assert.equal(await page.locator('#coverage').textContent(), '7/8');
    assert.equal(await page.locator('.passage').count(), 4);
    assert.equal(await page.locator('#disagreement').textContent(), '0.65');
    const expected = await page.locator('[data-segment=p2] > p').first().textContent();
    let event = page.waitForEvent('download');
    await page.locator('#markdown').click();
    const md = await event;
    const content = await readFile(await md.path(), 'utf8');
    assert.ok(content.includes(expected));
    assert.ok(content.includes('^'));
    await page.locator('#observer').fill('new-reader');
    await page.locator('#score-fear').fill('0.95');
    await page.locator('#save').click();
    await page.waitForFunction(() => document.getElementById('readers').textContent === '3');
    assert.equal(await page.locator('#coverage').textContent(), '8/12');
    event = page.waitForEvent('download');
    await page.locator('#svg').click();
    assert.equal((await event).suggestedFilename(), 'emotion-arc.svg');
  }
  await page.locator('#import').setInputFiles('docs/live-text-annotations.json');
  await page.waitForFunction(() => document.querySelectorAll('.layer').length === 18);
  assert.equal(await page.locator('#document-language').inputValue(), 'fr');
  assert.equal(await page.locator('#coverage').textContent(), '7/8');
  await page
    .locator('#input')
    .fill('Été 🛰️ <script>window.injected=true</script>.\n\nSecond passage.');
  await page.locator('#document-language').selectOption('fr');
  await page.locator('#replace').click();
  await page.waitForFunction(() => document.querySelectorAll('.passage').length === 2);
  assert.equal(await page.evaluate(() => window.injected), undefined);
  assert.ok((await page.locator('.passage').first().textContent()).includes('<script>'));
  await page.goto(`${base}/?lang=en`);
  await page.waitForFunction(() => document.querySelectorAll('.passage').length === 2);
  assert.equal(await page.locator('#document-language').inputValue(), 'fr');
  assert.ok((await page.locator('#input').inputValue()).startsWith('Été 🛰️'));
  await page.locator('#demo').click();
  await page.waitForFunction(() => document.querySelectorAll('.passage').length === 4);
  await mkdir('.local', { recursive: true });
  await page.screenshot({ path: '.local/preview-en.png', fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  assert.deepEqual(errors, []);
  assert.equal((await fetch(`${base}/.env`)).status, 404);
  console.log(
    'FR/EN/ES: perspective separation, disagreement, annotations, Obsidian/SVG exports, Unicode, text preservation, injection and mobile verified.',
  );
} finally {
  if (browser) await browser.close();
  server.kill('SIGTERM');
}
