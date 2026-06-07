"""Entry point — delegates all logic to the SDK."""

from latex_article_generator.sdk.sdk import ArticleGeneratorSDK


def main() -> None:
    """Run the article generator via the SDK."""
    sdk = ArticleGeneratorSDK()
    print(f"LaTeX Article Generator ready. SDK initialised: {sdk}")


if __name__ == "__main__":
    main()
