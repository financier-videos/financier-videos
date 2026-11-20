import {registerRoot, Composition, useCurrentFrame, interpolate, spring, useVideoConfig, AbsoluteFill} from 'remotion';
import React from 'react';
const Counter = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const v = Math.round(interpolate(f, [0, 45], [0, 1332], {extrapolateRight: 'clamp'}));
  const s = spring({frame: f - 45, fps, config: {damping: 9}});
  return <AbsoluteFill style={{background: '#0a0c12', justifyContent: 'center', alignItems: 'center', fontFamily: 'sans-serif'}}>
    <div style={{color: '#F5C542', fontSize: 220, fontWeight: 900, transform: `scale(${1 + 0.15 * s})`}}>${v.toLocaleString('en-US')}</div>
    <div style={{color: '#eee', fontSize: 64, opacity: s, marginTop: 40}}>A YEAR ON SUBSCRIPTIONS</div>
  </AbsoluteFill>;
};
const Root = () => <Composition id="Counter" component={Counter} durationInFrames={90} fps={30} width={1080} height={1920}/>;
registerRoot(Root);
