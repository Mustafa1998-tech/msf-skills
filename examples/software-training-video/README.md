# Software training video / فيديو تدريبي للبرامج

[العربية](README.ar.md)

This offline example teaches a single task in a fictional workbench: update a practice task to **Ready for review** and confirm the change saved. The English cut uses generic local synthetic narration and a generated tone. The Arabic cut uses localized screens, shaped Arabic captions, and the same quiet tone. Add an approved Arabic narration track to practice bilingual voice delivery. No account, production records, stock footage, or real person’s voice is used.

From the repository root:

```bash
python3 skills/msf-video-studio/scripts/render.py examples/software-training-video/storyboard.en.json output/training.en.mp4 --resolution 1080p
python3 skills/msf-video-studio-ar/scripts/render.py examples/software-training-video/storyboard.ar.json output/training.ar.mp4 --resolution 4k
python3 examples/software-training-video/smoke.py
# Add --4k to the smoke command to run both locales at 3840 × 2160.
```

Each render writes an MP4, SRT and QA JSON. The smoke test copies each skill folder to a temporary directory before rendering and decodes the result. The sample stills are 1080p, so 4K export upscales them. If you change the example, update the overlay positions and review both cuts at normal speed. The generated inputs are already included; `prepare_assets.py` is optional and uses Pillow with libraqm, DejaVu Sans, and FFmpeg with its Flite filter.

### Optional recording of the fixture

Install Playwright and its Chromium build in an environment available to Node. For an already approved compatible Chromium build, set `MSF_CHROMIUM_PATH` to its executable. Browser WebM recording still requires Playwright’s FFmpeg helper. In one terminal, serve the example only on loopback:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory examples/software-training-video
```

In another terminal:

```bash
node skills/msf-video-studio/scripts/capture.cjs examples/software-training-video/capture.en.json examples/software-training-video/local-captures-en
node skills/msf-video-studio-ar/scripts/capture.cjs examples/software-training-video/capture.ar.json examples/software-training-video/local-captures-ar
```

The demo captures the initial screen, opens the status selector, selects **Ready for review**, then saves and captures the confirmation. Set `record_video` to `true` in a copy of the capture plan for a browser-only WebM. To render your capture, update the storyboard’s source paths, scene timings, and overlays for the captured screen. The renderer works with the bundled PNGs without Playwright.

### بالعربية

يدرّب المثال على تحديث مهمة وهمية إلى **جاهزة للمراجعة** ثم التحقّق من حفظ التغيير. يتضمن المخطط العربي صورًا ونصوصًا عربية مع نغمة خافتة، ويضيف المخطط الإنجليزي تعليقًا اصطناعيًا عامًا. استخدم أوامر الإخراج أعلاه لإنشاء فيديو MP4 وترجمة SRT وتقرير تحقق. لا يحتاج الإخراج إلى إنترنت أو Playwright. يمكنك إضافة تعليق عربي مُعتمد بتحديد `narration` في المشهد. يلتقط أمر Playwright الاختياري أربع حالات للواجهة المحلية عند تثبيته. راجع اتصال الحروف واتجاه النص ومواضع الإبراز قبل التسليم.
