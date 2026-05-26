# Empty Body HTML Defaults

`Body (HTML)` is visible storefront copy. Do not change it silently.

## Required Prompt

When empty body copy is found, ask:

```text
I found X products with empty `Body (HTML)`, which likely means no visible product description appears on the product page. Should I only list these products, or fill empty descriptions with conservative default copy? Existing descriptions will not be overwritten.
```

## Fill Rules

Only fill `Body (HTML)` when the user explicitly approves.

- Fill only product rows where `Body (HTML)` is empty.
- Do not modify existing body copy.
- Use only facts from `Title`, `Handle`, `Tags`, options, and known product context.
- Keep HTML simple: `<p>`, `<strong>`, `<ul>`, `<li>`.
- Do not invent materials, dimensions, shipping, production method, origin, discounts, sustainability, reviews, or care instructions.
- Do not add long sales copy when the product facts are thin.

## Conservative Template

Use this structure when enough facts are known:

```html
<p><strong>{Product name}</strong></p>
<p>{One factual sentence about the product type, personalization, recipient, occasion, or use case.}</p>
<ul>
  <li><p>{Known personalization fact, if any}</p></li>
  <li><p>{Known recipient/occasion/motif fact, if any}</p></li>
  <li><p>{Known product type or accessory use, if any}</p></li>
</ul>
```

If there are fewer than two reliable facts, use a shorter version:

```html
<p><strong>{Product name}</strong></p>
<p>{Product name} von FamilySurprise als passende Ergänzung für personalisierte Geschenke.</p>
```

## Examples

These examples show the expected level of caution and structure. Do not reuse them 1:1 unless they fit the actual product; adapt or shorten the text based only on reliable product facts from the CSV/context.

For `LED Teelicht` with tag `zubehör`:

```html
<p><strong>LED Teelicht</strong></p>
<p>LED Teelicht von FamilySurprise als passendes Zubehör für dekorative und personalisierte Geschenkideen.</p>
```

For `Geschenkverpackung Weinglas`:

```html
<p><strong>Geschenkverpackung Weinglas</strong></p>
<p>Geschenkverpackung für ein Weinglas von FamilySurprise, passend als Ergänzung zu personalisierten Geschenkideen.</p>
```
