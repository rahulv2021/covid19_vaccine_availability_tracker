import requests
import time
from decorators import retry


def get_districts_by_state_id(scheme, hostname, headers, state_id):
    time.sleep(2)
    api = "api/v2/admin/location/districts/{state_id}".format(
        state_id=state_id)
    url = build_url(scheme, hostname, api)
    districts = do_get_request(url, headers).json()["districts"]
    district_ids = []
    for district in districts:
        district_ids.append(district["district_id"])
    return district_ids


def get_vaccine_centers_by_district_and_date(scheme, hostname, headers, district_id, date):
    time.sleep(3.5)
    api = "api/v2/appointment/sessions/calendarByDistrict?district_id={district_id}&date={date}".format(
        district_id=district_id, date=date)
    url = build_url(scheme, hostname, api)
    print url
    centers = do_get_request(url, headers).json()["centers"]
    return centers


def build_url(scheme, hostname, api):
    return "{scheme}://{hostname}/{api}".format(scheme=scheme,
                                                hostname=hostname,
                                                api=api)


@retry(Exception, max_retries=10, delay=2, backoff=2)
def do_get_request(url, headers, timeout=30):
    ret = requests.get(url=url, timeout=timeout, headers=headers)
    ret.raise_for_status()
    print ret
    return ret
