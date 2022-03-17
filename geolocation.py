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
        flag = ":flag_" +  self.georesult["country_code"].lower() + ":"
        return f"Country: {self.georesult['country_name']} {flag} | state: {self.georesult['state']}" + \
               f"| city: {self.georesult['city']} | IPv4: {self.georesult['IPv4']}"

    def geolocation(self):
        """gets the geolocation of the server"""
        # URL to send the request to
        request_url = 'https://geolocation-db.com/jsonp/' + self.ipaddress
        # Send request and decode the result
        response = requests.get(request_url)
        self.georesult = response.content.decode()
        # Clean the returned string so it just contains the dictionary data for the IP address
        self.georesult = self.georesult.split("(")[1].strip(")")
        # Convert this data into a dictionary
        self.georesult  = json.loads(self.georesult)
