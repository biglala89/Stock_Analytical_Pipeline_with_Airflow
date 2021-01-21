## Stock-Pipeline_with-Airflow

### Objective
The goal of this mini project is to use airflow DAG to automate the authoring, scheduling and monitoring a data pipeline for a few stocks that are publicly trading on the stock market and analyze their trend and behaviors.

To run the program, consider using a docker image configured for running airflow jobs. 

First, pull the image from docker hub using this command: 
```bash
docker pull puckel/docker-airflow
```

To run the container, use the following command:
```bash
docker run -d -p 8080:8080 \
-v $(PWD)/dags:/usr/local/airflow/dags \
-v $(PWD)/logs:/usr/local/airflow/logs \
-v $(PWD)/requirements.txt:/requirements.txt \
-v $(PWD)/script:/usr/local/airflow/script \
-v $(PWD)/tmp/data:/usr/local/airflow/tmp/data \
puckel/docker-airflow webserver
```

The volumes are shared between local host system and the container and are persisted even after the container is stopped.
