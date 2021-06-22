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

### Flink (embedded)

To run with the Flink Runner:

```shell
source ./venv/bin/activate
python -m apache_beam.examples.wordcount --output flink-counts \
                                         --runner FlinkRunner
```

This will run on an "embedded Flink cluster" by default. Later we can try running against a real Flink cluster running locally with docker.

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

### Flink (docker)

**NOT YET WORKING**

Now we can try standing up a flink cluster locally. Apache Beam 2.30.0 supports up to Flink 1.12 (see [Apache Beam: Flink Version Compatibility](https://beam.apache.org/documentation/runners/flink/#flink-version-compatibility)).

To start the Flink session cluster:

```shell
pushd flink
docker-compose up -d
popd
```

You can verify that the cluster is up and running by visiting the web UI at http://localhost:8081/

Now try running the wordcount task:

```shell
source ./venv/bin/activate
python -m apache_beam.examples.wordcount --output flink-docker-counts \
                                         --runner PortableRunner \
                                         --job_endpoint localhost:8099 \
                                         --flink_version 1.12 \
                                         --environment_type EXTERNAL \
                                         --environment_config localhost:50000 \
                                         --flink_submit_uber_jar
```

#### Troubleshooting

Try checking the container logs with `pushd flink; docker-compose logs -f`

## My minimal wordcount example

Here I follow the section https://beam.apache.org/get-started/wordcount-example/#minimalwordcount-example

This executes with the embedded Flink runner:

```shell
source ./venv/bin/activate
python -m wordcount-examples.my_wordcount_minimal
```

And the results match what we expect:

```shell
$ cat minimal-counts-000* | sort | md5sum
a456459c18c4b1d50d9f61b2f8946720  -
```

## My wordcount example

```shell
source ./venv/bin/activate
python -m wordcount-examples.my_wordcount
```

```shell
$ cat my-counts-000* | sort | md5sum
a456459c18c4b1d50d9f61b2f8946720  -
```
