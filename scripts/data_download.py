import logging
import os
from urllib.request import urlretrieve
import ssl
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

ssl._create_default_https_context = ssl._create_unverified_context
out_dir = "../data/raw"

def download_zone():
    '''Download zones lookup data'''

    if not os.path.exists(f"{out_dir}/abs_data/zone_data"):
        os.mkdir(f"{out_dir}/abs_data/zone_data")

    logging.info("Beginning zone download")

    urlretrieve(
        "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA2_2021_AUST_SHP_GDA2020.zip", f"{out_dir}/abs_data/zone_data/zones.zip")

    logging.info("Finished zone download")

    os.system("unzip ../data/raw/abs_data/zone_data/zones.zip -d ../data/raw/abs_data/zone_data")

    return

def main():
    download_zone()
    return

if __name__ == "__main__":
    main()