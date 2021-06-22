import logging
import re

import apache_beam as beam
import click
from apache_beam.pipeline import PipelineOptions


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.option(
    "--input",
    default="gs://dataflow-samples/shakespeare/kinglear.txt",
)
@click.option("--output", type=click.Path(), default="minimal-counts")
@click.option("--loglevel", type=str, default="INFO")
@click.pass_context
def cli(ctx, input, output, loglevel):
    logging.getLogger().setLevel(loglevel.upper())

    pipeline_options = {
        ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)
    }
    print(pipeline_options)

    # options = PipelineOptions(**pipeline_options)

    pipeline_flags = [
        "--runner=FlinkRunner",
    ]

    options = PipelineOptions(pipeline_flags)
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
