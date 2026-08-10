#!/usr/bin/env python3
"""
AI learning for NYLON WATCH.

Turns examples the user LIKES — product links or uploaded photos — into shine
keywords that widen the allowlist. So "send it stuff you like and it learns
what's good" becomes: Claude looks at each liked item, decides if it's genuinely
shiny, and extracts the fabric/finish words that describe why. Those words are
merged into the allowlist (learned.json), so the next run surfaces more like it.

Runs inside the poller ONLY when ANTHROPIC_API_KEY is set (a GitHub Actions
secret). With no key, this module is skipped entirely and the feed stays a plain
keyword filter — nothing breaks. The API key never touches the web app; the call
happens server-side in the Action.

Files:
  liked.json   (you export from the app, drop in the repo)  -> {links:[...], images:[{data,media_type}]}
  learned.json (generated)  -> {terms:[...], seen:[...hashes], log:[...]}
"""

import os
import re
import json
import hashlib
import urllib.request

MODEL = "claude-opus-4-8"
MAX_NEW_PER_RUN = 12          # cap AI calls per run (only ever on NEW likes)
_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
       "(KHTML, like Gecko) Version/17.0 Safari/605.1.15 NYLON-WATCH-LEARN/1.0")

SCHEMA = {
    "type": "object",
    "properties": {
        "shiny": {"type": "boolean"},
        "keywords": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["shiny", "keywords"],
    "additionalProperties": False,
}

PROMPT = (
    "You curate a feed of SHINY garments — gloss, glossy, high-shine, satin, sheen, "
    "coated nylon, nylon taffeta, metallic, chrome, iridescent, translucent, latex, "
    "PVC, patent, wet-look and similar high-sheen fabrics; matte fabrics like cotton, "
    "linen and wool are unwanted. The user LIKES the item shown. First decide if it is "
    "genuinely shiny / high-sheen (shiny:true) or matte (shiny:false). If shiny, return "
    "up to 6 lowercase one- or two-word FABRIC or FINISH keywords a shop listing would "
    "use to describe why it looks shiny (e.g. \"taffeta\", \"coated nylon\", \"satin\", "
    "\"iridescent\", \"metallic\", \"wet-look\"). Only fabric/finish words — never "
    "colours, brand names, or garment types. If matte, return an empty keyword list."
)


def _log(*a):
    print("[learn]", *a, flush=True)


def available():
    return bool(os.environ.get("ANTHROPIC_API_KEY", "").strip())


def _fetch_text(url, cap=3_000_000, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(cap).decode("utf-8", "replace")


def _meta(html, prop):
    """Pull an Open Graph / meta tag value (og:image, og:title, og:description)."""
    for pat in (
        rf'<meta[^>]+(?:property|name)=["\']{re.escape(prop)}["\'][^>]+content=["\']([^"\']+)',
        rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']{re.escape(prop)}["\']',
    ):
        m = re.search(pat, html, re.I)
        if m:
            return m.group(1)
    return ""


def _link_example(url):
    """A product link -> (image_url, listing_text) via Open Graph tags."""
    html = _fetch_text(url)
    img = _meta(html, "og:image")
    text = (_meta(html, "og:title") + " " + _meta(html, "og:description")).strip()
    return img, text


def _content_blocks(image_url=None, image_b64=None, media_type="image/jpeg", text=""):
    blocks = []
    if image_url:
        blocks.append({"type": "image", "source": {"type": "url", "url": image_url}})
    elif image_b64:
        blocks.append({"type": "image", "source": {
            "type": "base64", "media_type": media_type, "data": image_b64}})
    prompt = PROMPT + (f"\n\nListing text: {text}" if text else "")
    blocks.append({"type": "text", "text": prompt})
    return blocks


def _classify(client, **kw):
    """Ask Claude: shiny? which shine words? Returns (shiny_bool, [keywords])."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=300,
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": _content_blocks(**kw)}],
    )
    text = next((b.text for b in resp.content if b.type == "text"), "{}")
    data = json.loads(text)
    kws = [str(k).strip().lower() for k in data.get("keywords", []) if str(k).strip()]
    return bool(data.get("shiny")), kws


def run(here):
    """Process any NEW liked examples and return the merged learned-terms list.
    Best-effort: any failure returns whatever terms were already learned, and the
    caller falls back to the shipped allowlist. Never raises into the poller."""
    liked_path = os.path.join(here, "liked.json")
    learned_path = os.path.join(here, "learned.json")

    learned = {"terms": [], "seen": [], "log": []}
    if os.path.exists(learned_path):
        try:
            learned = {**learned, **json.load(open(learned_path, encoding="utf-8"))}
        except Exception as e:
            _log(f"WARN reading learned.json: {e}")

    if not available():
        _log("ANTHROPIC_API_KEY not set — AI learning off; using shipped keywords only.")
        return learned["terms"]
    if not os.path.exists(liked_path):
        return learned["terms"]

    try:
        liked = json.load(open(liked_path, encoding="utf-8"))
    except Exception as e:
        _log(f"WARN reading liked.json: {e}")
        return learned["terms"]

    try:
        import anthropic
        client = anthropic.Anthropic()
    except Exception as e:
        _log(f"anthropic SDK unavailable ({e}); skipping learning.")
        return learned["terms"]

    seen = set(learned["seen"])
    terms = list(dict.fromkeys(learned["terms"]))
    examples = []
    for url in liked.get("links", []):
        if isinstance(url, str) and url.strip():
            examples.append(("link", url.strip()))
    for img in liked.get("images", []):
        if isinstance(img, dict) and img.get("data"):
            examples.append(("image", img))

    analyzed = 0
    for kind, item in examples:
        key = hashlib.sha1((kind + json.dumps(item, sort_keys=True)).encode()).hexdigest()[:16]
        if key in seen:
            continue
        if analyzed >= MAX_NEW_PER_RUN:
            break
        try:
            if kind == "link":
                image_url, text = _link_example(item)
                if not image_url and not text:
                    _log(f"no OG data at {item[:60]} — skipping")
                    seen.add(key)
                    continue
                shiny, kws = _classify(client, image_url=image_url or None, text=text)
            else:
                shiny, kws = _classify(
                    client, image_b64=item["data"],
                    media_type=item.get("media_type", "image/jpeg"))
            seen.add(key)
            analyzed += 1
            if shiny:
                new = [k for k in kws if k and k not in terms]
                terms.extend(new)
                learned["log"] = (learned.get("log", []) + [{"k": key, "kws": kws}])[-200:]
                _log(f"learned from {kind}: +{new}" if new else f"{kind}: shiny, no new words")
            else:
                _log(f"{kind}: judged matte, ignored")
        except Exception as e:
            _log(f"WARN classifying {kind}: {str(e)[:120]}")
            seen.add(key)  # don't retry a broken example forever

    learned["terms"] = terms
    learned["seen"] = list(seen)[-2000:]
    if analyzed:
        try:
            tmp = learned_path + ".tmp"
            json.dump(learned, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
            os.replace(tmp, learned_path)
            _log(f"analyzed {analyzed} new likes; allowlist now +{len(terms)} learned words")
        except Exception as e:
            _log(f"WARN writing learned.json: {e}")
    return terms
