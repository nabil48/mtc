# original source code by http://github/nabil48
from requests import Session
import json
import sys
import argparse
from colorama import Fore, Back
from config import config


class Mtc:
    def __init__(self, **config):
        self.headersJson = {
            "Host": "saosdeveloper.club",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0"
        }
        self.payload = {
            "id": config["id"]
        }

    def _request(self, url, post=True, **kwargs):
        try:
            rs = Session()
            if post:
                result = rs.post(url=url, **kwargs)
            else:
                result = rs.get(url=url, **kwargs)
            if int(result.status_code) == 200:
                if result.headers["Content-Type"] == "aplication/json":
                    return result.json()
                else:
                    return result.text
            else:
                return result.text
        except ConnectionError as e:
            print("{r}{msg}{fr}".format(r=Back.RED, fr=Back.RESET, msg=str(e)))

    def balance(self):
        url = "http://saosdeveloper.club/mtc/loadbalance.php"
        result = self._request(url=url, post=False,
                               params=self.payload, headers=self.headersJson)
        return result

    def solvedTask(self):
        url = "http://saosdeveloper.club/mtc/mtcreward.php"
        result = self._request(url=url, post=False,
                               params=self.payload, headers=self.headersJson)
        return result
    
    def solvedChallange(self, count):
        url = "http://saosdeveloper.club/mtc/challangereward.php"
        self.payload["count"] = count
        result = self._request(url=url, post=False,
                               params=self.payload, headers=self.headersJson)
        return result
    
    def getChallange(self):
        pass


def command(args=None):
    parse = argparse.ArgumentParser(
        description="wellcome in mathematic faucet pro")
    parse.add_argument("-b", "--balance",
                       help="show account balance", action="store_true")
    parse.add_argument("-st", "--startTask",
                       help="solved the task", action="store_true")
    parse.add_argument("-sc", "--startChallange",
                       help="solved the challange", action="store_true")
    result = parse.parse_args(args)
    return (result.balance, result.startTask, result.startChallange)


botmtc = Mtc(**config)


def do_balance():
    balance = json.loads(botmtc.balance())
    print(" saldo akun anda adalah {g}{balance} MTC{rs}".format(
        balance=balance[0]["wallet"], g=Fore.GREEN, rs=Fore.RESET))


def do_startTask():
    try:
        print("{y}{b}press CTRL+C for stop this job's{br}{fr}".format(
            y=Back.YELLOW, br=Back.RESET, b=Fore.BLACK, fr=Fore.RESET))
        print("Bot Is Starting!!!......")
        while True:
            result = botmtc.solvedTask()
            try:
                print("{b}[+]{fr}{g}{msg}{fr} >> Current Ballance {y}{saldo} MTC{fr}".format(fr=Fore.RESET,
                                                                                            y=Fore.YELLOW,
                                                                                            b=Fore.BLUE,
                                                                                            g=Fore.GREEN,
                                                                                            msg=result[0]["notif"],
                                                                                            saldo=result[0]["wallet"]))
            except:
                print(result)
    except KeyboardInterrupt:
        print("Program Was Stopped....")

def do_startchallange():
    print("{y}{b}press CTRL+C for stop this job's{br}{fr}".format(
        y=Back.YELLOW, br=Back.RESET, b=Fore.BLACK, fr=Fore.RESET))
    print("Bot Is Starting!!!......")
    for a in range(1,12):
            result = botmtc.solvedChallange(a)
            print(result)
            # if result["notif"] != "Reward failed!":
            #     print("{b}[+]{fr}{g}{msg}{fr} >> Current Ballance {y}{saldo} MTC{fr}".format(fr=Fore.RESET,
            #                                                                                 y=Fore.YELLOW,
            #                                                                                 b=Fore.BLUE,
            #                                                                                 g=Fore.GREEN,
            #                                                                                 msg=result[0]["notif"],
            #                                                                                 saldo=result[0]["wallet"]))
            # else:
            #     break


if __name__ == "__main__":
    balance, starttask, startchallange = command(sys.argv[1:])
    if balance:
        do_balance()
    elif starttask:
        do_startTask()
    elif startchallange:
        do_startchallange()
