(venv) student@edge:~/IdeaProjects/UrbanAirMonitor$ docker-compose up
WARNING: Found orphan containers (urbanairmonitor_task_2_1) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
Recreating urbanairmonitor_task2_edge_cloud_1 ... error

ERROR: for urbanairmonitor_task2_edge_cloud_1  Cannot start service task2_edge_cloud: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: exec: "/usr/src/app/run": stat /usr/src/app/run: no such file or directory: unknown

ERROR: for task2_edge_cloud  Cannot start service task2_edge_cloud: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: exec: "/usr/src/app/run": stat /usr/src/app/run: no such file or directory: unknown
ERROR: Encountered errors while bringing up the project.
