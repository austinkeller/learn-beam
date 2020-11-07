import logging
import re

import apache_beam as beam
import click
from apache_beam.pipeline import PipelineOptions, StandardOptions


@click.command()
@click.option(
    "--input",
    default="gs://dataflow-samples/shakespeare/kinglear.txt",
)
@click.option("--output", type=click.Path(), default="counts")
@click.option("--runner", default="DirectRunner")
@click.option("--loglevel", type=str, default="INFO")
def cli(input, output, runner, loglevel):
    logging.getLogger().setLevel(loglevel.upper())
    options = PipelineOptions()
    options.view_as(StandardOptions).runner = runner
    with beam.Pipeline(options=options) as p:
        (
            p
            | beam.io.ReadFromText(input)
            | "ExtractWords"
            >> beam.FlatMap(lambda line: re.findall(r"[A-Za-z\']+", line))
            | "CountElements" >> beam.combiners.Count.PerElement()
            | "FormatOutput"
            >> beam.MapTuple(lambda word, count: "%s: %s" % (word, count))
            | beam.io.WriteToText(output)
        )


if __name__ == "__main__":
    cli()
