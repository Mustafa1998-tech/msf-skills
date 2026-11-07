# فيديو تدريبي للبرامج

[English](README.md)

يدرّب المثال على تحديث حالة مهمة وهمية في منصة تجريبية إلى **جاهزة للمراجعة**، ثم التحقّق من حفظ التغيير. يستخدم الإصدار العربي لقطات ونصوصًا عربية ونغمة خافتة مولّدة محليًا. يضيف الإصدار الإنجليزي تعليقًا صوتيًا اصطناعيًا عامًا. لا يستخدم المثال حسابًا حقيقيًا أو سجلات إنتاج أو صوت شخص معروف.

شغّل من جذر المستودع:

```bash
python3 skills/msf-video-studio-ar/scripts/render.py examples/software-training-video/storyboard.ar.json output/training.ar.mp4 --resolution 1080p
python3 skills/msf-video-studio/scripts/render.py examples/software-training-video/storyboard.en.json output/training.en.mp4 --resolution 4k
python3 examples/software-training-video/smoke.py
```

ينتج كل أمر إخراج ملف MP4 وترجمة SRT وتقرير تحقق بصيغة JSON. ينسخ اختبار الإخراج كل مهارة إلى مجلد مؤقت، ثم يصيّر الفيديو ويفك ترميزه. أضف `--4k` إلى الاختبار للتحقق من الإصدارين بدقة 3840 × 2160. دقة الصور التجريبية الأصلية 1080p، لذا تُكبَّر في إخراج 4K. لإضافة تعليق عربي مُعتمد، حدّد `narration` في المشهد. عند تعديل اللقطات راجع مواضع الإبراز واتصال الحروف واتجاه النص وتزامنه.

### التقاط واجهة المتصفح اختياريًا

ثبّت Playwright ومتصفح Chromium الخاص به بحيث يصل Node.js إليهما. إذا توفّر إصدار Chromium متوافق ومعتمد، اضبط `MSF_CHROMIUM_PATH` على مسار ملفه التنفيذي. يحتاج تسجيل WebM إلى مساعد FFmpeg الخاص بـPlaywright. شغّل البيئة التجريبية في نافذة أوامر على عنوان محلي:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory examples/software-training-video
```

شغّل الالتقاط في نافذة أخرى:

```bash
node skills/msf-video-studio-ar/scripts/capture.cjs examples/software-training-video/capture.ar.json examples/software-training-video/local-captures-ar
```

يحفظ السكربت أربع حالات: فتح الشاشة، وعرض قائمة الحالة، واختيار **جاهزة للمراجعة**، ثم ظهور نتيجة الحفظ. ضع `record_video` بقيمة `true` في نسخة من خطة الالتقاط لحفظ ملف WebM للمتصفح. لاستخدام اللقطات الجديدة، عدّل مساراتها وتوقيتها وإحداثيات الإبراز في المخطط. لا يتطلب إخراج الصور المرفقة وجود Playwright أو الاتصال بالإنترنت.
