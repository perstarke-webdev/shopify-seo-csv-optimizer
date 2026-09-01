#!/usr/bin/env python3
"""Audit and validate Shopify product CSV edits for SEO-safe workflows."""

from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import sys
from pathlib import Path


DEFAULT_EDITABLE = {"SEO Title", "SEO Description", "Image Alt Text"}
ASK_FIRST = {
    "Body (HTML)",
    "Tags",
    "Product Category",
    "Google Shopping / Google Product Category",
}
CONTEXT_ONLY = {
    "Handle",
    "Title",
    "Vendor",
    "Type",
    "Published",
    "Status",
    "Gift Card",
    "Option1 Name",
    "Option1 Value",
    "Option1 Linked To",
    "Option2 Name",
    "Option2 Value",
    "Option2 Linked To",
    "Option3 Name",
    "Option3 Value",
    "Option3 Linked To",
    "Image Src",
    "Image Position",
    "Variant Image",
    "B2B (product.metafields.custom.b2b)",
}
TITLE_SUFFIX = " | FamilySurprise"


def shopify_dialect() -> csv.Dialect:
    """Return Shopify's standard CSV dialect without heuristic sniffing.

    Shopify exports comma-separated CSV with doubled double quotes inside quoted
    fields. ``csv.Sniffer`` can incorrectly infer ``doublequote=False`` from
    quote-heavy product HTML, which makes valid rows appear structurally broken.
    """
    return csv.get_dialect("excel")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]], csv.Dialect]:
    dialect = shopify_dialect()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, dialect=dialect)
        headers = reader.fieldnames or []
        rows = []
        for row_number, row in enumerate(reader, start=2):
            if None in row:
                extras = row.pop(None)
                raise SystemExit(
                    f"{path}: row {row_number} has {len(extras)} extra value(s), "
                    "which indicates malformed CSV structure."
                )
            rows.append({key: (value if value is not None else "") for key, value in row.items()})
    if not headers:
        raise SystemExit(f"{path}: no CSV headers found")
    return headers, rows, dialect


def product_groups(rows: list[dict[str, str]]) -> collections.OrderedDict[str, list[tuple[int, dict[str, str]]]]:
    groups: collections.OrderedDict[str, list[tuple[int, dict[str, str]]]] = collections.OrderedDict()
    for offset, row in enumerate(rows, start=2):
        handle = row.get("Handle", "")
        groups.setdefault(handle, []).append((offset, row))
    return groups


def product_row(items: list[tuple[int, dict[str, str]]]) -> dict[str, str]:
    for _, row in items:
        if row.get("Title"):
            return row
    return items[0][1]


def classify_field(field: str) -> str:
    if field in DEFAULT_EDITABLE:
        return "editable_default"
    if field in ASK_FIRST:
        return "ask_first"
    if field in CONTEXT_ONLY:
        return "context_only"
    return "protected_by_default"


def nonempty(value: str | None) -> bool:
    return bool((value or "").strip())


def contains_exclude_search(tags: str) -> bool:
    normalized = tags.lower().replace("_", "-").replace(" ", "")
    return "exclude-search" in normalized or "exlude-search" in normalized


def field_stats(headers: list[str], rows: list[dict[str, str]]) -> list[dict[str, object]]:
    stats = []
    for field in headers:
        values = [row.get(field, "") for row in rows]
        stats.append(
            {
                "field": field,
                "classification": classify_field(field),
                "nonempty": sum(1 for value in values if nonempty(value)),
                "unique": len(set(values)),
            }
        )
    return stats


def duplicate_values(rows: list[dict[str, str]], field: str) -> list[dict[str, object]]:
    counts = collections.Counter(row.get(field, "") for row in rows if nonempty(row.get(field, "")))
    return [
        {"value": value, "count": count}
        for value, count in counts.most_common()
        if count > 1
    ]


def audit_data(path: Path) -> dict[str, object]:
    headers, rows, dialect = read_csv(path)
    groups = product_groups(rows)
    products = [product_row(items) for items in groups.values()]
    image_rows = [row for row in rows if nonempty(row.get("Image Src", ""))]
    empty_body = [row.get("Handle", "") for row in products if not nonempty(row.get("Body (HTML)", ""))]
    missing_seo_title = [row.get("Handle", "") for row in products if not nonempty(row.get("SEO Title", ""))]
    missing_seo_description = [
        row.get("Handle", "") for row in products if not nonempty(row.get("SEO Description", ""))
    ]
    missing_alt = [
        row.get("Handle", "")
        for row in image_rows
        if not nonempty(row.get("Image Alt Text", ""))
    ]
    status_counts = collections.Counter(row.get("Status", "") for row in products)
    published_counts = collections.Counter(row.get("Published", "") for row in products)
    vendor_counts = collections.Counter(row.get("Vendor", "") for row in products)
    b2b_handles = [
        row.get("Handle", "")
        for row in products
        if row.get("B2B (product.metafields.custom.b2b)", "").strip().upper() == "TRUE"
    ]
    excluded_handles = [
        row.get("Handle", "")
        for row in products
        if contains_exclude_search(row.get("Tags", ""))
    ]
    draft_handles = [
        row.get("Handle", "")
        for row in products
        if row.get("Status", "").lower() != "active" or row.get("Published", "").lower() != "true"
    ]

    return {
        "path": str(path),
        "dialect": {
            "delimiter": getattr(dialect, "delimiter", ","),
            "quotechar": getattr(dialect, "quotechar", '"'),
            "lineterminator": repr(getattr(dialect, "lineterminator", "\r\n")),
        },
        "headers_count": len(headers),
        "row_count": len(rows),
        "product_count": len(groups),
        "image_row_count": len(image_rows),
        "missing": {
            "seo_title_products": missing_seo_title,
            "seo_description_products": missing_seo_description,
            "body_html_products": empty_body,
            "image_alt_text_rows": len(missing_alt),
            "image_alt_text_handles": sorted(set(missing_alt)),
        },
        "counts": {
            "status": dict(status_counts),
            "published": dict(published_counts),
            "vendor": dict(vendor_counts),
            "b2b_products": len(b2b_handles),
            "draft_or_unpublished_products": len(draft_handles),
            "excluded_search_products": len(excluded_handles),
        },
        "handles": {
            "b2b": b2b_handles,
            "draft_or_unpublished": draft_handles,
            "excluded_search": excluded_handles,
        },
        "duplicates": {
            "seo_title": duplicate_values(products, "SEO Title"),
            "seo_description": duplicate_values(products, "SEO Description"),
            "image_alt_text": duplicate_values(image_rows, "Image Alt Text"),
        },
        "fields": field_stats(headers, rows),
    }


def md_escape(value: object) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def render_audit_markdown(data: dict[str, object]) -> str:
    missing = data["missing"]  # type: ignore[index]
    counts = data["counts"]  # type: ignore[index]
    handles = data["handles"]  # type: ignore[index]
    lines = [
        "# Shopify SEO CSV Audit",
        "",
        f"- Source: `{data['path']}`",
        f"- Rows: {data['row_count']}",
        f"- Products by `Handle`: {data['product_count']}",
        f"- Headers: {data['headers_count']}",
        f"- Image rows: {data['image_row_count']}",
        "",
        "## SEO Gaps",
        "",
        f"- Products missing `SEO Title`: {len(missing['seo_title_products'])}",
        f"- Products missing `SEO Description`: {len(missing['seo_description_products'])}",
        f"- Products with empty `Body (HTML)`: {len(missing['body_html_products'])}",
        f"- Image rows missing `Image Alt Text`: {missing['image_alt_text_rows']}",
        "",
        "## Product Groups Needing Decisions",
        "",
        f"- B2B products: {counts['b2b_products']}",
        f"- Draft/unpublished products: {counts['draft_or_unpublished_products']}",
        f"- Excluded-search tagged products: {counts['excluded_search_products']}",
        "",
    ]
    for label, key in [
        ("Empty Body (HTML)", "body_html_products"),
        ("B2B", "b2b"),
        ("Draft/Unpublished", "draft_or_unpublished"),
        ("Excluded Search", "excluded_search"),
    ]:
        source = missing if key.endswith("_products") else handles
        values = source.get(key, [])  # type: ignore[union-attr]
        if values:
            lines.extend([f"### {label}", ""])
            lines.extend(f"- `{value}`" for value in values)
            lines.append("")

    lines.extend(
        [
            "## Field Inventory",
            "",
            "| Field | Classification | Non-empty cells | Unique values |",
            "|---|---|---:|---:|",
        ]
    )
    for item in data["fields"]:  # type: ignore[index]
        lines.append(
            "| {field} | {classification} | {nonempty} | {unique} |".format(
                field=md_escape(item["field"]),
                classification=md_escape(item["classification"]),
                nonempty=item["nonempty"],
                unique=item["unique"],
            )
        )
    lines.append("")
    return "\n".join(lines)


def title_or_description_warnings(
    updated_rows: list[dict[str, str]],
    original_rows: list[dict[str, str]],
) -> list[str]:
    warnings: list[str] = []
    for row_number, (original, updated) in enumerate(zip(original_rows, updated_rows), start=2):
        title = updated.get("SEO Title", "")
        description = updated.get("SEO Description", "")
        alt = updated.get("Image Alt Text", "")
        if title and not title.endswith(TITLE_SUFFIX):
            warnings.append(f"Row {row_number}: SEO Title does not end with `{TITLE_SUFFIX}`.")
        if title and updated.get("Title") and title == updated.get("Title"):
            warnings.append(f"Row {row_number}: SEO Title is identical to product Title.")
        if title and len(title) > 70:
            warnings.append(f"Row {row_number}: SEO Title is longer than 70 characters.")
        if description and len(description) > 165:
            warnings.append(f"Row {row_number}: SEO Description is longer than 165 characters.")
        if description and len(description) < 80 and description != original.get("SEO Description", ""):
            warnings.append(f"Row {row_number}: new SEO Description is shorter than 80 characters.")
        if alt and len(alt) > 125:
            warnings.append(f"Row {row_number}: Image Alt Text is longer than 125 characters.")
        weak_reason = weak_alt_text_reason(alt)
        if weak_reason:
            state = "unchanged original" if alt == original.get("Image Alt Text", "") else "updated"
            warnings.append(f"Row {row_number}: {state} weak Image Alt Text ({weak_reason}): `{alt}`.")
    return warnings


def weak_alt_text_reason(alt: str) -> str:
    text = (alt or "").strip()
    if not text:
        return ""
    lowered = text.lower()
    words = re.findall(r"[A-Za-zÄÖÜäöüß0-9]+", text)
    if text.startswith("FamilySurprise-"):
        return "brand-prefix or filename-like value"
    if re.search(r"\b[a-z]+-[a-z0-9-]+\b", lowered) and " " not in text:
        return "hyphenated slug-like value"
    if len(words) <= 3 and any(term in lowered for term in ["hoodie", "shirt", "cap", "glas", "armband"]):
        return "too generic for an optimized product alt"
    if "rosafarbenes" in lowered:
        return "awkward color phrasing; prefer `Rosa ...`"
    if re.search(r"\b(am|an)\s+(weiblichen?\s+|männlichen?\s+)?model\b", lowered):
        if not any(term in lowered for term in ["statement", "motiv", "foto", "gravur", "namen", "name"]):
            return "`am/an Model` used as filler without product intent"
    if " anfangen am model" in lowered:
        return "awkward phrase; use `mit Anfangen-Statement`"
    return ""


def validate_data(
    original_path: Path,
    updated_path: Path,
    allowed_fields: set[str],
    allow_empty_body_html: bool,
) -> tuple[dict[str, object], int]:
    original_headers, original_rows, _ = read_csv(original_path)
    updated_headers, updated_rows, _ = read_csv(updated_path)
    errors: list[str] = []
    warnings: list[str] = []
    allowed_changes: list[dict[str, object]] = []
    protected_changes: list[dict[str, object]] = []

    if original_headers != updated_headers:
        errors.append("Header names/order changed.")
    if len(original_rows) != len(updated_rows):
        errors.append(f"Row count changed: {len(original_rows)} -> {len(updated_rows)}.")

    comparable_rows = min(len(original_rows), len(updated_rows))
    comparable_fields = original_headers if original_headers == updated_headers else [
        field for field in original_headers if field in updated_headers
    ]

    for index in range(comparable_rows):
        original = original_rows[index]
        updated = updated_rows[index]
        row_number = index + 2
        if original.get("Handle", "") != updated.get("Handle", ""):
            errors.append(
                f"Row {row_number}: Handle changed from `{original.get('Handle', '')}` "
                f"to `{updated.get('Handle', '')}`."
            )
        for field in comparable_fields:
            old_value = original.get(field, "")
            new_value = updated.get(field, "")
            if old_value == new_value:
                continue

            body_allowed = (
                allow_empty_body_html
                and field == "Body (HTML)"
                and not nonempty(old_value)
                and nonempty(new_value)
            )
            if field in allowed_fields or body_allowed:
                allowed_changes.append(
                    {
                        "row": row_number,
                        "handle": updated.get("Handle", ""),
                        "field": field,
                        "old": old_value,
                        "new": new_value,
                    }
                )
            else:
                protected_changes.append(
                    {
                        "row": row_number,
                        "handle": updated.get("Handle", ""),
                        "field": field,
                        "old": old_value,
                        "new": new_value,
                    }
                )

    if protected_changes:
        errors.append(f"Protected or unauthorized cells changed: {len(protected_changes)}.")

    warnings.extend(title_or_description_warnings(updated_rows[:comparable_rows], original_rows[:comparable_rows]))

    data = {
        "original": str(original_path),
        "updated": str(updated_path),
        "allowed_fields": sorted(allowed_fields),
        "allow_empty_body_html": allow_empty_body_html,
        "errors": errors,
        "warnings": warnings,
        "allowed_change_count": len(allowed_changes),
        "protected_change_count": len(protected_changes),
        "allowed_changes": allowed_changes,
        "protected_changes": protected_changes,
    }
    return data, 1 if errors else 0


def render_validation_markdown(data: dict[str, object]) -> str:
    lines = [
        "# Shopify SEO CSV Validation",
        "",
        f"- Original: `{data['original']}`",
        f"- Updated: `{data['updated']}`",
        f"- Allowed fields: {', '.join(data['allowed_fields'])}",  # type: ignore[arg-type]
        f"- Empty Body (HTML) additions allowed: {data['allow_empty_body_html']}",
        f"- Allowed changed cells: {data['allowed_change_count']}",
        f"- Protected changed cells: {data['protected_change_count']}",
        "",
    ]
    if data["errors"]:  # type: ignore[index]
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in data["errors"])  # type: ignore[index]
        lines.append("")
    else:
        lines.extend(["## Result", "", "- PASS: no protected or structural changes detected.", ""])

    if data["warnings"]:  # type: ignore[index]
        lines.extend(["## Warnings", ""])
        lines.extend(f"- {warning}" for warning in data["warnings"])  # type: ignore[index]
        lines.append("")

    protected_changes = data["protected_changes"]  # type: ignore[index]
    if protected_changes:
        lines.extend(
            [
                "## Protected Changes",
                "",
                "| Row | Handle | Field |",
                "|---:|---|---|",
            ]
        )
        for change in protected_changes[:200]:
            lines.append(
                f"| {change['row']} | `{md_escape(change['handle'])}` | `{md_escape(change['field'])}` |"
            )
        if len(protected_changes) > 200:
            lines.append(f"| ... | ... | {len(protected_changes) - 200} more |")
        lines.append("")

    allowed_changes = data["allowed_changes"]  # type: ignore[index]
    if allowed_changes:
        lines.extend(
            [
                "## Allowed Changes",
                "",
                "| Row | Handle | Field |",
                "|---:|---|---|",
            ]
        )
        for change in allowed_changes[:300]:
            lines.append(
                f"| {change['row']} | `{md_escape(change['handle'])}` | `{md_escape(change['field'])}` |"
            )
        if len(allowed_changes) > 300:
            lines.append(f"| ... | ... | {len(allowed_changes) - 300} more |")
        lines.append("")
    return "\n".join(lines)


def write_output(content: str, output: str | None) -> None:
    if output:
        Path(output).write_text(content, encoding="utf-8")
    else:
        print(content)


def command_audit(args: argparse.Namespace) -> int:
    data = audit_data(Path(args.csv))
    if args.format == "json":
        content = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        content = render_audit_markdown(data)
    write_output(content, args.output)
    return 0


def command_validate(args: argparse.Namespace) -> int:
    allowed = set(DEFAULT_EDITABLE)
    if args.allowed:
        allowed = {item.strip() for item in args.allowed.split(",") if item.strip()}
    data, exit_code = validate_data(
        Path(args.original),
        Path(args.updated),
        allowed,
        args.allow_empty_body_html,
    )
    if args.format == "json":
        content = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        content = render_validation_markdown(data)
    write_output(content, args.output)
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Audit a Shopify product CSV before editing.")
    audit.add_argument("csv")
    audit.add_argument("--format", choices=["markdown", "json"], default="markdown")
    audit.add_argument("--output")
    audit.set_defaults(func=command_audit)

    validate = subparsers.add_parser("validate", help="Validate an edited CSV against its original.")
    validate.add_argument("original")
    validate.add_argument("updated")
    validate.add_argument(
        "--allowed",
        help="Comma-separated allowed fields. Defaults to SEO Title, SEO Description, Image Alt Text.",
    )
    validate.add_argument(
        "--allow-empty-body-html",
        action="store_true",
        help="Allow Body (HTML) changes only when the original cell was empty and the updated cell is non-empty.",
    )
    validate.add_argument("--format", choices=["markdown", "json"], default="markdown")
    validate.add_argument("--output")
    validate.set_defaults(func=command_validate)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
