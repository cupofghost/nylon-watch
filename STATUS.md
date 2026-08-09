# STATUS

Last consolidation: (never)

## Active work
| Date | Area / files | Task & state (≤3 lines) | Signature |
|------|--------------|-------------------------|-----------|
| 2026-08-09 | SHINY-HUNT.md (new) | Compiled all owner feedback/taste rules, sources and tuning levers into one hunt brief. Read-only survey — no behavior changed. Done. | Signed: Claude Code \| Opus \| high |

## Shared-file touches
(list file + what changed + signature)

## Known issues
- `global_avoid` no longer filters: it only lowers `fit_score` (poller.py:193-196), which stopped being a gate — ~336/774 feed items are non-garments (sunglasses/drinkware/footwear/bags). 2026-08-09. Signed: Claude Code | Opus | high
- Visual gloss off (taxonomy.json:7) so tone ranking is inert — all items `neutral`, no colored/metallic/black-satin ordering. 2026-08-09. Signed: Claude Code | Opus | high
- Substring keyword matching: "lame" hits "Flame", "tpu" hits trainer soles, "silk" hits silk-slub knitwear + parfum. 2026-08-09. Signed: Claude Code | Opus | high
- Dead branch: index.html:443 filters `keep_reason === "GLOSSY"`, poller only emits SHINE/PICK. 2026-08-09. Signed: Claude Code | Opus | high

## Archive
(completed entries moved here during consolidation — one line each)
