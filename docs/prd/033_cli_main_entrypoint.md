---
id: "033"
title: "CLI Main Entry Point"
group: "10 — CLI Entry Point"
priority: high
status: NOT_STARTED
---

# Task 033 — CLI Main Entry Point

## Goal

Implement `src/main.py` as the CLI entry point that parses arguments, invokes the SDK, handles errors, and exits with appropriate codes.

## Files to Create or Modify

- `src/main.py` — full implementation (replace skeleton)

## Exact Expected Behavior

```python
import sys
from latex_article_generator.cli.parser import parse_args
from latex_article_generator.sdk.sdk import ArticleGeneratorSDK

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    sdk = ArticleGeneratorSDK()

    print(f"Generating article on: {args.topic}")
    print(f"Sections: {args.sections}")

    latex_source = sdk.generate_article(args.topic, args.sections)

    if args.format == "pdf":
        output_path = sdk.compile_pdf(latex_source, args.output)
        print(f"PDF written to: {output_path}")
    else:
        import pathlib
        tex_path = args.output.replace(".pdf", ".tex")
        pathlib.Path(tex_path).write_text(latex_source, encoding="utf-8")
        print(f"LaTeX written to: {tex_path}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Acceptance Criteria

- [ ] `python src/main.py --topic "AI" --format latex` exits 0 and writes a `.tex` file.
- [ ] `python src/main.py --topic "AI" --format pdf` exits 0 and writes a `.pdf` file.
- [ ] Runtime exceptions from the SDK print a clear error message and exit with code 1.
- [ ] `main(["--topic", "AI"])` is callable from tests with a mock SDK.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- Wrap the SDK call in try/except and print to stderr on failure:
  ```python
  except Exception as exc:
      print(f"Error: {exc}", file=sys.stderr)
      return 1
  ```
- `main()` must return an integer exit code, not call `sys.exit()` internally (caller does that).
- `src/main.py` is excluded from coverage measurement (see `pyproject.toml` `omit` list).
