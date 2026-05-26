---
name: shopify-seo-csv-optimizer
description: Safely audit, improve, and validate Shopify product CSV exports for SEO content. Use when Codex needs to work on Shopify product CSV files for FamilySurprise or similar shops, especially to generate or improve SEO Title, SEO Description, and Image Alt Text while preserving all operational, variant, pricing, inventory, metafield, and Shopify structure fields. Also use when checking empty product descriptions in Body (HTML), deciding whether to inspect product image URLs for precise alt text, or creating an upload-ready duplicate CSV with a change report.
---

# Shopify SEO CSV Optimizer

## Workflow

1. Audit the source CSV before editing.
   - Run `scripts/shopify_csv_guard.py audit <csv> --output <report.md>`.
   - Report product count, row count, missing SEO fields, missing/duplicated alt text, empty `Body (HTML)`, drafts, B2B products, and excluded-search tags.
   - Explain that Shopify product exports can have multiple rows per product because variants/images share a `Handle`.

2. Ask before changing anything outside the default editable fields.
   - Ask all required workflow questions together immediately after the audit, so the user can answer once and the optimization can then run uninterrupted.
   - Default editable fields: `SEO Title`, `SEO Description`, `Image Alt Text`.
   - Ask before filling empty `Body (HTML)`. Never overwrite existing body copy unless the user explicitly asks.
   - Ask before optimizing draft products, B2B/shop-in-shop products, tags, product categories, or Google Shopping categories.
   - Ask whether to use image inspection for alt text:
     - Table-only mode is faster and cheaper but must be more generic.
     - Image-inspection mode uses the `Image Src` links, needs more time/tokens, and can create more visually precise alt text.
   - After the user answers the upfront questions, continue through generation, duplicate CSV creation, and validation without asking again unless validation fails or an unanticipated risk appears.

3. Generate improved content conservatively.
   - Use `Title`, `Handle`, `Body (HTML)`, `Tags`, product/variant options, `Image Src`, `Image Position`, existing `Image Alt Text`, B2B marker, `Status`, and `Published` as context.
   - Do not invent visual facts, materials, shipping claims, production claims, discounts, reviews, or origin claims.
   - Keep product identity intact; SEO titles should be close keyword variants, not unrelated rewrites.
   - When the user chooses "optimize all", overwrite weak existing alt text, including filename-like values such as `FamilySurprise-Hoodie-schwarz`, brand-prefix slugs, color-only product labels, and awkward captions.
   - If the user asks to skip drafts or another product group, preserve those rows exactly but explicitly mention that weak original SEO/alt text may remain in the skipped rows.

4. Save a duplicate CSV, not an overwrite.
   - Keep the original headers, row order, handle order, quoting-compatible CSV structure, and row count.
   - Use UTF-8 and normal CSV quoting.

5. Validate before delivery.
   - Run `scripts/shopify_csv_guard.py validate <original.csv> <updated.csv> --output <validation.md>`.
   - If empty body copy was explicitly allowed, add `--allow-empty-body-html`.
   - Treat any protected-field change as a blocker.
   - Read and summarize the validation report before handing off the CSV.

## Field Policy

Read `references/shopify-csv-field-policy.md` when classifying columns or deciding whether a field may be changed.

Use these defaults:

- Change by default: `SEO Title`, `SEO Description`, `Image Alt Text`.
- Ask first: `Body (HTML)`, `Tags`, `Product Category`, `Google Shopping / Google Product Category`.
- Preserve by default: every other column, including unknown columns.

## SEO Rules

Read `references/familysurprise-seo-guidelines.md` before generating titles, descriptions, or alt text.

Key rules:

- End every non-empty `SEO Title` with ` | FamilySurprise`.
- Do not set `SEO Title` equal to `Title`; make a small search-intent variant.
- Write German SEO copy unless the user asks otherwise.
- Use factual search intent: product type, recipient, occasion, personalization, motif, or use case.
- Keep claims grounded in the CSV context or inspected image.

## Image Alt Text Modes

Always ask which mode to use before large batches:

```text
I can create image alt texts in two modes:
1. Table-only: faster and cheaper, but more generic because I will not verify each image visually.
2. Image inspection: slower and more token-intensive, but more precise because I inspect the actual image URLs before describing visible attributes.
Which mode should I use?
```

In table-only mode:

- Do not say `blue shirt`, `black hoodie`, `gold lettering`, `woman wearing`, or similar unless the value is explicit in the row, options, existing alt text, title, tags, or body.
- Prefer safe wording such as `Personalisierter Mama Hoodie von FamilySurprise` or `Bierkrug mit Papa-Motiv und Fotoupload`.

In image-inspection mode:

- Inspect the actual image when a visual attribute would improve the alt text.
- Still avoid over-specific claims that are not clearly visible.
- Keep the alt text product-focused, not a long photo caption.

## Empty Body HTML

Read `references/body-html-defaults.md` when products have empty `Body (HTML)`.

Required behavior:

- First report how many products have empty visible description copy.
- Ask whether to list them only or fill empty descriptions.
- If filling is approved, fill only empty `Body (HTML)` cells on product rows.
- Existing `Body (HTML)` must remain unchanged unless explicitly requested.

## Scripts

Use `scripts/shopify_csv_guard.py` for deterministic guardrails:

```bash
python3 scripts/shopify_csv_guard.py audit products_export.csv --output audit.md
python3 scripts/shopify_csv_guard.py validate products_export.csv products_export_seo.csv --output validation.md
python3 scripts/shopify_csv_guard.py validate products_export.csv products_export_seo.csv --allow-empty-body-html --output validation.md
```

The validation command exits non-zero when headers, row count, row order, protected fields, or unauthorized columns changed.

## Completion Checklist

Before finalizing a CSV optimization task:

- Source CSV was audited.
- All required user decisions were asked upfront in one checkpoint.
- User chose table-only or image-inspection mode for alt text.
- User chose whether empty `Body (HTML)` should be listed or filled.
- Updated CSV is a duplicate file.
- Validation passed with no protected-field changes.
- A concise change summary and validation report path are provided.
