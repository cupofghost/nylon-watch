# NYLON WATCH — shiny-garment watcher

Finds shiny garments (gloss, satin, coated nylon, metallic, latex, PVC, patent,
wet-look, taffeta…) across curated Shopify shops and alerts you to new drops and
restocks even while the app is closed.

## How it works — a simple keyword engine

1. **Shine allowlist (`taxonomy.json → shine_terms`).** A product is kept **only**
   if its title/description contains a shine word (gloss, glossy, high shine, satin,
   sheen, coated nylon, nylon taffeta, iridescent, translucent, PVC, metallic,
   chrome, latex, patent, wet-look…). A plain fabric label like "nylon" is not
   enough — it must actually read as shiny. Edit the list to taste.

2. **Matte blocklist (`taxonomy.json → matte_fibers`).** Anything whose name says
   cotton, linen, wool (and other matte fabrics) is dropped even if it also says
   "satin". This is what keeps the feed to shiny fabric only.

3. **Silhouette veto (`taxonomy.json → disqualifiers`).** Fetish/hardware/expose-
   not-cover cuts (corset, harness, crotch-zip, lace-up…) are dropped regardless.

The feed is instant and deterministic — no image analysis in the keep decision.
(A classical-CV gloss scorer still ships in `gloss.py`; it's turned **off** by
default via `visual.enabled=false`. Flip it back on to rank by a 0-100 gloss meter.)

## Teaching it your taste (optional AI)

Tap **✓ / ✕** on any card to mark it shiny or not — ✓ pins it and always keeps it,
✕ hides it. Export **ratings.json** to your repo and the poller obeys those calls
on every device.

Go further in **≡ → Teach it what you like**: paste **links** or add **photos** of
shiny things you love, export **liked.json** to the repo, and — if you set an
`ANTHROPIC_API_KEY` repo secret — the poller shows each example to Claude, decides
what makes it shiny, and adds those fabric words to your allowlist automatically
(`learned.json`). Without the key, the feed just stays keyword-only (no AI, no cost).

## Parts
```
nylon-watch/
├─ poller.py          # engine: fetch -> keyword gate -> diff -> alert
├─ learn.py           # optional AI: liked.json -> shine keywords (needs ANTHROPIC_API_KEY)
├─ gloss.py           # classical-CV gloss scorer (Pillow+numpy) — off by default
├─ taxonomy.json      # shine_terms allowlist, matte_fibers blocklist, disqualifiers  (edit me)
├─ shops.json         # watch list  (edit me)
├─ excludes.json      # items/brands/keywords to hide + mute  (app-generated, or edit)
├─ ratings.json       # your ✓/✕ shiny verdicts  (app-generated)
├─ liked.json         # examples you like, for AI learning  (app-generated)
├─ learned.json       # generated: shine words the AI learned from your likes
├─ state.json         # generated: live inventory + persistent memory
├─ imgcache.json      # generated: per-image gloss cache (only used if gloss is on)
├─ index.html         # the home-screen app (feed + closet)
└─ .github/workflows/nylon-watch.yml   # 30-min cron, installs pillow/numpy, commits state
```

## Excluding shops and items

**Shops** — temporary: toggle any shop off in the ≡ sheet (local to your phone).
Permanent: set `"enabled": false` on a shop in `shops.json` (the poller skips it
entirely — no fetch, no alerts).

**Items, brands, and keywords** — tap the **⊘** button on any feed card. You get
three choices:
- *Hide just this item* — that one product disappears.
- *Mute this brand* — every product from that vendor disappears.
- *Mute a keyword* — anything with that word in its title disappears (e.g. "corset").

Hiding is instant and local (feed only). To also **stop a hidden item re-alerting
via push**, open ≡ → **Export excludes.json** and drop the file in your repo root.
The poller reads it and filters those items *before* diffing — so they never render
and never push, on every device. Excluded items also don't consume image-analysis
budget. Review or un-hide anything anytime in ≡ → **Excluded**.

The exclude-rule format (if you'd rather hand-edit `excludes.json`):
```json
{ "items": ["uptherestore|7421"], "brands": ["maison atelier"], "keywords": ["corset"] }
```

## Digital closet

Switch between **Feed** and **Closet** with the toggle under the search bar. The
closet has two piles:

- **♥ Want / saved** — tap the **♡** on any feed card to save it. Saved entries keep
  the product link and, because the poller already watches these shops, show a live
  badge here: **IN STOCK**, **RESTOCK**, or **SOLD OUT**, refreshed each time state
  updates. This is a wishlist wired into the watcher, not a static list.
- **Own** — what you have. **+ Add owned** records an item by name, brand, size,
  material, optional link, image URL, and notes. Manual, since owned things aren't
  necessarily in any tracked shop.

The closet lives in your browser's local storage on that device. Back it up or move
it with ≡ → **Export closet.json** / **Import closet.json**.

## Setup — discrete action items

### 1. Repo (5 min)
- [ ] New **public** GitHub repo, e.g. `nylon-watch`. Upload all files, keeping the
      `.github/workflows/` path.
- [ ] Future edits: upload from the **outputs folder**, not the original, so changes
      carry forward (same note as BRICK WATCH).

### 2. Push notifications (5 min)
- [ ] Install **ntfy** on iPhone (App Store, free, no account).
- [ ] Pick a non-guessable topic, e.g. `nylon-watch-7h3k9q`. Subscribe to it in the app.
- [ ] Repo **Settings → Secrets and variables → Actions → New repository secret**:
      `NTFY_TOPIC` = your topic. (`NTFY_BASE`, `NTFY_TOKEN` optional.)
- [ ] Put the topic name into `index.html` where it shows `nylon-watch-xxxx` (cosmetic).

### 3. Baseline run (2 min)
- [ ] **Actions** tab → run **nylon-watch** manually. First run stores a baseline and
      sends **no** alerts (proven by test). It also does the first image-gloss pass —
      this run is the slowest; later runs reuse the image cache and are fast.
- [ ] Confirm a `state.json` + `imgcache.json` commit from `nylon-watch-bot`.

### 4. Deploy the app (3 min)
- [ ] **Settings → Pages → Deploy from branch → main / root.**
- [ ] Open `https://<you>.github.io/nylon-watch/` on iPhone → Share → **Add to Home Screen.**

## Using it
- **Material chips** under the search bar: tap to show/hide each surface. Toggles are
  local to your phone.
- **Min gloss slider**: drag up to show only shiny items. At 0 it's off.
- **Shiniest** sort: rank purely by visual gloss, ignoring keywords — best for finding
  unlisted shine.
- **● Unlisted shine** filter: show only items kept by image alone (no material keyword).
- Each card shows a **gloss meter** (0-100), material tags, sizes (restocked sizes
  highlighted), price, and links straight to the product.

## Materials & shops shipped
Enabled by default: **nylon, satin, wetlook, patent, rainwear** materials; shops
Satisfy, Gramicci, **Rains**, Up There, Yards, HAVN, Distance.

Off by default (one toggle to enable): **latex** and **pvc/vinyl** materials; shops
**Honour Clothing** and **MinimalLatex**. These cover the high-shine latex/PVC end.
They're shipped off because that retail space sits adjacent to fetish and your stated
aesthetic is non-sexual — turn them on deliberately when you want them.

## Tuning (after a week of real data)
- **taxonomy.json → materials**: add a term to a material's `terms` to catch more,
  or to `avoid` to exclude. `weight` scales how strongly a material's matches count.
- **taxonomy.json → visual.gloss_floor_for_unkeyworded** (default 62): lower it to
  surface more unlabelled-shine candidates (more noise), raise it to be stricter.
- **taxonomy.json → visual.max_images_per_run** (default 220): the per-run image cap.
  Raise if shops are large and you want fuller coverage; the cache means cost is
  one-time per image regardless.
- **taxonomy.json → visual.enabled**: set `false` to disable visual scoring entirely
  (keyword-only, fastest). The app shows "visual off" when this is the case.
- **shops.json**: add any Shopify store (`products_url` = `https://site/products.json`,
  or scope to one brand with `/collections/<handle>/products.json`). `enabled:false`
  to mute without deleting.

## Troubleshooting
- **Shop "unreachable HTTP 430/403"**: some larger Shopify stores block raw
  `products.json` from datacenter IPs (GitHub's). Others still work; or point at a
  collection URL; or use a peer boutique carrying the same brands.
- **First run slow / times out**: it's imaging every candidate once. If a shop has
  thousands of products, the `max_images_per_run` cap protects the run — later runs
  fill in the rest from cache across subsequent crons.
- **No pushes**: check the secret is exactly `NTFY_TOPIC` and you're subscribed to the
  same topic. The Action log prints `PUSH …` when it fires.
- **A matte item shows as SHINE**: bright product photography can fool the scorer.
  Raise `gloss_floor_for_unkeyworded`, or just rely on material chips for that session.
  This is why gloss is never the only signal.

## How the gloss scorer works (one paragraph)
Glossy/wet/latex/PVC/patent surfaces reflect light specularly: small clusters of
near-white blown pixels, sitting next to rapid dark falloff, with colored versions
keeping saturation in the lit band. Matte fabrics diffuse light evenly — no hotspots,
low local contrast. `gloss.py` downscales the image, finds locally-peaked bright
pixels (specular density), measures the bright-to-dark spread (dynamic range), and
checks saturation of the lit region, then blends them 0.50/0.34/0.16 into a 0-100
score. No model, no network beyond fetching the image, runs in the free Action.
