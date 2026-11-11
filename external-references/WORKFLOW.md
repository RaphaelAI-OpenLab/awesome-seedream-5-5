# How to remake external Seedream 5.5 references

These are third-party source images and prompts collected for research, not Raphael-generated works.

## Suggested states

- pending: the source image and source-attributed prompt have been collected but no new image has been generated
- recreated: a fresh image has been actually generated, checked, and recorded
- published: the recreated image has been reviewed for rights and deliberately approved for external publication

## Remake procedure

1. Open each case page and verify its original source and prompt. Check whether the prompt may be reused under the source site's terms.
2. When a reference image is required, use only properly licensed or owned inputs. Do not copy identifiable people, protected characters, branded packaging, or distinctive copyrighted compositions without clearance.
3. Generate a new work with the intended model; log actual model identifier, seed if supported, aspect ratio, prompts, inputs, generation date, and owned output path.
4. Save your generation under external-references/remade/<case-id>/ and update cases.json: remake.status = recreated and remake.own_media with the new files and provenance.
5. Run python3 scripts/build_external_refs.py and python3 scripts/validate_external_refs.py. Review the rendered pages and previews.
6. Before publishing to the main case collection, remove any unlicensed third-party reference thumbnails or obtain explicit permission. A fresh generation is not automatically free from copyright, brand or likeness conflicts.

Reference previews are deliberately low-resolution and should not be presented as licensed media, or used as promotional assets. Source web URLs remain available for provenance.
