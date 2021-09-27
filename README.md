
# Mk

## Description

Given the problematic, I opted for an Airflow solution which could appear excessive for one job only but it could handle whole workflow based process
in a company.

This solution is only a POC that is destined to be run locally.

For a production environment, I would have used Terraform to deploy Airflow and the service (the service image would have been hosted on a private repository). The DAGs would have been synchronized with the GIT repository.

I decided to store all stats in a PostgreSQL database and schedule an Airflow task to aggregate the data in a second table (stats).

Another cleaning Job could delete stats older than 10min for example in the non aggregated table.

The API workers could scale behind a Load balancer and the Celery workers aswell (this article looked promising: https://medium.com/back-market-engineering/how-to-improve-scalability-for-celery-on-kubernetes-16280ce547fb).

The docker-compose will show a connection error with PostgreSQL but the pod will retry. A better way to handle this would have been an health check preventing from starting the container until the connection is OK.

This POC lacks of test and logging aswell.

##  Requirements

    - Minikube - Tested with:
        minikube version: v1.21.0
        commit: 76d74191d82c47883dc7e1319ef7cebd3e00ee11
    - Helm - Tested with:
        Version:"v3.6.1", GitCommit:"61d8e8c4a6f95540c15c6a65f36a6dd0a45e7a2f"
    - Docker - Tested with:
        Docker version 20.10.7, build f0df350




## How To ?

### Start the stack

```
    make start
```

`make start` will start the minikube server with the DAGs mount point and install Airflow via Helm. The docker-compose stack will then be started.

Once the stack is up, `make forward_port` will make the AiflowUI available at `localhost:8000`.

The stats image will have to be built in order to be used by the KubernetesPodOperator: `make build_image`.

### Stop the stack

```
    make stop
```

`make stop` will stop the docker-compose stack, delete Airflow from minikube then delete the minikube cluster.

### Build the ingestor Docker image

```
    make build_image
```

This command will synchronize the local / minikube Docker registry. The built image will thus be available from the KubernetesPodOperator.


*Note:* Basically, the process is to have two terminals, one to start the stack, and one to build the image run by the *KubernetesPodOperator*.


## Endpoints

    - localhost:8000: Airflow WebUI (The port needs to be forwarded !)
    - localhost:80/stats POST


