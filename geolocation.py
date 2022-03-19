"""module imports"""
import json

import requests


class Serverlocation():
    """geolocation of the selected server"""
    def __init__(self, ipadd) -> None:
        self.ipaddress = ipadd
        self.georesult = {}

    def main(self):
        """main"""
        self.geolocation()
        if str(self.georesult['status']) == "success":
            flag = ":flag_" +  self.georesult["countryCode"].lower() + ":"
            return f"Country: {self.georesult['country']} {flag} | state: {self.georesult['regionName']}" + \
                f"| city: {self.georesult['city']} | IPv4: {self.georesult['query']} \n" + \
                f"ISP: {self.georesult['isp']} | timezone: {self.georesult['timezone']}"
        elif str(self.georesult['status']) == "fail":
            return f"failed to get geolocation of {self.georesult['query']}"


    def geolocation(self):
        """gets the geolocation of the server"""

        request_url = 'http://ip-api.com/json/' + self.ipaddress
        response = requests.get(request_url).json()

        if response['status'] == 'fail' and len(self.ipaddress.split(":")) > 1:
            request_url = 'http://ip-api.com/json/' + self.ipaddress.split(":")[0]
            response = requests.get(request_url).json()

        self.georesult = response