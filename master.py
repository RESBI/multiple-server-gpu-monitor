from flask import Flask
from flask import render_template
import requests
import json
from datetime import datetime
import pytz
from config import CONFIG

tz = pytz.timezone("Asia/Shanghai")

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

SITE_TITLE = CONFIG.get("site_title", "Server status")
TOP_MESSAGE = CONFIG.get("top_message", "Hello world")

if CONFIG.get("servers") is None:
    raise ValueError()
SERVERS = CONFIG.get("servers")


@app.route('/')
def server():
    servers = list()
    now = datetime.now(tz=tz).strftime("%Y-%m-%d %T")

    # Access and get infos.
    for server in SERVERS:
        [server_ip, server_name] = server
        try:
            resp = requests.get(f"http://{server_ip}:23333")
            # If no response
            if resp.status_code != 200:
                data = {
                    "ip": server_ip,
                    "name": server_name,
                    "active": False
                }
            else:
                data = json.loads(resp.text)
                data["ip"] = server_ip
                data["name"] = server_name
                data["active"] = True
        except:
            data = {
                "ip": server_ip,
                "name": server_name,
                "active": False
            }

        servers.append(data)

    context = {"title": SITE_TITLE,
               "top_message": TOP_MESSAGE,
               "now": now,
               "servers": servers}

    # Render the page and return.
    return render_template("index.html", **context)
