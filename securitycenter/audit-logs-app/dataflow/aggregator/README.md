# Dataflow aggregator


## Run with direct runner

Linux

```
$ mvn compile exec:java \
      -Dexec.mainClass=com.google.log.audit.LogAggregator \
      -Dexec.args="--output=aggregate-audit-logs"
```

Windows

```
set GOOGLE_APPLICATION_CREDENTIALS=path-to-sa\sa-file.json

set JAVA_HOME=path-to-jdk


$ mvn compile exec:java ^
      -Dexec.mainClass=com.google.log.audit.LogAggregator ^
      -Dexec.args="--output=aggregate-audit-logs"
```