"""CLI entry point — delegates all logic to the SDK (task 033)."""

import pathlib
import sys

from dotenv import load_dotenv

from latex_article_generator.cli.parser import parse_args
from latex_article_generator.sdk.sdk import ArticleGeneratorSDK


def main(argv: list[str] | None = None) -> int:
    """Parse CLI args, invoke SDK, return exit code."""
    load_dotenv()
    args = parse_args(argv)
    sdk = ArticleGeneratorSDK()

    try:
        print(f"Generating article on: {args.topic}")
        print(f"Sections: {args.sections}")

        latex_source = sdk.generate_article(args.topic, args.sections)

        if args.format == "pdf":
            output_path = sdk.compile_pdf(latex_source, args.output)
            print(f"PDF written to: {output_path}")
        else:
            tex_path = args.output.replace(".pdf", ".tex")
            pathlib.Path(tex_path).write_text(latex_source, encoding="utf-8")
            print(f"LaTeX written to: {tex_path}")

        return 0

    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
