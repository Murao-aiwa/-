const { chromium } = require('playwright');
// usage: node render.js in.svg out.png width height scale
(async () => {
  const [inp, out, w, h, sc] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +sc });
  await p.goto('file://' + inp);
  await p.waitForTimeout(300);
  await p.screenshot({ path: out, clip: { x: 0, y: 0, width: +w, height: +h } });
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
