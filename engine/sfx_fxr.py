"""8-bit game SFX for Buck via pyfxr (BSD-3-Clause; skill notes: docs/skills/notes/2026-11-21_pyfxr-sfx.md).
Only single short effects - pluck/chord/tone melodies are NEVER used (no-music rule).
Presets are frozen by seed so every render sounds the same. Softened (lowpass + short tail) so 8-bit does not sound cheap.
  pip install --break-system-packages pyfxr==0.3.0
Spec: "sfx": ["fxr_pickup", ...]  (fxr_pickup = coin grab, fxr_powerup = win/saving, fxr_hurt = money lost,
fxr_select = list item / count beat, fxr_jump = Buck hop). Missing pyfxr -> the engine silently skips these names.
"""
import random
import numpy as np

# name -> (pyfxr generator, seed, max seconds); seeds picked from 8 candidates by length/peak (see growth_log 2026-11-21)
PRESETS = {"fxr_pickup": ("pickup", 5, 0.6), "fxr_powerup": ("powerup", 1, 0.6), "fxr_hurt": ("hurt", 2, 0.4),
           "fxr_select": ("select", 5, 0.3), "fxr_jump": ("jump", 2, 0.4)}
_CACHE = {}


def render(name, sr):
    key = (name, sr)
    if key in _CACHE: return _CACHE[key].copy()
    import pyfxr
    gen, seed, mx = PRESETS[name]
    st = random.getstate(); random.seed(seed)
    try: buf = getattr(pyfxr, gen)().build()
    finally: random.setstate(st)
    x = np.frombuffer(memoryview(buf), dtype=np.int16).astype(np.float32) / 32768.0
    if sr != pyfxr.SAMPLE_RATE:  # linear resample is fine for sub-second 8-bit tones
        n = int(len(x) * sr / pyfxr.SAMPLE_RATE)
        x = np.interp(np.arange(n) * pyfxr.SAMPLE_RATE / sr, np.arange(len(x)), x).astype(np.float32)
    x = x[: int(mx * sr)]
    a = float(np.exp(-2 * np.pi * 6500 / sr)); y = np.empty_like(x); acc = 0.0  # one-pole lowpass ~6.5 kHz (softer)
    for i, v in enumerate(x): acc = (1 - a) * v + a * acc; y[i] = acc
    x = y
    f = min(len(x), int(0.04 * sr)); x[-f:] *= np.linspace(1, 0, f, dtype=np.float32)
    x /= (np.abs(x).max() + 1e-9)
    _CACHE[key] = x
    return x.copy()


def available():
    try:
        import pyfxr  # noqa
        return True
    except Exception:
        return False


if __name__ == "__main__":  # audition: writes one wav per preset + candidate stats
    import sys, wave, os
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/fxr"; os.makedirs(out, exist_ok=True)
    for n in PRESETS:
        y = render(n, 48000)
        with wave.open(f"{out}/{n}.wav", "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000); w.writeframes((y * 32000).astype(np.int16).tobytes())
        print(n, round(len(y) / 48000, 2), "s")
