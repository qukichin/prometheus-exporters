from configparser import ConfigParser
import requests

requests.packages.urllib3.disable_warnings()    # 控制台输出移除 SSL 认证警告

CODE = (200, 301, 302, 304)
confile = "./config.ini"


def show_configuration(encoding='utf-8') -> dict:
    cfg = ConfigParser()
    cfg.read(confile, encoding)
    return {
        sect: {k: v for k, v in cfg[sect].items()}
        for sect in cfg.sections()
    }


def geturl(timeout=30) -> dict:
    parameter = show_configuration()
    d = {}
    for name in parameter:
        http_url = parameter[name].get('http_url')
        http_user = parameter[name].get('http_user')
        http_password = parameter[name].get('http_password')

        try:
            if http_url and not (http_url and http_password):
                res_code = requests.get(
                    http_url,
                    timeout=timeout,
                    verify=False
                ).status_code

            if http_url and http_user and http_password:
                res_code = requests.get(
                    http_url,
                    timeout=timeout,
                    verify=False,
                    auth=(http_user, http_password)
                ).status_code
        except:
            res_code = 400

        d[name] = 1 if res_code in CODE else 0

    return d
