# Metricbeat vSphere module

## Description

The vSphere module uses the Govmomi library to collect metrics from any Vmware SDK URL (ESXi/VCenter). This library is built for and tested against ESXi and vCenter 5.5, 6.0 and 6.5.

By default it enables the metricsets **datastore**, **host** and **virtualmachine**.

## Setup

### Set environnement variables

For vSphere metricbeat module to work, you need to add a .env file at the root of the stack and to update your docker-compose.yml file accordingly.

Create the vsphere-variables.env file and add your vSphere credentials:

```
VSPHEREHOST=https://vcenter.ulaval.ca/sdk

VSPHEREUID=userid

VSPHEREPWD='password'
```

In the docker-compose.yml file, set the metricbeat env_file field to your vsphere-variables.env file path:

```
metricbeat:

    ...

    env_file:
      - vsphere-variables.env
```

## Exported fields

### Datastore fields [datastore metricset]

#### Datastore name
```
vsphere.datastore.name
```
type: keyword

#### Filesystem type
```
vsphere.datastore.fstype
```
type: keyword

#### Total bytes of the datastore
```
vsphere.datastore.capacity.total.bytes
```
type: long

format: bytes

#### Free bytes of the datastore
```
vsphere.datastore.capacity.free.bytes
```
type: long

format: bytes

#### Used bytes of the datastore
```
vsphere.datastore.capacity.used.bytes
```
type: long

format: bytes

#### Used percent of the datastore
```
vsphere.datastore.capacity.used.pct
```
type: long

format: percent

### Host fields [host metricset]

#### Host name
```
vsphere.host.name
```
type: keyword

#### Used CPU in Mhz
```
vsphere.host.cpu.used.mhz
```
type: long

#### Total CPU in Mhz
```
vsphere.host.cpu.total.mhz
```
type: long

#### Free CPU in Mhz
```
vsphere.host.cpu.free.mhz
```
type: long

#### Used Memory in bytes
```
vsphere.host.memory.used.bytes
```
type: long

format: bytes

#### Total Memory in bytes
```
vsphere.host.memory.total.bytes
```
type: long

format: bytes

#### Free Memory in bytes
```
vsphere.host.memory.free.bytes
```
type: long

format: bytes

#### Network names
```
vsphere.host.network_names
```
type: keyword

### Virtualmachine fields [virtualmachine metricset]

#### Host name
```
vsphere.virtualmachine.host
```
type: keyword

#### Virtual Machine name
```
vsphere.virtualmachine.name
```
type: keyword

#### Used CPU in Mhz
```
vsphere.virtualmachine.cpu.used.mhz
```
type: long

#### Used Memory of Guest in bytes
```
vsphere.virtualmachine.memory.used.guest.bytes
```
type: long

format: bytes

#### Used Memory of Host in bytes
```
vsphere.virtualmachine.memory.used.host.bytes
```
type: long

format: bytes

#### Total Memory of Guest in bytes
```
vsphere.virtualmachine.memory.total.guest.bytes
```
type: long

format: bytes

#### Free Memory of Guest in bytes
```
vsphere.virtualmachine.memory.free.guest.bytes
```
type: long

format: bytes

#### Custom fields
```
vsphere.virtualmachine.custom_fields
```
type: object

#### Network names
```
vsphere.virtualmachine.network_names
```
type: keyword

## Exported fields

### Datastore metricset

A manageable storage entity, usually used as a repository for virtual machine files including log files, scripts, configuration files, virtual disks, and so on.

```
{
    "@timestamp": "2017-10-12T08:05:34.853Z",
    "beat": {
        "hostname": "host.example.com",
        "name": "host.example.com"
    },
    "metricset": {
        "host": "http://127.0.0.1:36937/sdk",
        "module": "vsphere",
        "name": "datastore",
        "rtt": 115
    },
    "vsphere": {
        "datastore": {
            "capacity": {
                "free": {
                    "bytes": 50021150720
                },
                "total": {
                    "bytes": 63918878720
                },
                "used": {
                    "bytes": 13897728000,
                    "pct": 21
                }
            },
            "fstype": "local",
            "name": "LocalDS_0"
        }
    }
}
```

### Host metricset

A physical computer that uses virtualization software to run virtual machines. Also called the host computer, host machine, or host system

```
{
    "@timestamp": "2017-10-12T08:05:34.853Z",
    "beat": {
        "hostname": "host.example.com",
        "name": "host.example.com"
    },
    "metricset": {
        "host": "http://127.0.0.1:43843/sdk",
        "module": "vsphere",
        "name": "host",
        "rtt": 115
    },
    "vsphere": {
        "host": {
            "cpu": {
                "free": {
                    "mhz": 4521
                },
                "total": {
                    "mhz": 4588
                },
                "used": {
                    "mhz": 67
                }
            },
            "memory": {
                "free": {
                    "bytes": 2822230016
                },
                "total": {
                    "bytes": 4294430720
                },
                "used": {
                    "bytes": 1472200704
                }
            },
            "name": "localhost.localdomain"
        }
    }
}
```

### Virtualmachine metricset

A software computer that, like a physical computer, runs an operating system and applications. Multiple virtual machines can operate concurrently
on a single host system.

```
{
    "@timestamp": "2017-10-12T08:05:34.853Z",
    "beat": {
        "hostname": "host.example.com",
        "name": "host.example.com"
    },
    "metricset": {
        "host": "http://127.0.0.1:35887/sdk",
        "module": "vsphere",
        "name": "virtualmachine",
        "rtt": 115
    },
    "vsphere": {
        "virtualmachine": {
            "cpu": {
                "used": {
                    "mhz": 0
                }
            },
            "host": "ha-host",
            "memory": {
                "free": {
                    "guest": {
                        "bytes": 33554432
                    }
                },
                "total": {
                    "guest": {
                        "bytes": 33554432
                    }
                },
                "used": {
                    "guest": {
                        "bytes": 0
                    },
                    "host": {
                        "bytes": 0
                    }
                }
            },
            "name": "ha-host_VM1"
        }
    }
}
```

## Links

- [Metricbeat vSphere module configuration](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-module-vsphere.html)

- [Metricbeat vSphere module exported fields](https://www.elastic.co/guide/en/beats/metricbeat/current/exported-fields-vsphere.html)

- [Metricbeat vSphere module datastore metricset](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-metricset-vsphere-datastore.html)

- [Metricbeat vSphere module host metricset](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-metricset-vsphere-host.html)

- [Metricbeat vSphere module virtualmachine metricset](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-metricset-vsphere-virtualmachine.html)

- [VMware Glossary](https://www.vmware.com/pdf/master_glossary.pdf)

- [50 terms and acronyms for VMware that you should know](https://www.techrepublic.com/blog/data-center/50-terms-and-acronyms-for-vmware-that-you-should-know/)

- [Template grafana dashboard](https://grafana.com/dashboards/8159)

- [Template grafana dashboard - Github](https://github.com/jorgedlcruz/vmware-grafana)