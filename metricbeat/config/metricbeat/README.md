# Welcome to Metricbeat 6.4.1

Metricbeat is a lightweight shipper for metrics.

## Getting Started

To get started with Metricbeat, you need to set up Elasticsearch on
your localhost first. After that, start Metricbeat with:

     ./metricbeat -c metricbeat.yml -e

This will start Metricbeat and send the data to your Elasticsearch
instance. To load the dashboards for Metricbeat into Kibana, run:

    ./metricbeat setup -e

For further steps visit the
[Getting started](https://www.elastic.co/guide/en/beats/metricbeat/6.4/metricbeat-getting-started.html) guide.

## Documentation

Visit [Elastic.co Docs](https://www.elastic.co/guide/en/beats/metricbeat/6.4/index.html)
for the full Metricbeat documentation.

## Release notes

https://www.elastic.co/guide/en/beats/libbeat/6.4/release-notes-6.4.1.html
