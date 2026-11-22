#!/bin/bash
# One-command render environment for a fresh cloud container (vazifa sessiyasi 2026-11-22).
# Usage: bash engine/setup_env.sh   -> then render with: --model /tmp/kokoro/kokoro-v1.0.int8.onnx --voices /tmp/kokoro/voices-v1.0.bin
set -e
PY=python3
$PY -m pip install --break-system-packages -q numpy soundfile kokoro-onnx 2>&1 | grep -v WARNING || true
# system PIL (dist-packages) can be broken ("cannot import _imaging") -> own copy
$PY -I -c "from PIL import Image, ImageFilter" 2>/dev/null || $PY -m pip install --break-system-packages -q --ignore-installed pillow 2>&1 | grep -v WARNING || true
$PY -m pip install --break-system-packages -q praat-parselmouth==0.4.7 2>&1 | grep -v WARNING || true   # prosody_check
fetch() { [ -s "$2" ] || { mkdir -p "$(dirname "$2")"; curl -sSfL -o "$2" "$1"; }; }
G=https://raw.githubusercontent.com/google/fonts/main/ofl
fetch $G/anton/Anton-Regular.ttf /usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf
fetch $G/comicrelief/ComicRelief-Bold.ttf /usr/share/fonts/truetype/google-fonts/ofl/comicrelief/ComicRelief-Bold.ttf
if [ ! -s /usr/share/fonts/opentype/inter/Inter-ExtraBold.otf ]; then
  curl -sSfL -o /tmp/inter.zip https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip
  $PY -c "import zipfile,os;z=zipfile.ZipFile('/tmp/inter.zip');os.makedirs('/usr/share/fonts/opentype/inter',exist_ok=True)
[open('/usr/share/fonts/opentype/inter/'+n.split('/')[-1],'wb').write(z.read(n)) for n in z.namelist() if 'extras/otf/' in n and n.endswith(('Inter-ExtraBold.otf','Inter-SemiBold.otf'))]"
fi
K=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
fetch $K/kokoro-v1.0.int8.onnx /tmp/kokoro/kokoro-v1.0.int8.onnx
fetch $K/voices-v1.0.bin /tmp/kokoro/voices-v1.0.bin
mkdir -p /tmp/fin/bg/bank /tmp/fin/tts
$PY -I -c "import numpy, PIL, soundfile, kokoro_onnx; from PIL import ImageFont; ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf', 20); print('setup_env: OK')"
