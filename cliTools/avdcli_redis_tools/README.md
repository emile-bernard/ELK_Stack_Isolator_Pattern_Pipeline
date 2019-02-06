# avdcli_redis_tools 

avdcli_redis_tools est un outil utiliser conjointement avec une stack ELK docker pour assurer la cohérence et la performance de l'image redis. Cet outil comporte deux scripts qui scripts, soit : janitor et publisher.

## Scripts

- janitor efface des documents d'une liste et garde les plus récents.

- publisher prend les éléments d'une liste et les publient sur un channel.

## Venv

Pour utiliser les scripts on doit etre dans un environnement virtuel
```
$ . venv/bin/activate
```

## Utilisation de janitor

Run sans logs
```
$ python3 avd_redis_tools/janitor.py -H localhost -P 6379 -D 0 -N 1000 -K UL_REPLAY_*
```

Run avec logs
```
$ python3 avd_redis_tools/janitor.py -H localhost -P 6379 -D 0 -N 1000 -K UL_REPLAY_* --log-filename testLogFile
```

Run avec niveau de verbosite
```
$ python3 avd_redis_tools/janitor.py -H localhost -P 6379 -D 0 -N 1000 -K UL_REPLAY_* -vvv
```

## Utilisation de publisher

Run sans logs
```
$ python3 avd_redis_tools/publisher.py -H localhost -P 6379 -D 0 -L UL_REPLAY_* -N 10
```

Run avec logs
```
$ python3 avd_redis_tools/publisher.py -H localhost -P 6379 -D 0 -L UL_REPLAY_* -N 10 --log-filename testLogFile
```

Run avec niveau de verbosite
```
$ python3 avd_redis_tools/publisher.py -H localhost -P 6379 -D 0 -L UL_REPLAY_* -N 10 -vvv
```

## Utilisation des tests unitaires

Tests de Janitor
```
$ python3 tests/test_suite_janitor.py
```

Tests de Publisher
```
$ python3 tests/test_suite_publisher.py
```

## Architecture

![ELK Stack Diagram](https://gitea.avd.ulaval.ca/ember89/stack_elk_proxy_redis/src/commit/24fc55febdc1b1356d192b97c23f827893bbca74/doc/ELK_Stack_Diagram.jpg)

![Persistant Redis Sequence Diagram](https://gitea.avd.ulaval.ca/ember89/stack_elk_proxy_redis/src/commit/b121acdc8227b01386e0845b4a82359a3b89d385/doc/PersistantRedisScriptsSequenceDiagram.jpg)

![ELK Stack Scripts Diagram](https://gitea.avd.ulaval.ca/ember89/stack_elk_proxy_redis/src/commit/6339791fee571c298f5ec991f2555c33bfcb2e43/doc/ELK_Stack_Scripts_Diagram.jpg)

![Persistant Redis Script Sequence Diagram](https://gitea.avd.ulaval.ca/ember89/stack_elk_proxy_redis/src/commit/3037f7bb368295c82a35a698743a2da7d183e03d/doc/PersistantRedisSequenceDiagram.jpg)

## Liens

[Top-5-Redis-Performance-Metrics](https://www.datadoghq.com/pdf/Understanding-the-Top-5-Redis-Performance-Metrics.pdf)

[Official Redis Doc](https://redis.io/)

[Redis desktop manager](https://redisdesktop.com/)

[Redis command line tool](https://redis.io/topics/rediscli)

[Redis with python (redis library documentation)](https://redis-py.readthedocs.io/en/latest/)

[Unit testing a plumbum cli app](https://searchcode.com/codesearch/view/94387427/)

[Drone Configuration)](https://docs.drone.io/cli/setup/)

[Drone Exec](https://docs.drone.io/cli/drone-exec/)