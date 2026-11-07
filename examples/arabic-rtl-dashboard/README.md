# Mirsad: Arabic RTL shipment dashboard

[العربية](README.ar.md) · [Visual workflow](VISUAL.md)

Mirsad is a local, standalone example for dispatch operators reviewing synthetic shipments. Arabic RTL is the default; the language switch changes the document language and direction without resetting the active filters. Light and dark modes share the same semantic colors. The example has no API, accounts, analytics, or CDN assets.

## Run and try it

From this directory, start a local static server and open `http://127.0.0.1:8080`:

```sh
python -m http.server 8080 --bind 127.0.0.1
```

- Open **View delayed shipments** to narrow the ledger to the exception, then open its details.
- Search by an Arabic or English item name, a hub, or a reference such as `MC-4182`. The hub filter has its own searchable, keyboard-operable picker.
- Change the date sort, browse both pages, then switch language and theme. A search with no matches explains how to recover.
- With only a keyboard, use the skip link, Tab, Enter, and Escape. The dialog returns focus to its opener. On mobile, scroll the table region if a column is offscreen.

## Verify

```sh
node --test model.test.mjs
node --check app.mjs
```

Run the optional browser check against the local server. Install Playwright and its Chromium locally first:

```sh
npm install --no-save playwright
npx playwright install chromium
node browser.mjs
```

To write screenshots outside the project, set `DASHBOARD_SHOTS` to an absolute folder. If the server is on another port, set `DASHBOARD_URL`. The browser check covers RTL and LTR, theme switching, keyboard focus and dialog dismissal, filters and empty states, sort, pagination, and mobile overflow.

## Skill routing

Use `msf-orchestrator` and `msf-planning` to identify the operator's main task and plan the checks; use `msf-ui-ux` for the design and state decisions in [VISUAL.md](VISUAL.md); use `msf-frontend` to build the locale, theme and interaction behavior; use `msf-testing` for the model/browser checks and `msf-documentation` for bilingual setup and QA. Append `-ar` for the Arabic counterparts.
