# Worked workflow / مسار عمل تطبيقي

**Request:** “Add an Arabic-first inventory ledger. A reader can find an item; an editor can correct it and archive it with a way to restore it.”

**Example handoff:** Use the English skill IDs below for an English brief, or append `-ar` to each ID for the Arabic counterpart. Inspect the repository conventions before writing; use this example as a reference rather than an instruction to replace established choices.

| Order and skill | Decision made for Raff | Evidence |
| --- | --- | --- |
| 1. `msf-orchestrator`, `msf-planning` | Warehouse staff need list/create/edit/archive/restore. Keep hard delete and production deployment out of scope. Split the work into contract/schema, end-to-end behavior, and QA. | Acceptance cases below |
| 2. `msf-architecture` | Angular owns interaction; the .NET API owns permission and validation; SQL owns data invariants. Angular proxies to the API locally. | [Proxy](web/proxy.conf.json), [API](api/Program.cs), [DDL](sql/001-inventory.sql) |
| 3. `msf-ui-ux`, `msf-frontend` | Start in RTL; keep SKU in its own LTR run. Search names and SKU, search category labels and codes, and explain save errors next to the form. Archive and restore show the consequence before submitting. | [Template](web/src/inventory.html), [copy](web/src/copy.ts) |
| 4. `msf-backend`, `msf-database` | Validate in the API; protect unique SKU even after archive; use Unicode and typed parameters; make writes conditional on the saved row version. | [API](api/Program.cs), [DDL](sql/001-inventory.sql) |
| 5. `msf-security` | Enforce permissions on every API call. Reject reader writes and missing keys; keep demo keys out of code and storage. Bind local listeners to loopback; use SQL table permissions scoped to read and required writes. | [API](api/Program.cs), [runbook](README.md) |
| 6. `msf-testing` | Exercise representative success, failure, and stale-version cases using the real API and database. Review RTL/LTR and keyboard states separately. | [HTTP smoke](tests/smoke.mjs), acceptance cases below |
| 7. `msf-devops`, `msf-documentation` | Separate database setup from API startup; add a database readiness probe and a release/rollback checklist. Provide both language entry points. | [Readiness endpoint](api/Program.cs), [English](README.md), [العربية](README.ar.md) |

## Contract and acceptance

| Scenario | Expected result |
| --- | --- |
| Search Arabic/English name or SKU; choose a category | At most 25 rows, descending ID cursor, literal search; display a clear empty state |
| Create and edit a valid item | `201` on creation; `200` and a new version on update |
| Save with missing data, invalid category, or duplicate SKU | `400` or `409` with stable code, translated into a correction in the form |
| Save with an earlier version | `409 item_conflict`; keep the operator's form open and point to reload |
| Archive and restore | Version changes; item moves between lists without recycling its SKU |
| Missing credentials, or a reader attempting a mutation | `401 sign_in_required` or `403 write_forbidden`; no data changes |
| Keyboard-only and mixed direction | Operable native controls and dialog dismissal, visible focus, isolated SKU, matching RTL/LTR document attributes |

The filter includes both display languages in search; changing interface language does not translate stored values. The 25-row keyset cursor is useful for this example, although an exactly full final page can offer one empty page. Contains-search can scan candidates; benchmark or change indexing before using it at larger scale.

## Release and rollback

- Provision only a disposable database and least-privileged application user. Run the SQL setup with `sqlcmd -b`, then verify API readiness.
- Run `npm ci && npm run build`, `dotnet build api`, and `node tests/smoke.mjs`. Manually review Arabic and English, tab/focus, filters, and the stale error in two sessions.
- Keep a local synthetic snapshot if data needs to survive experimentation. To stop or undo an application change, stop the UI and API, and restart the previous compatible revision. For schema changes in a real system, rehearse a forward correction or backup restore before deployment; do not drop data to roll back the app.
- This example intentionally refuses non-Development startup. An actual release first needs real authentication/authorization, individual audit events, protected secret handling, migration automation, and an operational owner.

## العربية

**الطلب:** إضافة سجل مخزون يبدأ بالعربية. يستطيع القارئ العثور على صنف، ويستطيع المحرر تعديله وأرشفته واستعادته.

1. تبدأ مهارتا التنسيق والتخطيط بتحديد الأدوار وحالات القبول وحدود العمل؛ لا يشمل المثال الحذف النهائي أو النشر.
2. تحدد المعمارية حدود الواجهة والخادم وقاعدة البيانات. تختبر الواجهة اتجاه RTL، والأسماء ثنائية اللغة، والبحث في الفئات، ورسائل الخطأ التي توضّح الإجراء التالي.
3. يفرض الخادم الصلاحيات ويتحقق من المدخلات، وتفرض قاعدة البيانات تفرد الرمز وصحة الفئة والكمية. يمنع رقم النسخة تعديل بيانات أصبحت قديمة.
4. يغطي اختبار HTTP المنع والصلاحيات والتعارض والأرشفة والاستعادة. يُراجع ترتيب التركيز واتجاه النص في المتصفح، بصورة مستقلة.
5. تفصل خطة التشغيل بين تهيئة البيانات وتشغيل API، وتطلب اختبار الجاهزية وتجربة الرجوع قبل التفكير في أي نشر حقيقي.

## Recorded evidence / التحقق المنفّذ

| Check | Result |
| --- | --- |
| Angular build with lockfile | Passed on Angular 20.3.35 and Node 24 |
| Angular browser check with simulated API | Passed in Chromium 138: RTL/LTR, searchable category picker, search and empty state, conflict feedback, archive and restore |
| .NET API build and boundary smoke | Passed on SDK 10.0.100 with SqlClient 6.1.8 (zero build warnings/errors); live HTTP verified missing/invalid credentials, denied reader writes, and invalid item/version/cursor |
| SQL-backed HTTP test | Provided in [tests/smoke.mjs](tests/smoke.mjs); SQL Server was unavailable in the authoring environment, so end-to-end database behavior remains to be verified locally |

نجح بناء Angular و.NET 10، واختبار حدود API الفعلي للصلاحيات والمدخلات، واختبار الواجهة في Chromium باستجابات API محاكية. لم يتوفر محرك SQL Server في بيئة إعداد المثال؛ شغّل اختبار التكامل محلياً للتحقق من قاعدة البيانات والأرشفة والاستعادة عبر الخادم الحقيقي.
