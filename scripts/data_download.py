import logging
import os
from urllib.request import urlretrieve
import ssl
import requests
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

ssl._create_default_https_context = ssl._create_unverified_context
out_dir = "../data/raw"

headers = {
    'authority': 'api.data.abs.gov.au',
    'accept': 'application/vnd.sdmx.data+csv;urn=true;file=true;labels=both',
    'accept-language': 'en',
    'origin': 'https://explore.data.abs.gov.au',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}


def download_zone():
    '''Download zones lookup data'''

    if not os.path.exists(f"{out_dir}/abs_data/zone_data"):
        os.mkdir(f"{out_dir}/abs_data/zone_data")

    logging.info("Beginning zone download")

    urlretrieve(
        "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA2_2021_AUST_SHP_GDA2020.zip", f"{out_dir}/abs_data/zone_data/zones.zip")

    logging.info("Finished zone download")

    os.system(
        "unzip ../data/raw/abs_data/zone_data/zones.zip -d ../data/raw/abs_data/zone_data")

    return


def download_pop():

    logging.info("Beginning population download")

    params = {
        'startPeriod': '2011',
        'dimensionAtObservation': 'AllDimensions',
    }

    response = requests.get(
        'https://api.data.abs.gov.au/data/ABS,ABS_ANNUAL_ERP_ASGS2021,1.2.0/.SA2..', params=params, headers=headers)

    with open('../data/raw/abs_data/pop_data.csv', 'w') as f:
        f.write(response.text)

    logging.info("Finished population download")
    return


def download_median_income():
    """Download census income data"""
    logging.info("Beginning income download")

    params = {
        'dimensionAtObservation': 'AllDimensions',
    }

    response = requests.get(
        'https://api.data.abs.gov.au/data/ABS,C21_G02_SA2,1.0.0/2..SA2.', params=params, headers=headers)
    with open('../data/raw/abs_data/2021_income.csv', 'w') as f:
        f.write(response.text)

    params = {
        'startPeriod': '2011',
        'endPeriod': '2020',
        'dimensionAtObservation': 'AllDimensions',
    }

    response = requests.get(
        'https://api.data.abs.gov.au/data/ABS,ABS_REGIONAL_ASGS2016,1.2.0/INCOME_2.SA2..A', params=params, headers=headers)
    with open('../data/raw/abs_data/2011_2019_income.csv', 'w') as f:
        f.write(response.text)

    logging.info("Finished population download")


def main():
    download_zone()
    download_pop()
    download_median_income()
    return


if __name__ == "__main__":
    main()
