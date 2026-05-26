# FamilySurprise SEO Guidelines

## Brand

- Use the brand spelling `FamilySurprise`.
- End every non-empty `SEO Title` with ` | FamilySurprise`.
- Write in German unless the user asks otherwise.
- Prefer clear gift/search wording over decorative copy.

## SEO Titles

Goal: a close keyword variant of the product title, not a duplicate.

Rules:

- Keep the main product type and personalization intent.
- Use search phrases such as `Personalisierter`, `mit Foto`, `mit Namen`, `für Mama`, `für Papa`, `Geschenk`, `Gravur`, or the occasion only when supported by the CSV context.
- Keep the title concise. Aim for 45-65 characters including ` | FamilySurprise`; avoid exceeding about 70.
- Do not invent materials, colors, delivery promises, discounts, handmade claims, or origin claims.

Examples:

- Product title `Hoodie personalisierbar - Mama Outline`: `Personalisierter Mama Hoodie | FamilySurprise`
- Product title `Bierkrug personalisierbar - Papa, Fotoupload`: `Personalisierter Bierkrug für Papa mit Foto | FamilySurprise`
- Product title `Zollstock personalisierbar - PAPA Fotoupload + Namen`: `Personalisierter Zollstock für Papa mit Foto | FamilySurprise`
- Product title `Schlüsselanhänger personalisierbar - Fotoupload + Wunschtext`: `Personalisierter Schlüsselanhänger mit Foto | FamilySurprise`

## SEO Descriptions

Goal: factual search snippet that helps the right customer understand the product.

Rules:

- Aim for 140-160 characters when possible.
- Mention product type, personalization, recipient, occasion, motif, or use case when known.
- Use product body facts if present.
- Keep a natural German sentence. Avoid keyword stuffing.
- Do not promise delivery speed, quality level, production method, sustainability, origin, reviews, or material unless stated in the CSV/body text.

Good pattern:

`Personalisiertes Geschenk für Papa: Bierkrug mit Foto und Wunschmotiv gestalten. Eine persönliche Idee zum Vatertag, Geburtstag oder einfach so.`

## Image Alt Text

Goal: concise, factual, product-focused alt text.

Rules:

- Do not start with `Bild von` or `Foto von`.
- Include product type and meaningful motif/personalization when known.
- Mention visual attributes only when known from row data or confirmed by image inspection.
- Keep it concise; usually 5-12 words is enough.
- Avoid repeating the exact same alt text for many images when different image positions or variants are known.
- In "optimize all" mode, replace weak existing alt text even when it is non-empty.
- Treat filename-like or brand-prefix values as weak, for example `FamilySurprise-Hoodie-schwarz`, `FamilySurprise-Hoodie-Sportsgrey`, and hyphenated slug fragments.
- Avoid awkward literal color adjectives such as `Rosafarbenes` when a simple color noun sounds more natural. Prefer `Rosa Cropped Shirt ...`, `Grünes Armband ...`, or `Schwarzer Hoodie ...`.
- Do not use `am Model` / `an weiblichem Model` as filler. Mention the model only when it meaningfully distinguishes the image; otherwise describe product, motif, personalization, and color.
- Prefer search-intent wording over pure visual captions: `Rosa Cropped Shirt mit Anfangen-Statement` is better than `Rosafarbenes Cropped Shirt Anfangen am Model`.
- Use `mit ...-Statement`, `mit ...-Motiv`, `mit Namen`, `mit Foto`, `mit Gravur`, or recipient wording when supported by the product context.
- Write natural German noun phrases, not literal image captions. Prefer `Rosa Cropped Shirt mit Anfangen-Statement`, `Schwarzer Hoodie mit Fußball-Dad-Motiv`, or `Whiskyglas mit Built-Not-Born-Gravur`.
- Avoid bare product-name fragments after the color. `Rosa Cropped Shirt Anfangen`, `Graues Hoodie Push Your Limits`, and `Schwarzes Shirt BE GREAT am Model` are not acceptable.

Safe table-only examples:

- `Personalisierter Mama Hoodie von FamilySurprise`
- `Bierkrug für Papa mit Fotoupload`
- `Personalisierter Schlüsselanhänger mit Wunschtext`
- `Zollstock mit Papa-Motiv und Foto`

Unsafe table-only examples unless verified:

- `Blauer Hoodie mit weißem Druck`
- `Schwarzes Shirt an weiblichem Model`
- `Goldene Gravur auf Glas`

Weak alt text to rewrite:

- Bad: `FamilySurprise-Hoodie-schwarz`
  Good: `Schwarzer Hoodie mit Push-Your-Limits-Print`
- Bad: `Rosafarbenes Cropped Shirt Anfangen am Model`
  Good: `Rosa Cropped Shirt mit Anfangen-Statement`
- Bad: `Dunkelgraues Stand Up Oversized Shirt am Model`
  Good: `Dunkelgraues Oversized Shirt mit Stand-Up-Statement`
- Bad: `FamilySurprise-Hoodie-Sportsgrey`
  Good: `Grauer Hoodie mit Fußball-Motiv und Namen`

## Image Inspection Decision

Before a large batch, ask the user to choose:

- Table-only mode: faster, cheaper, and safer, but slightly more generic.
- Image-inspection mode: slower and more token-intensive, but better for accurate colors, motifs, model/product framing, and image-specific alt text.

If using table-only mode, prefer accurate generic phrasing over visually specific guesses.

## B2B And Shop-In-Shop Products

If a product is marked B2B or tagged for exclusion from search, ask before optimizing it.

When optimizing B2B/shop-in-shop products, avoid changing the brand positioning unless the user gives client-specific wording. Keep copy factual and avoid implying it is a normal FamilySurprise consumer product when it belongs to a partner/shop-in-shop campaign.
