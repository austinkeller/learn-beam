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
@click.option("--output", type=click.Path(), default="my-counts")
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
        lines = p | beam.io.ReadFromText(input)
        counts = lines | CountWords()
        formatted = counts | "FormatOutput" >> beam.ParDo(FormatAsTextFn())
        formatted | beam.io.WriteToText(output)


class FormatAsTextFn(beam.DoFn):
    def process(self, element):
        word, count = element
        yield "%s: %s" % (word, count)


@beam.ptransform_fn
def CountWords(pcoll):
    return (
        pcoll
        # Convert lines of text into individual words
        | "ExtractWords" >> beam.FlatMap(lambda x: re.findall(r"[A-Za-z\']+", x))
        # Count the number of times each word occurs
        | beam.combiners.Count.PerElement()
    )


if __name__ == "__main__":
    cli()
