const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1052, height: 272 }, deviceScaleFactor: 1 })).newPage();
  let svg = fs.readFileSync('dl/im8logo.svg', 'utf8').replace(/#FF9693/g, '#8E1B2C');
  await p.setContent(`<body style="margin:0;background:transparent">${svg}</body>`); await p.waitForTimeout(300);
  await p.screenshot({ path: 'dl/im8logo.png', omitBackground: true }); await b.close(); })();
