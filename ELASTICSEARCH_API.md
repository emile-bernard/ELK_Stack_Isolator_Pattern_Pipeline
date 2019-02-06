# Elasticsearch API

## Description
You can fix the low cluster health by updating elasticsearch index with CURL or Postman. For the purposes of this project (and a slick GUI) I chose postman.

This bug is caused by having a document type mismatch and can be fixed by setting the number of shards to 1 and the number of replicas to 0.

## Step-by-Step solution
- Retrieve the full list of templates with
```
GET localhost:9200/_template
```

- Retrieved a single template with
```
GET localhost:9200/_template/template_name
```

Alternatively you can check if a tempklate exists with
```
HEAD localhost:9200/_template/template_name
```

- Edit a single template with
```
PUT localhost:9200/_template/template_name
```
With the following raw JSON(application/json) body
```
{
    "index_patterns": ["*"],
    "order" : 0,
    "settings" : {
    	"number_of_shards" : "1",
    	"number_of_replicas" : "0"
    }
}
```

- Delete all index with
```
DELETE localhost:9200/*
```

- Update your metricbeat.yml logstash output with
```
output.logstash:
  hosts: ["proxy:5044"]
  setup.template.json.enabled: true
  setup.template.json.path: "template.json"
  setup.template.json.name: "template-name"
```

## Links
- [Index API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html)