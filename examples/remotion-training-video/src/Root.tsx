import {Composition} from 'remotion';
import {TrainingVideo} from './TrainingVideo';

const common = {
  component: TrainingVideo,
  durationInFrames: 360,
  fps: 30,
  width: 1920,
  height: 1080,
} as const;

export const RemotionRoot = () => (
  <>
    <Composition id="MSFTrainingAR" {...common} defaultProps={{locale: 'ar'}} />
    <Composition id="MSFTrainingEN" {...common} defaultProps={{locale: 'en'}} />
  </>
);
