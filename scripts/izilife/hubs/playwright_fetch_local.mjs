import { pathToFileURL } from 'node:url';
import { existsSync } from 'node:fs';

const [modulePath, url, waitRaw, scrollRaw] = process.argv.slice(2);
const { chromium } = await import(pathToFileURL(modulePath).href);
const candidates = [process.env.PLAYWRIGHT_CHROME_BIN, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'].filter(Boolean);
const executablePath = candidates.find(existsSync);
const browser = await chromium.launch({headless:true, executablePath, args:['--disable-blink-features=AutomationControlled']});
try {
  const context = await browser.newContext({locale:'fr-FR', timezoneId:'Europe/Paris', viewport:{width:1440,height:1000}});
  const page = await context.newPage();
  await page.goto(url, {waitUntil:'domcontentloaded', timeout:90000});
  await page.waitForTimeout(Math.max(0, Number(waitRaw)||2500));
  for (let i=0; i<Math.max(0, Number(scrollRaw)||0); i++) {
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(800);
  }
  process.stdout.write(await page.content());
} finally {
  await browser.close();
}
