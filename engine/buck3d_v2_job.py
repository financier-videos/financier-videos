#!/usr/bin/env python3
"""Resumable builder for the Buck 3D v2 (cinema) sprite library — safe to run from any fresh cloud session.

Run inside a clone of financier-videos (branch media):
    pip install --break-system-packages -q bpy==5.3.0 pillow
    python3 engine/buck3d_v2_job.py --repo . --max-poses 4

What it does:
  * Looks at assets/buck3d_v2_parts/<pose>.tar to see which poses are already finished.
  * Renders the next missing poses one at a time with engine/buck3d.py --cinema (1080 px, 64 samples, ~75 s/frame on 2 CPU cores).
  * Converts the frames to WebP (quality 92, alpha kept), packs each pose as assets/buck3d_v2_parts/<pose>.tar
    and commits + pushes AFTER EVERY POSE, so a session that stops early loses at most one pose.
  * When all 15 poses exist it assembles assets/buck3d_v2.tar (make_video.py auto-loads it; it only uses a COMPLETE
    library, otherwise it keeps v1) and deletes the parts.
Exit codes: 0 = progress made or already complete, 2 = render failed, 3 = push failed.
Prints one JSON line at the end: {"done": [...], "missing": [...], "complete": bool}.
"""
import argparse, json, os, shutil, subprocess, sys, tarfile, tempfile, time

FPS = 15
MOODS = ["happy", "shocked", "laugh", "smug", "confused", "sideeye", "sad", "angry", "point", "dizzy", "thumbsup", "proud"]
ACTS = {"flip_happy": 11, "bonk_dizzy": 23, "dodge_shocked": 12}
FRAMES = dict({m: FPS for m in MOODS}, **ACTS)
ORDER = ["shocked", "happy", "sideeye", "confused", "dizzy", "laugh", "thumbsup", "dodge_shocked", "bonk_dizzy",
         "flip_happy", "smug", "proud", "point", "sad", "angry"]
TRAILER = ("\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"
           "Claude-Session: https://claude.ai/code/session_01MWGZtabPhoeqLpiUntG9jE")


def git(repo, *args, check=True):
    return subprocess.run(["git", "-C", repo, "-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", *args],
                          check=check, capture_output=True, text=True)


def push(repo, msg):
    git(repo, "add", "-A", "assets")
    if not git(repo, "diff", "--cached", "--quiet", check=False).returncode:
        return True
    git(repo, "commit", "-q", "-m", msg + TRAILER)
    for attempt in range(4):
        r = git(repo, "-c", "push.negotiate=true", "push", "origin", "HEAD:media", check=False)
        if r.returncode == 0:
            return True
        time.sleep(5 * (attempt + 1))
        git(repo, "fetch", "-q", "--depth", "20", "origin", "+refs/heads/media:refs/remotes/origin/media", check=False)
        if git(repo, "rebase", "-q", "origin/media", check=False).returncode:
            # add/add conflict = another session already pushed the same pose: take the remote and move on
            git(repo, "rebase", "--abort", check=False)
            git(repo, "reset", "-q", "--hard", "origin/media", check=False)
            return True
    print(r.stderr[-800:], file=sys.stderr)
    return False


def sync(repo):
    """Fast-forward to the remote so poses finished by other sessions are not rendered twice."""
    git(repo, "fetch", "-q", "--depth", "20", "origin", "+refs/heads/media:refs/remotes/origin/media", check=False)
    git(repo, "merge", "-q", "--ff-only", "origin/media", check=False)


def pack_pose(src, pose, parts):
    from PIL import Image
    n = FRAMES[pose]
    tmp = tempfile.mkdtemp(prefix=f"b3_{pose}_")
    for i in range(n):
        p = os.path.join(src, f"{pose}_{i:02d}.png")
        im = Image.open(p).convert("RGBA")
        if im.getchannel("A").getbbox() is None:
            raise RuntimeError(f"empty frame {p}")
        im.save(os.path.join(tmp, f"{pose}_{i:02d}.webp"), "WEBP", quality=92, method=6)
    os.makedirs(parts, exist_ok=True)
    out = os.path.join(parts, f"{pose}.tar")
    with tarfile.open(out + ".part", "w") as t:
        for i in range(n):
            t.add(os.path.join(tmp, f"{pose}_{i:02d}.webp"), arcname=f"{pose}_{i:02d}.webp")
    os.replace(out + ".part", out)
    shutil.rmtree(tmp, ignore_errors=True)


def assemble(repo, parts):
    final = os.path.join(repo, "assets", "buck3d_v2.tar")
    with tarfile.open(final + ".part", "w") as out:
        for pose in ORDER:
            with tarfile.open(os.path.join(parts, f"{pose}.tar")) as t:
                for m in t.getmembers():
                    out.addfile(m, t.extractfile(m))
    os.replace(final + ".part", final)
    shutil.rmtree(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--max-poses", type=int, default=4)
    ap.add_argument("--work", default=os.path.join(tempfile.gettempdir(), "buck3d_v2_frames"))
    ap.add_argument("--frames-dir", default="", help="optional dir that already holds finished PNG frames")
    ap.add_argument("--no-render", action="store_true", help="only pack poses whose PNG frames are already complete")
    ap.add_argument("--ignore-hold", action="store_true", help="pack/push even while assets/BUCK3D_HOLD exists (chat-side render)")
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    parts = os.path.join(repo, "assets", "buck3d_v2_parts")
    final = os.path.join(repo, "assets", "buck3d_v2.tar")
    if os.path.exists(final):
        print(json.dumps({"done": ORDER, "missing": [], "complete": True})); return 0
    hold = os.path.join(repo, "assets", "BUCK3D_HOLD")
    if os.path.exists(hold) and not a.ignore_hold:  # model file is private: scheduled sessions render nothing
        print(json.dumps({"hold": True, "why": open(hold).read().strip()[:200], "complete": False})); return 0
    have = lambda p: os.path.exists(os.path.join(parts, f"{p}.tar"))
    src = a.frames_dir or a.work
    os.makedirs(src, exist_ok=True)
    rendered = 0
    for pose in ORDER:
        if have(pose):
            continue
        sync(repo)
        if have(pose) or os.path.exists(final):
            continue
        ready = all(os.path.exists(os.path.join(src, f"{pose}_{i:02d}.png")) for i in range(FRAMES[pose]))
        if not ready:
            if a.no_render or rendered >= a.max_poses:
                continue
            r = subprocess.run([sys.executable, os.path.join(repo, "engine", "buck3d.py"), "--cinema",
                                "--out", src, "--only", pose])
            rendered += 1
            ready = all(os.path.exists(os.path.join(src, f"{pose}_{i:02d}.png")) for i in range(FRAMES[pose]))
            if r.returncode or not ready:
                print(f"render failed: {pose}", file=sys.stderr); return 2
        pack_pose(src, pose, parts)
        if not push(repo, f"assets: Buck 3D v2 cinema pose {pose}"):
            return 3
        print(f"pushed {pose}", flush=True)
    sync(repo)
    if os.path.exists(final):
        print(json.dumps({"done": ORDER, "missing": [], "complete": True})); return 0
    missing = [p for p in ORDER if not have(p)]
    if not missing:
        assemble(repo, parts)
        if not push(repo, "assets: Buck 3D v2 cinema library complete (buck3d_v2.tar)"):
            return 3
    print(json.dumps({"done": [p for p in ORDER if have(p)] if missing else ORDER, "missing": missing,
                      "complete": not missing}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
