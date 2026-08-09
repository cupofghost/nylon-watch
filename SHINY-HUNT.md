# SHINY HUNT — everything the repo knows about what the owner likes

Compiled 2026-08-09 from every piece of stated feedback, tuning note and live data in
this repo (`taxonomy.json`, `shops.json`, `poller.py`, `gloss.py`, `index.html`,
`README.md`, `state.json` @ 2026-08-08T23:56Z). Purpose: brief a future hunt for shiny
clothes without re-reading the codebase.

Note on sourcing: git history here is shallow — all 50 commits are automated
`state update` commits from `nylon-watch-bot`. **Every piece of owner feedback that
exists lives in the config/comments below**, not in commit messages.

---

## 1. The taste, in one page

### Wanted
- **Shiny surfaces, judged as a surface — not a fiber.** The owner's own word list, quoted
  in `taxonomy.json:80`: *nylon taffeta, gloss / glossy / high gloss, shine / high shine,
  iridescent, translucent, PVC, coated nylon, satin, sheen*. Everything else in the
  allowlist was extrapolated from those.
- **Real clothes, boxy/baggy cuts.** Verbatim from `taxonomy.json:90`: *"the aesthetic
  wants boxy/baggy real-clothes cuts (button-ups, tees, track jackets, trousers, shorts)"*.
- **Non-sexual.** `README.md:120` — *"your stated aesthetic is non-sexual"*. This is why
  the two latex/PVC shops ship disabled and why the silhouette veto list exists at all.

### Tone priority order (the ranking the owner asked for)
From `taxonomy.json:16` and `poller.py:391-413`. Each kept item gets a tone and a
`desire = gloss + bonus`:

| Rank | Tone | Bonus | Note |
|---|---|---|---|
| 1 | **colored** (jewel-tone gloss) | **+30** | lit-band saturation ≥ 0.28 |
| 2 | **metallic / silver** | **+18** | bright subject (≥0.55) + colorless |
| 3 | **wetlook_black** (true wet-look) | 0 | dark + *sharp* highlights (specden ≥ 0.02) |
| — | neutral / unscorable | 0 | |
| ✗ | **black_satin** | **−25** | dark + colorless + *soft* sheen — *"reads flat/cheap"* |

Owner's picks override all of it: an item rated shiny gets `+1000` and pins to the top
(`poller.py:502`, `index.html:452`) — *"your judgment outranks the score."*

### Not wanted
- **Matte fibers, named by the owner** (`taxonomy.json:85` — *"You named cotton/linen/wool"*):
  cotton, linen, wool + merino, cashmere, mohair, alpaca, canvas, denim, corduroy, fleece,
  flannel, tweed, hemp, jersey, terry, bouclé, suede, chino, khaki, jute, muslin.
  Hard veto on the garment's **identity** (title/type/tags), so a "cotton lining" note in
  the body copy won't kill a shiny shell.
- **Matte technical nylon.** `taxonomy.json:30`: *"'nylon' and technical/brand labels are
  NOT a reliable shine signal (most technical nylon is matte)"* — this was called *"the
  matte-nylon flood"* and is the single biggest historical false-positive source. Brand
  names (And Wander, Goldwin, Satisfy, Arc'teryx…) only **tag** an item; they never keep it.
- **Fetish silhouettes and hardware** (`taxonomy.json:91`, dropped before anything else):
  locking/posture collar, harness, corset, bondage, BDSM, gimp, hobble, crotchless,
  crotch zip, lace-up, cutout, open back / backless / sideless, underboob, underbust,
  nipple, garter, waist cincher, waspie, bodycon, strappy.
  Deliberate omissions, so as not to cut real clothes: *"cage"* (inside "cagoule"), bare
  *"crotch"* (technical trousers list a gusseted crotch), *"chest zip"* (running shops use
  chest-zip pockets).
- **Plain rainwear labels.** `taxonomy.json:68` — rain/waterproof words often mean matte,
  so they tag only. High-gloss PU (Rains) still gets through on genuine shine words.

### Working style (from `AGENTS.md`)
Owner is **not a coder** (`AGENTS.md:4`). Be brief, no essays, don't re-verify other
agents' signed work, sign every commit and `STATUS.md` entry.

---

## 2. Sources

Live status from the 2026-08-08T23:56Z run — **all 7 enabled shops reachable**.
"Raw → kept" is catalog size vs. items that survived the shine gate.

| Shop | On? | Raw → kept | What it's for |
|---|---|---|---|
| **Yards Store** `yardsstore.com` | ✔ | 2000 → **334** | Biggest yield. And Wander, Goldwin, Snow Peak, Gramicci. Ships intl. |
| **Satisfy** `satisfyrunning.com` | ✔ | 660 → **121** | Brand direct. Technical running nylon, shells. |
| **Distance** `distance-store.com` | ✔ | 2000 → **109** | Satisfy, District Vision, technical shells. EU sizing. |
| **Rains** `us.rains.com` | ✔ | 311 → **107** | *"Core rainwear source"* — high-gloss PU, shiny black/amber, String Overcoat. |
| **HAVN** `havnstore.com` | ✔ | 499 → **52** | Goldwin / Goldwin 0, And Wander, Snow Peak, ROA, Satisfy. |
| **Up There** `uptherestore.com` | ✔ | 248 → **47** | And Wander, Goldwin, Snow Peak, Gramicci, Satisfy. |
| **Gramicci** `gramicci.com` | ✔ | 190 → **4** | Brand direct. Nylon flares, shells, and wander collabs. Weakest yield — mostly matte. |
| **Honour Clothing** `honourclothing.com` | ✘ | — | Latex/rubber, PVC, wetlook. *"Adjacent to fetish retail — disabled by default; turn on deliberately."* |
| **MinimalLatex** `minimallatex.com` | ✘ | — | *"Minimal/tailored latex, clean silhouettes."* Closest match to the aesthetic at the high-shine end. |

**Brands that actually surface** (current 774-item feed): SATISFY 141, Rains 107,
Patagonia 77, Fjällräven 53, Snow Peak 15, plus long tails of Karhu, Hoka, Wild Things,
Carhartt WIP, Elliker, Filson, Barbour.

**Adding a source:** any Shopify store — `products_url` = `https://site/products.json`, or
scope to one brand with `/collections/<handle>/products.json`. Set `"enabled": false` to
mute without deleting. Some larger stores block raw `products.json` from GitHub's
datacenter IPs (HTTP 430/403) — point at a collection URL or use a peer boutique carrying
the same brands (`README.md:137-143`).

---

## 3. The hunt vocabulary

**Search these words** (the allowlist — the *only* way into the feed, `taxonomy.json:81`):

> nylon taffeta · taffeta · gloss · glossy · high gloss · gloss finish · shine · shiny ·
> high shine · sheen · iridescent · opalescent · pearlescent · holographic · translucent ·
> transparent · see-through · sheer · pvc · vinyl · tpu · coated nylon · coated · coating ·
> wax coated · waxed · glazed · lacquer · lacquered · enamel · satin · satiny · sateen ·
> charmeuse · duchesse · silk · silky · metallic · metalised · chrome · foil · liquid metal ·
> liquid · lamé · mirror · mirrored · reflective · polished · wet look · wetlook · oil slick ·
> slick · patent · patent leather · latex · rubberised · glanz · poly smooth · ultralight

Highest-frequency winners in the current feed: `tpu` (111), `silk` (98), `reflective` (75),
`coated` (65), `coating` (55), `polished` (36), `ultra-light` (34), `vinyl` (34), `waxed` (31),
`metallic` (25), `patent` (19), `rubberized` (17).

**Manual-hunt shortcuts**
- For **colored gloss** (top priority): Rains (amber/colorways), Satisfy, and Wander.
- For **metallic/silver**: Goldwin 0, Snow Peak, foil/lamé/chrome searches on Yards.
- For **true wet-look black**: Rains PU, coated/lacquer searches — avoid soft-sheen black
  satin, which the owner rates worst of all.
- For the **high-shine end**: flip `honour` / `minimallatex` to `"enabled": true` in
  `shops.json` and the `latex` / `pvc_vinyl` materials to `true` in `taxonomy.json`. The
  disqualifier veto is what keeps those shops' fetish cuts out — leave it on.

---

## 4. How the machine currently decides (so you know what it missed)

Pipeline (`poller.py:416+`), in order:
1. Fetch each enabled shop's `products.json`.
2. Drop `excludes.json` matches (item / brand / title-keyword).
3. Drop anything rated **matte** in `ratings.json`.
4. **Hard veto**: silhouette disqualifiers, then matte fibers — unless rated shiny.
5. **The gate**: keep only items whose text hits a `shine_terms` word (or rated shiny).
6. Score images for ranking only, classify tone, compute `desire`, diff vs. previous
   state, push via ntfy, sort and write `state.json`.

`fit_score` (what it's made of) and `gloss_score` (how shiny it looks) are kept separate
end to end so that when one axis misfires the other still works.

Gloss scoring itself (`gloss.py`): specular-highlight density (0.50) + bright-to-dark
dynamic range (0.34) + lit-region saturation (0.16). Matte cotton ≈ 3, glossy nylon ≈ 75,
latex ≈ 96. Documented failure modes: a white matte item on a white seamless scores mid;
black latex in flat studio light scores low.

---

## 5. Known gaps — read before trusting the feed

1. **Visual gloss is OFF.** `taxonomy.json:7` sets `visual.enabled: false` — the feed is
   purely keyword-driven right now. Consequences: every one of the 774 items has
   `tone: "neutral"` and no `gloss_score`, so **the colored > metallic > black priority
   ranking is inert**, and the app hides the gloss slider, the "Shiniest" sort and the
   "★ Priority tone" filter (`index.html:523-528`). Flip it back to `true` to get the
   ranking the owner asked for.
2. **Keyword matching is bare substring, no word boundaries.** Real false positives in the
   current feed: `lame` matches "Classic **Flame** Orange"; `tpu` matches TPU-soled
   trainers and bag coatings; `silk` matches "Natural Mix **Silk** Slub" knitwear and
   "Sienna Brume Parfum".
3. **`global_avoid` no longer filters anything.** It only subtracts from `fit_score`
   (`poller.py:193-196`), and `fit_score` stopped being a gate when `shine_terms` became
   the gate. That's why sunglasses, drinkware, fragrance, caps and backpacks are in the
   feed despite being on the avoid list — roughly **336 of 774 current items are not
   garments** (57 ACCESSORIES, 41 trainers, 34 footwear, 23 backpacks, 21 sunglasses,
   19 drinkware…). Biggest single cleanup available.
4. **No personal verdicts recorded yet.** `ratings.json` is `{"shiny": [], "matte": []}`
   and `excludes.json` is empty. Rating items in the app and exporting those two files is
   the strongest available lever — a shiny rating pins an item and survives every veto; a
   matte rating hides it everywhere, on every device.
5. **Dead filter branch:** `index.html:443` filters on `keep_reason === "GLOSSY"`, but the
   poller only emits `SHINE` / `PICK` (`poller.py:498`). Harmless — the pill was removed
   from the toolbar — but the code path never matches.
6. Feed size for reference: 774 kept, 627 in stock, 0 excluded, 56 disqualified on
   silhouette, 658 vetoed for matte fibers this run.

---

## 6. Tuning levers (one line each)

| Want | Change |
|---|---|
| Surface more / fewer items | add / remove words in `taxonomy.json → shine_terms.terms` |
| Stop over-blocking | trim `taxonomy.json → matte_fibers.terms` |
| Real clothes getting cut | remove the offending term from `disqualifiers.terms` |
| Re-enable gloss meter + tone ranking | `visual.enabled: true` |
| Re-tune the tone order | `visual.tone_ranking.bonus` (colored 30 / metallic 18 / wetlook_black 0 / black_satin −25) |
| Looser unlabelled-shine catch | lower `visual.gloss_floor_for_unkeyworded` (default 62) |
| Fuller image coverage | raise `visual.max_images_per_run` (default 220; cache makes cost one-time per image) |
| Add/mute a shop | `shops.json` — new entry, or `"enabled": false` |
| Kill an item/brand/word forever | app ⊘ button → export `excludes.json` to repo root |

Cadence: GitHub Action every 30 min, installs pillow + numpy, commits `state.json` +
`imgcache.json`. Pushes go out via ntfy (`NTFY_TOPIC` secret) on NEW and RESTOCK.

Signed: Claude Code | Opus | high
