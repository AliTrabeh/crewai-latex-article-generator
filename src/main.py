"""CLI entry point — delegates all logic to the SDK (task 033)."""

import pathlib
import sys

import truststore

truststore.inject_into_ssl()  # use OS cert store so corporate proxy certs are trusted

from dotenv import load_dotenv  # noqa: E402

from latex_article_generator.cli.parser import parse_args  # noqa: E402
from latex_article_generator.sdk.sdk import ArticleGeneratorSDK  # noqa: E402
from latex_article_generator.services.graph_generator import GraphGenerator  # noqa: E402


def _generate_graph(output_dir: str) -> str:
    """Pre-generate the accuracy bar chart; return absolute forward-slash path."""
    gen = GraphGenerator(output_dir)
    path = gen.bar_chart(
        categories=["CNN", "RNN", "Transformer", "Random Forest", "SVM"],
        values=[94, 89, 96, 87, 83],
        title="ML Algorithm Accuracy on Medical Datasets (%)",
        filename="ml_accuracy.png",
    )
    return str(pathlib.Path(path).resolve()).replace("\\", "/")


def main(argv: list[str] | None = None) -> int:
    """Parse CLI args, invoke SDK, return exit code."""
    load_dotenv()
    args = parse_args(argv)
    sdk = ArticleGeneratorSDK()

    output_dir = str(pathlib.Path(args.output).parent)
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    try:
        print(f"Generating article on: {args.topic}")
        print(f"Sections: {args.sections}")

        graph_path = _generate_graph(output_dir)
        print(f"Graph generated: {graph_path}")

        bib_path = str((pathlib.Path(output_dir) / "references.bib").resolve()).replace("\\", "/")
        print(f"Bibliography: {bib_path}")

        latex_source = sdk.generate_article(
            args.topic, args.sections, graph_path=graph_path, bib_path=bib_path
        )

        tex_path = args.output.replace(".pdf", ".tex")
        pathlib.Path(tex_path).write_text(latex_source, encoding="utf-8")
        print(f"LaTeX written to: {tex_path}")

        if args.format == "pdf":
            output_path = sdk.compile_pdf(latex_source, args.output)
            print(f"PDF written to: {output_path}")

        return 0

    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
