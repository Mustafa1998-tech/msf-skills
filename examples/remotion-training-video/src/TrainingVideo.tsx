import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

type Locale = 'ar' | 'en';
type Labels = {
  heading: string;
  intro: string;
  platform: string;
  section: string;
  asset: string;
  code: string;
  status: string;
  draft: string;
  saved: string;
  action: string;
  confirmation: string;
  footer: string;
};
const labels: Record<Locale, Labels> = {
  ar: {
    heading: 'تسجيل أصل تقني',
    intro: 'شرح تدريبي ببيانات تجريبية',
    platform: 'MSF · نموذج تدريبي',
    section: 'إدارة الأصول',
    asset: 'جهاز حاسب تجريبي',
    code: 'رمز الأصل: DEMO-001',
    status: 'الحالة',
    draft: 'مسودة',
    saved: 'محفوظ',
    action: 'حفظ الأصل',
    confirmation: 'تم حفظ الأصل بنجاح',
    footer: 'خطوة واحدة · نتيجة واضحة',
  },
  en: {
    heading: 'Register a technical asset',
    intro: 'A demo with fictional data',
    platform: 'MSF · Training fixture',
    section: 'Asset management',
    asset: 'Practice workstation',
    code: 'Asset code: DEMO-001',
    status: 'Status',
    draft: 'Draft',
    saved: 'Saved',
    action: 'Save asset',
    confirmation: 'Asset saved successfully',
    footer: 'One task · Visible confirmation',
  },
};
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const background: React.CSSProperties = {
  background: 'linear-gradient(140deg,#0a1427 0%,#112849 55%,#123e4e 100%)',
  color: '#eff8fb',
  fontFamily: 'Tahoma, Arial, sans-serif',
};
const fill: React.CSSProperties = {width: '100%', height: '100%'};

const Intro: React.FC<{copy: Labels; locale: Locale}> = ({copy, locale}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20, 62, 85], [0, 1, 1, 0], clamp);
  const position = interpolate(frame, [0, 32], [52, 0], clamp);
  return (
    <AbsoluteFill style={{...background, direction: locale === 'ar' ? 'rtl' : 'ltr', alignItems: 'center', justifyContent: 'center', opacity}}>
      <div style={{transform: 'translateY(' + position + 'px)', textAlign: 'center'}}>
        <div style={{fontSize: 28, letterSpacing: 2, color: '#66d9d2', marginBottom: 28}}>MSF VIDEO STUDIO</div>
        <div style={{fontSize: 84, fontWeight: 800, lineHeight: 1.4}}>{copy.heading}</div>
        <div style={{fontSize: 38, color: '#bfd5df', marginTop: 20}}>{copy.intro}</div>
      </div>
    </AbsoluteFill>
  );
};

const Walkthrough: React.FC<{copy: Labels; locale: Locale}> = ({copy, locale}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const visible = interpolate(frame, [0, 25], [0, 1], clamp);
  const done = frame >= 181;
  const toastOpacity = interpolate(frame, [178, 200, 265, 288], [0, 1, 1, 0], clamp);
  const cursorX = interpolate(frame, [40, 115, 165], [260, 255, 100], clamp);
  const cursorY = interpolate(frame, [40, 115, 165], [230, 200, 485], clamp);
  const focus = interpolate(frame, [110, 140, 180, 205], [0, 1, 1, 0], clamp);
  const direction = locale === 'ar' ? 'rtl' : 'ltr';
  return (
    <AbsoluteFill style={{...background, direction, opacity: visible, padding: 74, boxSizing: 'border-box'}}>
      <div style={{fontSize: 26, color: '#83deda', marginBottom: 38}}>{copy.platform}</div>
      <div style={{display: 'flex', gap: 44, ...fill, height: 780}}>
        <div style={{width: 300, border: '1px solid #2e5870', borderRadius: 28, padding: 32, background: '#112840'}}>
          <div style={{fontSize: 34, fontWeight: 700, marginBottom: 48}}>MSF</div>
          <div style={{background: '#184e61', borderRadius: 16, padding: 23, color: '#e8fcf9', fontSize: 27}}>{copy.section}</div>
        </div>
        <div style={{position: 'relative', flex: 1, background: '#f8fbff', color: '#1b3248', borderRadius: 28, padding: 62, overflow: 'hidden'}}>
          <div style={{fontSize: 51, fontWeight: 800, marginBottom: 60}}>{copy.heading}</div>
          <div style={{border: '2px solid #dce7ee', borderRadius: 24, padding: 36, background: 'white'}}>
            <div style={{fontSize: 35, fontWeight: 700}}>{copy.asset}</div>
            <div style={{fontSize: 26, color: '#688096', marginTop: 14}}>{copy.code}</div>
            <div style={{display: 'flex', alignItems: 'center', gap: 22, marginTop: 45}}>
              <span style={{fontSize: 27}}>{copy.status}</span>
              <span style={{padding: '11px 28px', fontSize: 24, borderRadius: 40, background: done ? '#dcf8ee' : '#fff3d7', color: done ? '#117d59' : '#926113'}}>{done ? copy.saved : copy.draft}</span>
            </div>
          </div>
          <div style={{position: 'absolute', bottom: 66, right: locale === 'ar' ? 60 : 'auto', left: locale === 'en' ? 60 : 'auto', background: done ? '#167f67' : '#126c8e', color: 'white', borderRadius: 17, padding: '23px 43px', fontSize: 30, fontWeight: 700, boxShadow: '0 10px 24px #0d406047'}}>
            {copy.action}
          </div>
          <div style={{position: 'absolute', bottom: 58, right: locale === 'ar' ? 51 : 'auto', left: locale === 'en' ? 51 : 'auto', width: 280, height: 92, border: '5px solid #40c9b8', borderRadius: 22, opacity: focus, boxSizing: 'border-box'}} />
          <div style={{position: 'absolute', right: locale === 'ar' ? cursorX : 'auto', left: locale === 'en' ? cursorX : 'auto', top: cursorY, color: '#10a3a0', fontSize: 80, textShadow: '2px 3px 3px #17465a', transform: 'rotate(-18deg)'}}>➤</div>
          <div style={{position: 'absolute', top: 34, right: 40, left: 40, opacity: toastOpacity, background: '#e4f8f0', color: '#137e55', textAlign: 'center', fontSize: 29, padding: 18, borderRadius: 15, boxShadow: '0 5px 18px #15544620'}}>{copy.confirmation}</div>
        </div>
      </div>
      <div style={{fontSize: 26, color: '#a9c5d2', marginTop: 23}}>{copy.footer} · {Math.round(360 / fps)}s</div>
    </AbsoluteFill>
  );
};

export const TrainingVideo: React.FC<{locale: Locale}> = ({locale}) => {
  const copy = labels[locale];
  return (
    <AbsoluteFill style={background}>
      <IntroSection copy={copy} locale={locale} />
      <WalkSection copy={copy} locale={locale} />
    </AbsoluteFill>
  );
};

import {Sequence} from 'remotion';

const IntroSection: React.FC<{copy: Labels; locale: Locale}> = (props) => (
  <Sequence from={0} durationInFrames={85}><Intro {...props} /></Sequence>
);
const WalkSection: React.FC<{copy: Labels; locale: Locale}> = (props) => (
  <Sequence from={65} durationInFrames={295}><Walkthrough {...props} /></Sequence>
);
