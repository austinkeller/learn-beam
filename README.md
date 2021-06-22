# Learning Apache Beam

I'm following the learning resources here in order to better understand Apache Beam and, more generally, Dataflow: https://beam.apache.org/documentation/resources/learning-resources/

I'll be using this repo to capture the local installation process so that I can easily boot up an environment.

## Requirements

To take full advantage of the development environment:

- make
- pyenv
  - Install python 3.7.9 with `pyenv install 3.7.9`
- docker

## Environment

### Python

To create the environment, run

```shell
make venv
```

### Flink

TODO

## WordCount Examples

Follows https://beam.apache.org/get-started/wordcount-example/

[wordcount-examples](wordcount-examples)

### Direct Runner

To run on the Direct Runner:

```shell
source ./venv/bin/activate
python -m apache_beam.examples.wordcount --output counts
```

This pulls the data from GCP and then outputs to the file locally to `counts-00000-of-00001`.

### Flink

To run with the Flink Runner:

```shell
source ./venv/bin/activate
python -m apache_beam.examples.wordcount --output flink-counts \
                                         --runner FlinkRunner
```

This pulls the beam SDK docker image and apparently runs it on Flink (also a docker server?)

This outputs to several files, such as `flink-counts-00000-of-00012`.

We can verify that the counts from the Direct and Flink runners are identical by sorting and computing their hashes, like so:

```shell
$ cat counts-00000-of-00001| sort | md5sum
a456459c18c4b1d50d9f61b2f8946720  -
```

```shell
$ cat flink-counts-* | sort | md5sum
a456459c18c4b1d50d9f61b2f8946720  -
```

The hashes match, so we've achieved the same results! Running locally, the Flink runner is much slower than the direct runner, but the Flink runner will allow us to scale up to much greater volumes of data.
