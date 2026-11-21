#!/usr/bin/env python3
"""buffer_post.py - schedule a YouTube Short on Red Flag Rocco through the Buffer GraphQL API (free plan).
Key: env BUFFER_API_KEY (never printed, never written to the repo). Host api.buffer.com must be allowed in the
environment's network settings (done 2026-11-21).

  python3 -I engine/buffer_post.py channels
  python3 -I engine/buffer_post.py schedule --video <public mp4 url> --title "..." --text desc.txt --at 2026-11-24T15:00:00Z
                                            [--channel <id>] [--privacy public] [--draft]
  python3 -I engine/buffer_post.py list            # scheduled posts of the organization
  python3 -I engine/buffer_post.py delete <postId>

Limits (Buffer free): 3 channels, 10 scheduled posts per channel at a time; the free plan appends #PoweredByBuffer
to the caption; no custom Shorts thumbnail. YouTube category 27 = Education. Rocco is an original cartoon -> not
"realistic altered content" -> isAiGenerated false.
"""
import json, os, subprocess, sys, argparse

API = "https://api.buffer.com"
ORG = "6b01941140458756ad9d2f17"          # "My organization"
ROCCO = "6b01953dece6dfde5f442367"        # YouTube: Red Flag Rocco


def gql(query, variables=None):
    key = os.environ.get("BUFFER_API_KEY") or sys.exit("BUFFER_API_KEY not set")
    body = json.dumps({"query": query, "variables": variables or {}})
    r = subprocess.run(["curl", "-sS", "--max-time", "60", API, "-H", "Content-Type: application/json",
                        "-H", "Authorization: Bearer " + key, "--data-binary", "@-"], input=body.encode(),
                       capture_output=True, check=True)
    d = json.loads(r.stdout)
    if d.get("errors"): sys.exit("buffer error: " + json.dumps(d["errors"])[:800])
    return d["data"]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("arg", nargs="?")
    ap.add_argument("--video"); ap.add_argument("--title"); ap.add_argument("--text"); ap.add_argument("--at")
    ap.add_argument("--channel", default=ROCCO); ap.add_argument("--privacy", default="public")
    ap.add_argument("--draft", action="store_true")
    a = ap.parse_args()
    if a.cmd == "channels":
        print(json.dumps(gql("query($o:OrganizationId!){channels(input:{organizationId:$o}){id name service}}", {"o": ORG}), indent=1))
    elif a.cmd == "list":
        print(json.dumps(gql("query($o:OrganizationId!){posts(first:50,input:{organizationId:$o}){edges{node{id status dueAt text channelId}}}}", {"o": ORG}), indent=1)[:6000])
    elif a.cmd == "delete":
        # 2026-11-21: back up the post before deleting (another session's fresh post was once deleted by mistake)
        posts = gql("query($o:OrganizationId!){posts(first:50,input:{organizationId:$o}){edges{node{id status dueAt text channelId}}}}", {"o": ORG})
        node = next((e["node"] for e in posts["posts"]["edges"] if e["node"]["id"] == a.arg), None)
        if node:
            os.makedirs("work/rocco/deleted_posts", exist_ok=True)
            json.dump(node, open("work/rocco/deleted_posts/%s.json" % a.arg, "w"), indent=1)
            print("backup: work/rocco/deleted_posts/%s.json | due %s | %s" % (a.arg, node["dueAt"], node["text"][:120].replace("\n", " ")))
        print(json.dumps(gql("mutation($i:DeletePostInput!){deletePost(input:$i){__typename}}", {"i": {"id": a.arg}})))
    elif a.cmd == "schedule":
        text = open(a.text).read().strip() if a.text and os.path.exists(a.text) else (a.text or "")
        if not (a.video and a.title and a.at): sys.exit("need --video --title --at")
        if len(a.title) > 100: sys.exit("title > 100 chars")
        inp = {"channelId": a.channel, "text": text, "schedulingType": "automatic", "mode": "customScheduled",
               "dueAt": a.at, "needsApproval": False, "saveToDraft": bool(a.draft),
               "assets": [{"video": {"url": a.video}}],
               "metadata": {"youtube": {"title": a.title, "privacy": a.privacy, "categoryId": "27",
                                        "madeForKids": False, "isAiGenerated": False, "notifySubscribers": True}}}
        q = ("mutation($i:CreatePostInput!){createPost(input:$i){__typename "
             "... on PostActionSuccess{post{id status dueAt}} ... on InvalidInputError{message} "
             "... on LimitReachedError{message} ... on UnexpectedError{message} ... on RestProxyError{message} "
             "... on UnauthorizedError{message} ... on NotFoundError{message}}}")
        res = gql(q, {"i": inp})["createPost"]
        print(json.dumps(res))
        return 0 if res.get("__typename") == "PostActionSuccess" else 1
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main())
