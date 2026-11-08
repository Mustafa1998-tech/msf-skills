# أرشيف المصادر الخارجية

[English](README.md) · [سجل المصادر الكامل](../GITHUB_SOURCES.ar.md)

تحفظ حزم ZIP ملفات المهارات والسكربتات والمراجع المختارة من المصدر عند مراجعات Git محددة. تحمل كل حزمة ترخيصها الأصلي والإشعارات ذات الصلة بالنطاق المُراجع. تظل تراخيص أصحابها سارية. تجد المراجعات الدقيقة وبصمات SHA-256 ونطاق كل حزمة في [الفهرس](index.json).

| الحزمة | الترخيص | المحتوى المحفوظ |
| --- | --- | --- |
| [Superpowers](archives/superpowers.zip) | MIT | مجلدات المهارات الـ15 مع سكربتاتها ومراجعها. إضافات المستودع وHooks والاختبارات خارج مجلد المهارات غير مشمولة. |
| [Impeccable](archives/impeccable.zip) | Apache-2.0 | مهارة Codex المبنية ومراجعها وسكربتاتها. استُبعد دليلان مشتقان للمنصات وحزمة المتصفح المبنية لحين مراجعة نسبها بصورة مستقلة. CLI متطلب منفصل. |
| [UI UX Pro Max](archives/ui-ux-pro-max.zip) | MIT | مجلد مهارة UI/UX Pro Max كاملًا، بما فيه البيانات وسجل مصادرها وسكربتات Python. |
| [Anthropic Skills (Frontend Design)](archives/anthropic-frontend-design.zip) | Apache-2.0 | مهارة Frontend Design كاملة مع ترخيصها الخاص. |
| [Vercel Web Interface Guidelines](archives/web-interface-guidelines.zip) | MIT | الإرشادات ومصدر الأمر. لم تُضمَّن أداة التثبيت الخارجية. |
| [Remotion Codex Plugin](archives/remotion-codex.zip) | MIT | تعليمات المهارات والمراجع والسكربتات من إضافة Codex بترخيص MIT. الشعارات والوسائط ومحرك Remotion ذي الترخيص المنفصل غير مشمولة. |
| [HyperFrames](archives/hyperframes.zip) | Apache-2.0 | كود ومراجع المهارات الأساسية وCLI والسجل وقوالب HTML/CSS. الخطوط والوسائط ومحرك CLI غير مشمولة. |
| [onetake-videogen](archives/onetake-videogen.zip) | MIT | المهارة وسكربتات خط الإنتاج ومصدر مشروع Remotion والإشعارات الأصلية. الوسائط والرقع وأداة التثبيت غير مشمولة. محركات التشغيل الخارجية منفصلة. |

## الاستعراض وفك الحزم دون اتصال

نفّذ من جذر المستودع باستخدام Python 3.11 أو أحدث:

```sh
python3 scripts/vendor-skills.py list
python3 scripts/vendor-skills.py verify
python3 scripts/vendor-skills.py extract superpowers ./superpowers-review
```

اختر مجلد إخراج جديدًا. يتحقق الأمر من الحزمة ويفك ملفاتها فقط. راجع التعليمات والسكربتات ومتطلبات التشغيل قبل استخدام المهارة المؤرشفة أو تفعيلها يدويًا، واحتفظ بملف الترخيص والإشعارات عند نسخ محتواها. يثبّت مساعد MSF مهارات MSF الأصلية فقط. تستبعد بعض الحزم أصولًا أو تتطلب محركات تشغيل أو مكتبات أو خدمات أو موارد شبكة منفصلة. يمكن فك الحزم محليًا، ويعتمد تشغيل كل مسار على متطلباته.

يبقى OneTake Motion في [سجل المصادر](../GITHUB_SOURCES.ar.md) بترخيصه غير التجاري. ويبقى مستودعا Remotion Skills وإضافة Remotion لـClaude مراجع لحين التحقق من تراخيصهما. حزمة Remotion المؤرشفة مصدرها إضافة Codex المرخّصة بـMIT وتشمل ملفات المهارات المختارة منها.
