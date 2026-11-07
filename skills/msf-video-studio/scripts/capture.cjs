#!/usr/bin/env node
// Optional capture from a local, authorized training fixture. Playwright >= 1.48.
"use strict";
const fs = require("node:fs/promises");
const path = require("node:path");

async function capture() {
  const [config, destination] = process.argv.slice(2);
  if (!config || !destination) throw Error("Usage: node capture.cjs capture.json output-dir");
  const plan = JSON.parse(await fs.readFile(config, "utf8"));
  if (!["synthetic", "approved_sanitized"].includes(plan.asset_scope)) {
    throw Error("Review the local fixture and set asset_scope before capture");
  }
  const url = new URL(plan.url);
  if (url.protocol !== "http:" || !["localhost", "127.0.0.1", "[::1]"].includes(url.hostname) ||
      url.username || url.password || url.search || url.hash) {
    throw Error("Use a plain HTTP URL on a loopback training server without credentials or query parameters");
  }
  if (!Array.isArray(plan.steps) || !plan.steps.length || plan.steps.length > 30) {
    throw Error("Supply 1–30 capture steps");
  }
  if (plan.locale !== undefined && !["en", "ar"].includes(plan.locale)) {
    throw Error("locale must be en or ar");
  }
  const fileNames = new Set();
  for (const step of plan.steps) {
    if (!step || typeof step.file !== "string" || !/^[a-z0-9][a-z0-9_-]*\.png$/.test(step.file) ||
        fileNames.has(step.file) ||
        (step.click !== undefined && (typeof step.click !== "string" || !step.click)) ||
        (step.select !== undefined && (!step.select || typeof step.select.locator !== "string" ||
           !step.select.locator || typeof step.select.value !== "string")) ||
        (step.wait_for !== undefined && (typeof step.wait_for !== "string" || !step.wait_for)) ||
        (step.hold_ms !== undefined && (!Number.isInteger(step.hold_ms) ||
           step.hold_ms < 0 || step.hold_ms > 10000))) {
      throw Error("Each step needs a unique lowercase PNG filename and valid optional selectors/hold");
    }
    fileNames.add(step.file);
  }
  if (plan.record_video !== undefined && typeof plan.record_video !== "boolean") {
    throw Error("record_video must be a boolean");
  }
  const out = path.resolve(destination);
  const { chromium } = require("playwright");
  const parent = path.dirname(out);
  await fs.mkdir(parent, { recursive: true });
  const temp = await fs.mkdtemp(path.join(parent, "training-capture-"));
  let browser;
  let context;
  try {
    browser = await chromium.launch({ headless: true, executablePath: process.env.MSF_CHROMIUM_PATH || undefined });
    const viewport = { width: 1920, height: 1080 };
    context = await browser.newContext({
      viewport, locale: plan.locale === "ar" ? "ar" : "en-US", deviceScaleFactor: 1, acceptDownloads: false, serviceWorkers: "block",
      ...(plan.record_video ? { recordVideo: { dir: temp, size: viewport } } : {}),
    });
    await context.route("**/*", async route => {
      const request = new URL(route.request().url());
      if (request.origin !== url.origin) return route.abort("blockedbyclient");
      // Do not let even a loopback response redirect the browser off the fixture.
      const response = await route.fetch({ maxRedirects: 0, timeout: 10000 });
      if (response.status() >= 300 && response.status() < 400) {
        return route.abort("blockedbyclient");
      }
      await route.fulfill({ response });
    });
    await context.routeWebSocket("**/*", socket => socket.close());
    const page = await context.newPage();
    page.setDefaultTimeout(10000);
    await page.goto(url.href, { waitUntil: "domcontentloaded", timeout: 15000 });
    if (new URL(page.url()).origin !== url.origin) throw Error("Navigation left the fixture origin");
    for (const step of plan.steps) {
      if (step.click) await page.locator(step.click).click();
      if (step.select) await page.locator(step.select.locator).selectOption(step.select.value);
      if (step.wait_for) await page.locator(step.wait_for).waitFor({ state: "visible" });
      if (step.hold_ms) await page.waitForTimeout(step.hold_ms);
      await page.screenshot({ path: path.join(temp, step.file), animations: "disabled" });
    }
    const video = page.video();
    await context.close();
    context = null;
    if (video) await fs.rename(await video.path(), path.join(temp, "capture.webm"));
    // Refuse to overwrite a previous capture.
    await fs.mkdir(out);
    for (const file of await fs.readdir(temp)) {
      await fs.rename(path.join(temp, file), path.join(out, file));
    }
    process.stdout.write(`Captured ${plan.steps.length} screen states in ${out}\n`);
  } finally {
    try {
      if (context) await context.close();
      if (browser) await browser.close();
    } finally {
      await fs.rm(temp, { recursive: true, force: true });
    }
  }
}

capture().catch(error => {
  process.stderr.write(`Capture failed: ${error.message}\n`);
  process.exitCode = 1;
});
