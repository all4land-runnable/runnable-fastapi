import os

import requests

from config.external.parser import parse_xml

OPEN_DATA_POTAL_ACCESS_KEY = os.getenv('OPEN_DATA_POTAL_ACCESS_KEY')

def get_hospitals(lon:float, lat:float, SAMPLE_RADIUS = 500):
    headers = {"Content-Type": "application/json"}
    url="http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
    data={
        "ServiceKey": OPEN_DATA_POTAL_ACCESS_KEY,
        "xPos": lon,
        "yPos": lat,
        "radius": SAMPLE_RADIUS
    }
    response = requests.get(url=url, params=data, headers=headers)
    return parse_xml(response, title="병원 위치 조회 실패")