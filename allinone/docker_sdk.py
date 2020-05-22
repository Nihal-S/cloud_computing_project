import requests

def spawn_slave():
    url='http://172.18.0.1:5555/containers/create'
    obj = {"image":"slave"}
    cont_create = requests.post(url, json=obj)
    print(cont_create)
    cont_id = str(cont_create.json()["Id"])
    url = 'http://172.18.0.1:5555/networks/allinone_default/connect'
    obj = {"Container":cont_id}
    net_add = requests.post(url, json=obj)
    print(net_add)
    url = 'http://172.18.0.1:5555/containers/'+cont_id+'/start'
    run_cont = requests.post(url)
    print(run_cont)
    return run_cont

spawn_slave()

# string = "docker rm 1fd1b866ef"
# l = string.split(" ")
# process = subprocess.Popen(l, stdout=subprocess.PIPE)
# stdout = process.communicate()[0]
# string = stdout.decode("utf-8")
# string = string.strip()


# import subprocess
# string = "docker inspect -f '{{.State.Pid}}' 1fd1b866ef"
# l = string.split(" ")
# process = subprocess.Popen(l, stdout=subprocess.PIPE)
# stdout = process.communicate()[0]
# string = stdout.decode("utf-8")
# string = string.strip()
# string = string[1:-1]
# print (int(string))


# import subprocess
# string = "docker stop 1fd1b866ef"
# l = string.split(" ")
# process = subprocess.Popen(l, stdout=subprocess.PIPE)
# stdout = process.communicate()[0]
# string = stdout.decode("utf-8")
# string = string.strip()
# print (string)
# string = "docker rm 1fd1b866ef"
# l = string.split(" ")
# process = subprocess.Popen(l, stdout=subprocess.PIPE)
# stdout = process.communicate()[0]
# string = stdout.decode("utf-8")
# string = string.strip()