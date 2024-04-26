import click
import os
import datetime as dt
from expanse.apple_health import to_df, write_parquet


@click.group()
@click.version_option()
def cli():
    "turn apple health export.xml into parquet"


@cli.command(name="parquet")
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-o",
    "--out",
    help="path where to write the parquet file",
)
def transform(path, out):
    "Command description goes here"
    cwd = os.getcwd()

    df = to_df(path)

    if out is None:
        stamp = dt.datetime.now().strftime("%Y-%m-%d")
        filename = f"apple-health-{stamp}.parquet"
        write_parquet(df, os.path.join(cwd, filename))
    else:
        write_parquet(df, out)
