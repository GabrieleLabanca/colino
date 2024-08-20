import click


@click.group()
def cli():
    """News Aggregator CLI"""
    pass


@cli.command()
def collect():
    """Collect daily articles"""
    click.echo("Collecting daily articles...")


@cli.command()
def search():
    """Search for relevant articles"""
    click.echo("Searching for relevant articles...")


@cli.command()
def synthesize():
    """Synthesize weekly topics"""
    click.echo("Synthesizing weekly topics...")


@cli.command()
@click.option("--port", default=5000, help="Port to run the web interface on")
def serve(port):
    """Start the web interface"""
    click.echo(f"Starting web interface on port {port}...")


if __name__ == "__main__":
    cli()
