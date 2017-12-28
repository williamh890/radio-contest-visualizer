import requests
import json

if __name__ == "__main__":
    counties_url = 'http://eric.clst.org/wupl/Stuff/gz_2010_us_outline_500k.json'
    r = requests.get(counties_url)
    data = json.loads(r.text)

