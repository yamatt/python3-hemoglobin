import click

from .hemoglobin import Hemoglobin
from .grammarbot import Language
from .rendering import render_human, render_json


@click.command()
@click.option(
    "--apikey",
    help="Your API key",
    envvar="HEMOGLOBIN_GRAMMARBOT_API_KEY",
)
@click.option("--path", help="Where to find these files to parse.", multiple=True)
@click.option(
    "--language",
    help="Language to use.",
    default="en_US",
    type=click.Choice(Language, case_sensitive=False),
)
@click.option("--use-json", "use_json", is_flag=True, help="Use JSON output")
def main(apikey, path, language, use_json):
    hemoglobin = Hemoglobin(apikey=apikey, paths=path, language=language)
    if use_json:
        render_json(hemoglobin)
    else:
        render_human(hemoglobin)

if __name__ == "__main__":
    main()
