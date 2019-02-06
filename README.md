# Stack Elk Proxy Redis

This project contains a basic docker-compose ELK stack using the logstash output isolator pattern.

## Contributor covenant code of conduct

Please acknowledge our [code of conduct](./CODE_OF_CONDUCT.md).
  
## Pipeline

(user) => kibana => elasticsearch => logstash => redis => proxy => filebeat/metricbeat => (data)

  Container  | Description   | Port
------------ | ------------- | -------------
[Kibana Production](https://www.elastic.co/products/kibana) | Open source data visualization plugin for Elasticsearch | 5601 (exposed)
[Kibana Development](https://www.elastic.co/products/kibana) | Open source data visualization plugin for Elasticsearch | 5602 (exposed)
[Elasticsearch Production](https://www.elastic.co/products/elasticsearch) | Search engine based on the Lucene library | 9200 (exposed)
[Elasticsearch Development](https://www.elastic.co/products/elasticsearch) | Search engine based on the Lucene library | 9200 (exposed)
[Logstash Production](https://www.elastic.co/products/logstash) | Open source, server-side data processing pipeline that ingests data from a multitude of sources simultaneously, transforms it, and then sends it to your favorite “stash.” | 5044 (not exposed)
[Logstash Development](https://www.elastic.co/products/logstash) | Open source, server-side data processing pipeline that ingests data from a multitude of sources simultaneously, transforms it, and then sends it to your favorite “stash.” | 5044 (not exposed)
[Redis Production](https://redis.io/) | Open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker | 6379 (exposed)
[Redis Development](https://redis.io/) | Open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker | 6379 (exposed)
[Proxy](https://www.elastic.co/products/logstash) | Open source, server-side data processing pipeline that ingests data from a multitude of sources simultaneously, transforms it, and then sends it to your favorite “stash.” | 5044 (not exposed)
[Filebeat](https://www.elastic.co/products/beats/filebeat) | Lightweight Shipper for Logs | default (not exposed)
[Metricbeat](https://www.elastic.co/products/beats/metricbeat) | Lightweight Shipper for Metrics | default (not exposed)
[Packetbeat](https://www.elastic.co/products/beats/packetbeat) | Lightweight Shipper for Network Data | default (not exposed)
[Auditbeat](https://www.elastic.co/products/beats/auditbeat) | Lightweight Shipper for Audit Data | default (not exposed)

> Note: Some of the containers listed here are commented out in the dokcer-compose.yml file. You can use them by uncomment them.

There's 3 queues between proxy and redis:

    1)UL_GEN => data_type: "list"

    2)UL_REPLAY_ENA => data_type: "list"

    3)UL_REPLAY_MPO => data_type: "list"

## Architecture

A complete description of this stack architecture can be found below.

### ELK Stack Diagram

![ELK Stack Isolator Pattern Diagram](Documentation/ELK_Stack/ELK_Stack_Isolator_Pattern_Diagram.jpg?raw=true "ELK Stack Isolator Pattern Diagram")

### ELK Stack Scripts Diagram

![ELK Stack Isolator Pattern Scripts Diagram](Documentation/ELK_Stack/ELK_Stack_Isolator_Pattern_Scripts_Diagram.jpg?raw=true "ELK Stack Isolator Pattern Scripts Diagram")

### Persistant Redis Script Sequence Diagram

![Persistant Redis Script Sequence Diagram](Documentation/Persistant_Redis/PersistantRedisScriptsSequenceDiagram.jpg?raw=true "Persistant Redis Script Sequence Diagram")

### The output isolator pattern

You can use the output isolator pattern to prevent Logstash from becoming blocked if one of multiple outputs experiences a temporary failure. Logstash, by default, is blocked when any single output is down. This behavior is important in guaranteeing at-least-once delivery of data.

For example, a server might be configured to send log data to both Elasticsearch and an HTTP endpoint. The HTTP endpoint might be frequently unavailable due to regular service or other reasons. In this scenario, data would be paused from sending to Elasticsearch any time the HTTP endpoint is down.

Using the output isolator pattern and persistent queues, we can continue sending to Elasticsearch, even when one output is down.

> Note that this approach uses up to N times as much disk space and incurs N times as much serialization/deserialization cost as a single pipeline (Where N is the total number of pipeline used).

## Metricbeat vSphere module

A complete description of this module and it's fields can be found here: 
[vSphere](VSPHEREMODULE.md)

## Packetbeat module configuration

To enable packetbeat to sniff packets in a container inside the stack (in this example the redis container) this as to be done in the docker-compose.yml file.

```
cap_add: ['NET_RAW', 'NET_ADMIN']
network_mode: "container:redis"
```

## Run the stack

In the same command line session where you previously exported your environnement variables:

- Run with output
```
$ docker-compose up
```

- Run without output
```
$ docker-compose up -d
```

- Follow the output when the stack runs in daemon (-d)
```
$ docker-compose logs -f | grep -v kibana_1
```

- Restart filebeat and reinject all logs (while the stack is up)
```
$ docker-compose stop filebeat; rm filebeat/config/data/registry; docker-compose start filebeat
```

- Monitor redis
```
$ redis-cli --stat
```

## Docker compose

### Install and release

[Install](https://docs.docker.com/compose/install/)

[Release](https://github.com/docker/compose/releases)

### Working with containers and images

- Open container
```
$ docker exec -ti [container name(ex: bd04...)] /bin/bash
```

- Remove all containers and images
```
#!/bin/bash
# Delete all containers
$ docker rm $(docker ps -a -q)
# Delete all images
$ docker rmi $(docker images -q)
# Maintenant la commande purge existe:
$ docker [image|container|volume|network|system] purge
```

- List stopped containers
```
$ docker ps -q --filter "status=exited"
```

- Remove stopped containers
```
$ docker rm $(docker ps -q --filter "status=exited")
```

- Clean up any resources — images, containers, volumes, and networks — that are dangling (not associated with a container)
```
$ docker system prune
```

- Remove dangling volumes: 
[Remove dangling volumes](https://stackoverflow.com/questions/27812807/orphaned-docker-mounted-host-volumes)

- List all orphaned volumes and Eliminate all of them
```
$ docker volume ls -qf dangling=true
$ docker volume rm $(docker volume ls -qf dangling=true)
```

- Alias to have the container name in stats
```
$ alias ds='docker stats --format "table {{.Name}}\t{{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.MemPerc}}\t{{.PIDs}}"'
```

- Get containers IP adresses
```
$ docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aq)
```

- Follow logs from a single container
```
$ docker-compose logs -f [Container Name]
```

- Get container CPU%, MEM USAGE/LIMIT, MEM%, NET I/O, BLOCK I/O, PIDS
```
$ docker stats [Container Name]
```

### Publish a docker image

An example of a script used to publish docker images from their respective Dockerfile.
[Build Image And Push Script](https://gitea.avd.ulaval.ca/AVD/avddockers/src/branch/master/drill/buildimage_and_push.sh)

## Common bugs

- Low cluster health: Can be fixed with API requests as described here: 
[Elasticsearch API](https://gitea.avd.ulaval.ca/ember89/stack_elk_proxy_redis/src/commit/09d360490bbf997d7106b4f81b815e512c9f5855/ELASTICSEARCH_API.md)

## Tools

- [AVDCLI redis tools](https://gitea.avd.ulaval.ca/ember89/avdcli_redis_tools)

- [Docker compose](https://docs.docker.com/compose/install/)

- [Redis desktop manager](https://redisdesktop.com/)

- [Redis command line tool](https://redis.io/topics/rediscli)

- [Draw.io](https://www.draw.io/)

## Links

### Docker

- [Pass environment variables to containers](https://docs.docker.com/compose/environment-variables/#pass-environment-variables-to-containers)

- [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

- [10 tips for docker-compose with multiple dockerfiles](https://nickjanetakis.com/blog/docker-tip-10-project-structure-with-multiple-dockerfiles-and-docker-compose)

- [Multiple dockerfiles in project](https://stackoverflow.com/questions/27409761/multiple-dockerfiles-in-project)

- [Docker ELK stack for devops](https://medium.com/tech-tajawal/elk-stack-docker-playground-for-devops-221179ca00dd)

### Elasticsearch

- [Elasticsearch API documentation](ELASTICSEARCH_API.md)

### Logstash

- [Logstash pipeline isolator pattern](https://www.elastic.co/guide/en/logstash/6.3/pipeline-to-pipeline.html)

### Redis

- [Top-5 redis performance metrics](https://www.datadoghq.com/pdf/Understanding-the-Top-5-Redis-Performance-Metrics.pdf)

- [Official redis documentation](https://redis.io/)

- [Redis with python (redis library documentation)](https://redis-py.readthedocs.io/en/latest/)

### Kibana

- [Kibana config](https://github.com/elastic/kibana/blob/master/config/kibana.yml)

### Beats

- [Filebeat](https://www.elastic.co/products/beats/filebeat)

- [Metricbeat](https://www.elastic.co/products/beats/metricbeat)

- [Packetbeat](https://www.elastic.co/products/beats/packetbeat)

- [Auditbeat](https://www.elastic.co/products/beats/auditbeat)

### Markdown

- [Mastering markdown guide](https://guides.github.com/features/mastering-markdown/)

- [Markdown real-time collaboration tool](https://hackmd.io/)