import docker
client = docker.from_env()
objectlocal = client.containers.run("slave:latest", '''sh -c "sleep 25 && python -u worker.py 0"''',detach=True,network="allinone_default") 
print((str(objectlocal)[12:-1]).strip())