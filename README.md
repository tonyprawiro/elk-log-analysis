# Log Analysis with ELK Stack

This is a collection of setup scripts and reference configuration from my previous experience setting up ELK environment for log analysis.

## cluster-setup

Shell commands and some configuration to setup the ELK platform.

## logstash

Contains the configuration files which accepts input from the beats, processing directives such as grok-patterns (10..14-*.conf), and output to elasticsearch.

There is also an outdated geoip_database.



## scripts

There are two scripts:

- Housekeeping script, to delete indexes older than X days older

- Mark latest doc, to add a custom field (is_latest=1) to the latest document in an index of certain type
