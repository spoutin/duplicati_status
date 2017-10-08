import json
import requests
import models
from properties import default_server, port, backup_api


class BackupIdNotFound(Exception):
    pass


def discovery(server=default_server):
    conn = requests.session()
    response = conn.get('http://' + server + ':' + str(port))
    xsrf_token = response.cookies.get('xsrf-token')
    xsrf_token = requests.utils.unquote(xsrf_token)

    status = conn.get('http://' + server + ':' + str(port) + backup_api, headers={'X-XSRF-Token': xsrf_token})
    backupJson = json.loads(str(status.text))
    myBackup = []
    for backup in backupJson:
        myBackup.append(models.get_model(backup).data)
    return myBackup


def get_backup_details(id, server=default_server):
    discovery_result = discovery(server=server)
    for d in discovery_result:
        if d.id == str(id):
            return d
    raise BackupIdNotFound("ID:{} not found".format(id))
