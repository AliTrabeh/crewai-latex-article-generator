"""Entry point — delegates all logic to the SDK."""

from dotenv import load_dotenv

load_dotenv()

from latex_article_generator.sdk.sdk import ArticleGeneratorSDK  # noqa: E402


def main() -> None:
    """Run the article generator via the SDK."""
    sdk = ArticleGeneratorSDK()
    print(f"LaTeX Article Generator ready. SDK initialised: {sdk}")


if __name__ == "__main__":
    main()
