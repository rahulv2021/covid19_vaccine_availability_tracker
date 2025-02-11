tokens = [
    token_mobile,
]

hostname = "cdn-api.co-vin.in"

scheme = "https"

headers = {
    'authority': 'cdn-api.co-vin.in',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': 'application/json, text/plain, */*',
    'authorization': 'BEARER {token}',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'origin': 'https://selfregistration.cowin.gov.in',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://selfregistration.cowin.gov.in/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}


states = {
    'delhi': {
        'id': 9,
        'district_ids': []
    },
    'haryana': {
        'id': 12,
        'district_ids': [188]
    }
    # 'karnal': {
    #     'id': 12,
    #     'district_ids': [203]
    # }
}

exceptions = {
    'karnal': {
        'covaxin': {
            18: {
                'dose_1': True,
                'dose_2': False
            },
            45: {
                'dose_1': False,
                'dose_2': True
            }
        }
    }
}

week_range = 2

age_limits = [18, 45]

vaccines = {
    "covaxin": {
        18: {
            "dose_1": True,
            "dose_2": True,
        },
        45: {
            "dose_1": True,
            "dose_2": True,
        },
    },
    "covishield": {
        18: {
            "dose_1": True,
            "dose_2": True,
        },
        45: {
            "dose_1": True,
            "dose_2": True,
        },
    },
    "sputnik": {
        18: {
            "dose_1": True,
            "dose_2": False,
        },
        45: {
            "dose_1": True,
            "dose_2": False,
        },
    },
}
