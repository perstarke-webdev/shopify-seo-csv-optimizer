# Shopify CSV Field Policy

## Default Editable Fields

Only these fields may be edited without additional permission:

| Field | Use |
|---|---|
| `SEO Title` | Search result title. Generate per product and always end with the FamilySurprise suffix. |
| `SEO Description` | Search result meta description. Generate per product from factual context. |
| `Image Alt Text` | Accessibility and image SEO. Generate per image row; do not invent visual details. |

Exact SEO title suffix: ` | FamilySurprise`.

## Ask Before Editing

These fields can affect the visible shop, collection behavior, feeds, or taxonomy. Ask first.

| Field | Rule |
|---|---|
| `Body (HTML)` | Fill only when empty and only after permission. Existing body copy must not be overwritten by default. |
| `Tags` | Use as context by default. Edit only when the user asks for tag cleanup/enrichment. |
| `Product Category` | Use as context by default. Edit only with a taxonomy plan. |
| `Google Shopping / Google Product Category` | Edit only with a validated category mapping. |

Also ask before optimizing:

- Draft products: `Status != active` or `Published != true`.
- B2B/shop-in-shop products: `B2B (product.metafields.custom.b2b) = TRUE`.
- Products tagged `exclude-search`, `exlude-search`, or similar.

## Context-Only Fields

Use these to understand the product, but do not change them in the default workflow:

`Handle`, `Title`, `Vendor`, `Type`, `Published`, `Status`, `Gift Card`, `Option1 Name`, `Option1 Value`, `Option2 Name`, `Option2 Value`, `Option3 Name`, `Option3 Value`, `Image Src`, `Image Position`, `Variant Image`, `B2B (product.metafields.custom.b2b)`, and existing Google Shopping audience/feed fields.

`Handle` is especially important context because it often contains normalized keywords, but changing it can change URLs. Preserve it.

## Protected Fields

Treat these as protected operational data. The validation report must fail if they change without explicit permission.

| Group | Fields |
|---|---|
| Variant identity | `Variant SKU`, `Variant Barcode`, variant options, `Variant Image` |
| Inventory and fulfillment | `Variant Inventory Tracker`, `Variant Inventory Policy`, `Variant Fulfillment Service` |
| Pricing and margin | `Variant Price`, `Variant Compare At Price`, `Cost per item`, market price fields |
| Shipping and tax | `Variant Grams`, `Variant Weight Unit`, `Variant Requires Shipping`, `Variant Taxable`, `Variant Tax Code`, unit price fields |
| Markets | `Included / Deutschland`, `Price / Deutschland`, `Compare At Price / Deutschland` |
| App/system fields | `Campaign version (product.metafields.teeinblue.campaign_version)`, option linked-to fields, unknown app metafields |
| Recommendations/search app fields | complementary products, related products, search boosts |

Unknown columns are protected by default.

## Structural Rules

- Preserve header names and order exactly.
- Preserve row count exactly.
- Preserve row order exactly.
- Preserve all `Handle` values exactly.
- Preserve all unapproved cells exactly.
- Produce a duplicate CSV; never overwrite the source file.
