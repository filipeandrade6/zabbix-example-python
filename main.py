from getpass import getpass
import requests
import json
import traceback


class Zabbix:
    def __init__(self, endereco_zabbix):
        self.zabbix_url = "http://" + endereco_zabbix + "/zabbix/api_jsonrpc.php"
        self.usuario = ""
        self.auth = ""
    
    def login(self, usuario, senha):
        self.usuario = usuario
        payload = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.usuario,
                "password": senha,
                },
            "auth": None,
            "id": 0,
        }    
        res = requests.post(self.zabbix_url, data=json.dumps(payload), headers={"Content-type": "application/json"})
        self.auth = res.json()["result"]

    def logout(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "user.logout",
            "params": [],
            "auth": self.auth,
            "id": 0,
        }
        _ = requests.post(self.zabbix_url, data=json.dumps(payload), headers={"Content-type": "application/json"})

    # Exemplo de método que pega os gráficos que um host
    def graphs_from_host(self, hostid):
        payload = {
            "jsonrpc": "2.0",
            "method": "graph.get",
            "params": {
                "output": "extend",
                "hostids": hostid,
                "sortfield": "name"
            },
            "auth": self.auth,
            "id": 1
        }
        res = requests.post(self.zabbix_url, data=json.dumps(payload), headers={"Content-type": "application/json"})
        resultados = res.json()["result"]

        for resultado in resultados:
            print(resultado)


endereco_zabbix = input("endereco (10.91.1.110): ") or "10.91.1.110"
usuario_zabbix = input("usuario: ")
senha_zabbix = getpass("senha: ")
hostid = input("HostID: ")

try:
    z = Zabbix(endereco_zabbix)
    z.login(usuario_zabbix, senha_zabbix)
    z.graphs_from_host(hostid)

except Exception:
    # Exibi na tela em caso de erro
    print(traceback.format_exc())
finally:
    # No final ou em caso aconteça erro na execução é executado o logout
    z.logout()
