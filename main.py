import json
import click
from src.collect_articles import fetch_articles, article_to_dict, transform_articles
from src.database import insert_articles
from itertools import batched
from prpl import prpl

@click.group()
def cli():
    """News Aggregator CLI"""
    pass


def etl_website(source):
    url = source["url"]
    name = source["name"]

    click.echo(f"Collecting daily articles from {url}...")
    articles = fetch_articles(url)
    click.echo(f"\t ... {len(articles)} collected...")
    transformed_articles = transform_articles(articles, name)
    insert_articles(transformed_articles)
    click.echo("\t ... inserted into the database.")



@cli.command()
@click.option(
    "--file",
    default="list_of_sources.json",
    help="""a file like [{"name": "news24", "url": "news24.com"}]""",
)
def collect_websites(file):
    """Collect daily articles"""
    with open(file) as f:
        sources = json.load(f)

    for source in sources:
        etl_website(source)
    # res = prpl(target_list=sources, target_function=etl_website , timer=True)




@cli.command()
def search():
    """Search for relevant articles"""
    click.echo("Searching for relevant articles...")


@cli.command()
def synthesize():
    """Synthesize weekly topics"""
    click.echo("Synthesizing weekly topics...")



if __name__ == "__main__":
    cli()
