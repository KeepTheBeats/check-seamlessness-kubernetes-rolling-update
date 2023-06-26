# Validate the seamlessness of Kubernetes Rolling Update
This is an experiment to validate the seamlessness of Kubernetes Rolling Update.

My Kubernetes version is `v1.26.3` with the git commit `9e644106593f3f4aa98f8a84b23db5fa378900bd`.

---
## An example to use `check.py`.
If I want to check the service url `http://192.168.100.31:30001` with the expected HTTP status code `200`, I should run `python3 -u check.py http://192.168.100.31:30001 200`. After collecting enough data, I can use `Ctrl+C` to stop this program and save data in to `check.csv`. The program will check the service without any interval until receiving "Ctrl+C".

## An example to use `kubectl_rolling_update.py`.
If I want to triger the rolling update of a deployment named `deploy1` in namespace `ns1`, migrating its pod to a node named `node1`, I should run `python3 -u kubectl_rolling_update.py deploy1 ns1 node1`. This program will record the start time and end time of the rolling update, and save them in to `update.csv`.

## An example to use `plotting.py`.
After generating the files `check.csv` and `update.csv` using `check.py` and `kubectl_rolling_update.py`, I can run `python3 -u plotting.py` to plot the figure to show the downtime of this service during a Kubernetes rolling update.


## The steps of my experiment.
1. I run a `Deployment` of `nginx:1.17.1` in Kubernetes with a `Service` and only `1` pod. The `maxUnavailable` is `0` and `maxSurge` is `1`. I also have `2` Kubernetes `Nodes`.
2. I use `check.py` to continually access the `Service` of this `Deployment`.
3. I use `kubectl_rolling_update.py` to trigger a `rolling update` by changing the `NodeName` to migrate the pod between the `2` Kubernetes `Nodes`.
4. After the `rolling update`, I stop `check.py`.
5. I collect the data, `check.csv` and `update.csv`, and use `plotting.py` to plot them.



