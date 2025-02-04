To monite RAM and GPU usage on multiple servers.

In a computer science lab or company, you usually have multiple servers and GPUs running many deep learning experiments. You want to know which device is working and which is available at a glance with a minimum setup.

## Screenshots

![](images/DeepinScreenshot_select-area_20230106200637.png)

## Installation

```shell
git clone https://github.com/kehanlu/server-monitor
cd server-monitor
pip install -r requirements.txt
```

- `nvidia-smi`: https://www.nvidia.com


## Usage

![](images/2021-02-04-04-53-08.png)

### Server

"Server" means the server you want to monitor.

1. Go to server you want to monitor
    - You have to be sure that `nvidia-smi` command is installed.

2. run the command to start an API.

```shell
gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:23333 server:app --daemon
```

### Master

"Master" means the web server which is going to fetch data from each servers. You can run this web server on any computer. In some case, you might want this web server to be accessible from public network, but still hide servers behind a firewall.

1. Edit `config.py`

2. In `config.py`, you need to have a list of server ips. Then the web server will iterate from the list and GET the API at `http://{ip}:23333`.

- `servers` : server IPs and their names
- `site_title(optional)`: the title of website
- `top_message(optional)`: the message shows on the top

```python
CONFIG = {
    "site_title": "Server status",
    "top_message": "Hello world",
    "servers": [
        ["192.168.0.2", "name1"],
        ["192.168.0.3", "name2"],
        ["192.168.0.4", "name3"],
    ],
}

```

3. run the command to start the server.

```shell
gunicorn -w 1 -b 0.0.0.0:8787 master:app
```

4. Visit `127.0.0.1:8787` or `<your_ip>:8787` to see the website.

### Systemctl startup configuration

You could do this by following https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04#step-4-configuring-gunicorn

#### Notice that it's necessary to change the bianry executing code into using the absolute path

That is, change this
```python
        ...
        info = os.popen("free -m").read().split('\n')[1].split()
        ...
```
into something like this
```python
        ...
        info = os.popen("/usr/bin/free -m").read().split('\n')[1].split()
        ...
```
By using `which` command to check the absolute path of `free` and `nvidia-smi`.

## Contribution

Pull requests are welcome. This is still an early project (and just for fun).

TODOs:

- Autorefresh
- Intel Xeon Phi Coprocessor supportance
