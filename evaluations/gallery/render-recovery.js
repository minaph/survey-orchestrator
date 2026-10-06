async page => {
  const root = '/Users/minaph/Projects/survey-orchestrator/evaluations/gallery';
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.emulateMedia({ media: 'screen' });
  await page.goto('http://127.0.0.1:8765/assets/survey-slide-templates.html');
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => [...document.images].every(image => image.complete));
  const inspect = () => [...document.querySelectorAll('.case')].map(item => {
    const stage = item.querySelector('.stage');
    const box = stage.getBoundingClientRect();
    const overflow = [...stage.querySelectorAll('*')].flatMap(element => {
      const bounds = element.getBoundingClientRect();
      if (!bounds.width || !bounds.height) return [];
      const excess = {
        left: box.left - bounds.left,
        right: bounds.right - box.right,
        bottom: bounds.bottom - box.bottom,
      };
      if (Object.values(excess).every(value => value <= 1)) return [];
      return [{ tag: element.tagName, class: element.className, text: element.textContent.slice(0, 100), excess }];
    });
    return {
      id: item.id,
      stage: { width: box.width, height: box.height },
      overflow,
      images: [...stage.querySelectorAll('img')].map(image => ({
        source: image.getAttribute('src'), complete: image.complete,
        naturalWidth: image.naturalWidth, naturalHeight: image.naturalHeight,
        loaded: image.complete && image.naturalWidth > 0,
      })),
    };
  });
  const screen = await page.evaluate(inspect);
  for (const item of screen) {
    await page.locator(`#${item.id} .stage`).screenshot({ path: `${root}/screen/${item.id}.png` });
  }
  await page.setViewportSize({ width: 390, height: 844 });
  await page.evaluate(() => document.fonts.ready);
  const mobile = await page.evaluate(() => ({
    viewport: innerWidth,
    documentWidth: document.documentElement.scrollWidth,
    bodyWidth: document.body.scrollWidth,
    overflow: document.documentElement.scrollWidth > innerWidth,
  }));
  await page.screenshot({ path: `${root}/mobile-390.png` });
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.fonts.ready);
  const print = await page.evaluate(inspect);
  await page.pdf({ path: `${root}/survey-slide-templates.pdf`, preferCSSPageSize: true, printBackground: true });
  await page.emulateMedia({ media: 'screen' });
  return {
    generatedAt: new Date().toISOString(),
    url: page.url(),
    browser: await page.evaluate(() => navigator.userAgent),
    viewport: { width: 1440, height: 1000 },
    screen, mobile, print,
  };
}
