# Visual direction / التوجّه البصري

**Brief.** مِرْصاد / Mirsad is a synthetic dispatch desk for reviewing shipments. The first task is finding an exception and opening its details. The interface defaults to Arabic and can switch to English without losing search, sort or filter state.

**Reference lock.** The live reference service returned `NO_SUBSCRIPTION`; the build uses bundled craft references (Typography, Color, Craft Details and Anti-AI-Slop) and the brief as the source of truth. The dominant direction is a transport control ledger: clear ruled sections, one strong teal lane for active controls and chart data, and plain typography at operational density. The amber watch band borrows the attention logic of the Color reference without introducing a second brand accent. There are no external graphics or bitmap requirements; the line chart is rendered from the sample records and backed by the same values in a text summary.

| Decision | Evidence and implementation |
| --- | --- |
| Distinctive identity | Operational context → Mirsad masthead, track-like bar motif, and code tokens |
| Priority | Operational brief → KPI strip and exception banner before the shipment table |
| Type | Typography → system sans with Arabic fallbacks; isolated monospace shipment IDs |
| Color | Color → two neutral palettes with separate chart, focus, warning and success roles |
| Controls | Craft Details → native dialog, buttons, labels, explicit focus, reduced motion |
| Density | Anti-AI-Slop → one ruled ledger, minimal radius, no decorative cards or shadows |

**QA matrix.** At 1440 × 900 and 390 × 844, review Arabic light, Arabic dark, and English light. Check initial, searched, filtered, empty, detail and keyboard focus states. Confirm that only the table container can scroll horizontally, the status is announced, and Escape returns focus to the invoking button. The browser check is separate from the Node model tests; see the README for recorded evidence.

**العربية.** مرصاد لوحة تشغيل لمتابعة الشحنات الوهمية. التصميم مستوحى من سجلات التشغيل: فواصل واضحة، لون فيروزي للتركيز والإجراءات، وشريط كهرماني للتأخير. استُخدمت مراجع الخطوط والألوان وقابلية الاستخدام لأن خدمة المراجع الحية لم تكن متاحة. افحص العربية الفاتحة والداكنة والإنجليزية على الهاتف وسطح المكتب، مع البحث والتصفية وعدم وجود نتائج والتنقل بلوحة المفاتيح.

## Recorded verification / نتائج التحقق

The Node suite passed all three model checks. Chromium 138 at 1440 × 900 and 390 × 844 passed the browser test for direction, theme, focus, dialogs, filtering, empty state, sorting, pagination, and containment of horizontal overflow. The visual review led to explicit chart ticks, equal three-day buckets, stronger placeholder text, and a mobile table-scroll hint. The captures below are from the final run.

نجحت اختبارات البحث والتصفية والإجماليات الثلاثة، ونجح اختبار Chromium لاتجاه الصفحة والسمات والتركيز والتصفية والتنقل. يوضّح الجدول لقطات التحقق النهائية.

| Capture / اللقطة | State / الحالة |
| --- | --- |
| [Desktop, Arabic light](evidence/desktop-rtl-light.jpg) | Initial ledger / السجل الأولي |
| [Desktop, Arabic dark](evidence/desktop-rtl-dark.jpg) | Alternate theme / الوضع الداكن |
| [Desktop, English light](evidence/desktop-ltr-light.jpg) | Second page after sort / الصفحة الثانية بعد الفرز |
| [Mobile, Arabic light](evidence/mobile-rtl-light.jpg) | Narrow viewport / عرض الهاتف |
