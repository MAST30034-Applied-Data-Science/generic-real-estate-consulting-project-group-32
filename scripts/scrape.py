import re
from bs4 import BeautifulSoup
import requests
from json import dump
from datetime import datetime
from selenium.common.exceptions import ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


BASE_URL = "https://www.domain.com.au"

BASE_URL_SUB_PROFILE = "https://www.domain.com.au/suburb-profile/"

SAVE_DIR = "../data/raw/"

PAGES_TO_SCRAPE = 50

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"
}


def property_scraper():
    property_urls = []
    for page_num in range(PAGES_TO_SCRAPE):

        # print(f"Requesting page {page_num + 1}")

        page_url = f"{BASE_URL}/rent/?state=vic&page={page_num + 1}"
        content = BeautifulSoup(
            requests.get(page_url, headers=HEADERS).text, "html.parser"
        )

        # print(f"Retrieved page {page_num + 1}")

        # find all property links on currect page
        links = content.find("ul", {"data-testid": "results"})
        if links:
            links = links.findAll("a", href=re.compile(f"{BASE_URL}/*"))
            if links:
                # add specific links to properties to list
                for link in links:
                    if "address" in link["class"]:
                        property_urls.append(link["href"])

    data = []

    for property_url in property_urls:

        print(property_url)

        price = None

        address = None

        num_beds = None
        num_bath = None
        num_car = None

        property_type = None

        agent = None

        bond = None
        internal_area = None
        land_area = None

        domain_says = None

        neighbourhood_under_20 = None
        neighbourhood_20_to_39 = None
        neighbourhood_40_to_59 = None
        neighbourhood_above_60 = None

        neighbourhood_long_term_residents = None

        neighbourhood_owners = None
        neighbourhood_renter = None
        neighbourhood_family = None
        neighbourhood_single = None

        performance_median_price = None
        performance_auction_clearance = None
        performance_sold_this_year = None
        performance_avg_days_on_market = None

        demographic_population = None
        demographic_average_age = None

        demographic_owner = None
        demographic_renter = None
        demographic_family = None
        demographic_single = None

        latitude = None
        longitude = None

        content = BeautifulSoup(
            requests.get(property_url, headers=HEADERS).text, "html.parser"
        )

        content_price = content.find(
            "div", {"data-testid": "listing-details__summary-title"}
        )

        content_address = content.find("h1", {"class": "css-164r41r"})

        content_features = content.find("div", {"data-testid": "property-features"})
        if content_features:
            content_features = content_features.findAll(
                "span", {"data-testid": "property-features-text-container"}
            )

        content_property_type = content.find(
            "div", {"data-testid": "listing-summary-property-type"}
        )

        content_agent = content.find(
            "a", {"data-testid": "listing-details__agent-details-agent-company-name"}
        )

        content_summary = content.find("div", {"data-testid": "strip-content-list"})
        if content_summary:
            content_summary = content_summary.findAll("li")

        content_domain_says = content.find(
            "p", {"data-testid": "listing-details__domain-says-text"}
        )

        content_neighbourhood_insights = content.find(
            "section", {"data-testid": "neighbourhood-insights"}
        )
        if content_neighbourhood_insights:
            content_age = content.findAll(
                "tr", {"data-testid": "neighbourhood-insights__age-brackets-row"}
            )
            content_long_term_residents = content.find(
                "div", {"data-testid": "single-value-doughnut-graph"}
            )
            content_type = content.findAll("div", {"class": "css-14hea9r"})
        else:
            content_age = content_long_term_residents = content_type = None

        content_stats = content.find(
            "div", {"data-testid": "listing-details__suburb-insights"}
        )
        if content_stats:
            content_values = content_stats.findAll("div", {"class": "css-35ezg3"})

            content_occupancy = content_stats.find(
                "div", {"data-testid": "suburb-insights__occupancy"}
            )
            content_household = content_stats.find(
                "div", {"data-testid": "suburb-insights__household"}
            )
        else:
            content_values = content_occupancy = content_household = None

        content_coordinates = content.find(
            "a", {"target": "_blank", "rel": "noopener noreferer"}
        )

        if content_price:
            price = content_price.getText()

        if content_address:
            address = content_address.getText()

        if len(content_features) >= 1:
            num_beds = content_features[0].getText()

        if len(content_features) >= 2:
            num_bath = content_features[1].getText()

        if len(content_features) >= 3:
            num_car = content_features[2].getText()

        if content_property_type:
            property_type = content_property_type.getText()

        if content_agent:
            agent = content_agent.getText()

        if content_summary:
            for entry in content_summary:
                bond_found = re.findall(r"([bB]ond \$[0-9,\.]+)", entry.getText())
                internal_area_found = re.findall(
                    r"([iI]nternal area .+)", entry.getText()
                )
                land_area_found = re.findall(r"([lL]and area .+)", entry.getText())

                if bond_found:
                    bond = bond_found[0]

                if internal_area_found:
                    internal_area = internal_area_found[0]

                if land_area_found:
                    land_area = land_area_found[0]

        if content_domain_says:
            domain_says = content_domain_says.getText()

        if content_age:
            content_under_20 = content_age[0].find("div", {"data-testid": "bar-value"})
            content_20_to_39 = content_age[1].find("div", {"data-testid": "bar-value"})
            content_40_to_59 = content_age[2].find("div", {"data-testid": "bar-value"})
            content_above_60 = content_age[3].find("div", {"data-testid": "bar-value"})

            neighbourhood_under_20 = content_under_20.getText()
            neighbourhood_20_to_39 = content_20_to_39.getText()
            neighbourhood_40_to_59 = content_40_to_59.getText()
            neighbourhood_above_60 = content_above_60.getText()

        if content_long_term_residents:
            neighbourhood_long_term_residents = content_long_term_residents.getText()

        if content_type:
            neighbourhood_owners = (
                content_type[0].find("span", {"data-testid": "left-value"}).getText()
            )
            neighbourhood_renter = (
                content_type[0].find("span", {"data-testid": "right-value"}).getText()
            )
            neighbourhood_family = (
                content_type[1].find("span", {"data-testid": "left-value"}).getText()
            )
            neighbourhood_single = (
                content_type[1].find("span", {"data-testid": "right-value"}).getText()
            )

        if content_values:
            performance_median_price = content_values[0].getText()
            performance_auction_clearance = content_values[1].getText()
            performance_sold_this_year = content_values[2].getText()
            performance_avg_days_on_market = content_values[3].getText()

            demographic_population = content_values[4].getText()
            demographic_average_age = content_values[5].getText()

        if content_occupancy:
            demographic_owner = content_occupancy.find(
                "span", {"data-testid": "left-value"}
            ).getText()
            demographic_renter = content_occupancy.find(
                "span", {"data-testid": "right-value"}
            ).getText()

        if content_occupancy:
            demographic_owner = content_occupancy.find(
                "span", {"data-testid": "left-value"}
            ).getText()
            demographic_renter = content_occupancy.find(
                "span", {"data-testid": "right-value"}
            ).getText()

        if content_household:
            demographic_family = content_household.find(
                "span", {"data-testid": "left-value"}
            ).getText()
            demographic_single = content_household.find(
                "span", {"data-testid": "right-value"}
            ).getText()

        if content_coordinates:
            coordinates = re.findall(
                r"destination=([-\s,\d\.]+)", content_coordinates.attrs["href"]
            )
            if coordinates:
                coordinates = coordinates[0].split(",")
                latitude = coordinates[0]
                longitude = coordinates[1]

        data.append(
            {
                "url": property_url,
                "price": price,
                "address": address,
                "num_beds": num_beds,
                "num_bath": num_bath,
                "num_car": num_car,
                "property_type": property_type,
                "agent": agent,
                "bond": bond,
                "internal_area": internal_area,
                "land_area": land_area,
                "domain_says": domain_says,
                "neighbourhood_under_20": neighbourhood_under_20,
                "neighbourhood_20_to_39": neighbourhood_20_to_39,
                "neighbourhood_40_to_59": neighbourhood_40_to_59,
                "neighbourhood_above_60": neighbourhood_above_60,
                "neighbourhood_long_term_residents": neighbourhood_long_term_residents,
                "neighbourhood_owners": neighbourhood_owners,
                "neighbourhood_renter": neighbourhood_renter,
                "neighbourhood_family": neighbourhood_family,
                "neighbourhood_single": neighbourhood_single,
                "performance_median_price": performance_median_price,
                "performance_auction_clearance": performance_auction_clearance,
                "performance_sold_this_year": performance_sold_this_year,
                "performance_avg_days_on_market": performance_avg_days_on_market,
                "demographic_population": demographic_population,
                "demographic_average_age": demographic_average_age,
                "demographic_owner": demographic_owner,
                "demographic_renter": demographic_renter,
                "demographic_family": demographic_family,
                "demographic_single": demographic_single,
                "latitude": latitude,
                "longitude": longitude,
            }
        )

    print(f"{len(data)} properties scraped")

    # save all data scraped with time code
    time_utc = (
        str(datetime.utcnow()).replace(" ", "_").replace(":", "-").replace(".", "-")
    )
    with open(f"{SAVE_DIR}/scrape_{time_utc}.json", "w") as file:
        dump(data, file)

    print(f"data saved")

    return


def driver_setup():
    """Set up driver configs"""
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install(), chrome_options=options
    )
    return driver


def df_setup():
    """Setup dataframe"""
    df = pd.DataFrame(
        columns=[
            "suburb",
            "postcode",
            "p_type",
            "median_sell",
            "avg_days_on_market",
            "clearance",
            "n_sold",
            "h_range",
            "l_range",
            "median_rent",
            "2022_median",
            "2022_growth",
            "2022_n_sold",
            "2021_median",
            "2021_growth",
            "2021_n_sold",
            "2020_median",
            "2020_growth",
            "2020_n_sold",
            "2019_median",
            "2019_growth",
            "2019_n_sold",
            "2018_median",
            "2018_growth",
            "2018_n_sold",
        ]
    )
    return df


def url_finder(row):
    suburb = row["locality"].lower().replace(r" ", "-")
    postcode = row["postcode"]

    url = f"{BASE_URL_SUB_PROFILE}{suburb}-vic-{postcode}"

    return url, suburb


def interactive_data(soup, index):
    """Find new data from interactive element"""
    all = []
    for tr in soup.find_all("tr"):
        cols = [td.text for td in tr.find_all("td")]
        all.append(cols)
    data = all[index][0]
    data = data.replace("\xa0", " ")
    return data


def yearly_history_parser(regex):
    try:
        median = regex.group(1)
    except AttributeError as e:
        median = None

    try:
        growth = regex.group(2)
    except AttributeError as e:
        growth = None

    try:
        n_sales = regex.group(3)
    except AttributeError as e:
        n_sales = None

    return [median, growth, n_sales]


def interactive_regex(data, rows, index):
    """Parse data from interactive element"""
    try:
        h_end = re.search(r"high end: \$?([\d.?]*k?m?)", data, re.IGNORECASE).group(1)
        low_end = re.search(
            r"entry level: \$?([\d.?]*k?m?)", data, re.IGNORECASE
        ).group(1)
        rent_median = re.search(
            r"rental median price: \$?([\d.?]*k?m?)", data, re.IGNORECASE
        ).group(1)

        hist_2022 = re.search(
            r"2022(\$\d.*[m|k]{1}|N/A)(-?\d.*%{1}|-)(\d*)2021", data, re.IGNORECASE
        )
        hist_2022 = yearly_history_parser(hist_2022)

        hist_2021 = re.search(
            r"2021(\$\d.*[m|k]{1}|N/A)(-?\d.*%{1}|-)(\d*)2020", data, re.IGNORECASE
        )
        hist_2021 = yearly_history_parser(hist_2021)

        hist_2020 = re.search(
            r"2020(\$\d.*[m|k]{1}|N/A)(-?\d.*%{1}|-)(\d*)2019", data, re.IGNORECASE
        )
        hist_2020 = yearly_history_parser(hist_2020)

        hist_2019 = re.search(
            r"2019(\$\d.*[m|k]{1}|N/A)(-?\d.*%{1}|-)(\d*)2018", data, re.IGNORECASE
        )
        hist_2019 = yearly_history_parser(hist_2019)

        hist_2018 = re.search(
            r"2018(\$\d.*[m|k]{1}|N/A)(-?\d.*%{1}|-)(\d*)", data, re.IGNORECASE
        )
        hist_2018 = yearly_history_parser(hist_2018)

        rows[index - 1].extend(
            [
                h_end,
                low_end,
                rent_median,
                *hist_2022,
                *hist_2021,
                *hist_2020,
                *hist_2019,
                *hist_2018,
            ]
        )

    except AttributeError as e:
        return rows

    return rows


def ingester(rows, df, suburb, postcode):
    """Insert data to dataframe"""
    for i in rows:
        if i:
            i.insert(0, f"{i.pop(0)}_{i.pop(0).lower()}")
            del i[5]
            i.insert(0, suburb)
            i.insert(1, postcode)
            # print(i)

            df = df.append(pd.Series(i, index=df.columns[: len(i)]), ignore_index=True)
    return df


def history_scraper(driver, url):
    """Scrape historical data from Domain"""
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, features='lxml')
    rows = []
    try:
        table = soup.find(lambda tag: tag.name == "table")
        n_rows = len(
            table.findAll(
                lambda tag: tag.name == "tr" and tag.findParent("table") == table
            )
        )
    except AttributeError as e:
        return rows

    # Static Rows
    for tr in soup.find_all("tr"):
        cols = [td.text for td in tr.find_all("td")]
        rows.append(cols)

    # Interactive Rows
    for i in range(2, n_rows + 1):

        driver.find_element(
            by=By.CSS_SELECTOR, value=f".css-168e8ow:nth-child({i}) .css-1vofcfi svg"
        ).click()

        soup2 = BeautifulSoup(driver.page_source, features='lxml')

        new_data = interactive_data(soup2, i)
        rows = interactive_regex(new_data, rows, i)

    return rows


def main():
    property_scraper()

    df = df_setup()
    driver = driver_setup()

    full_suburbs = pd.read_csv(
        f"{SAVE_DIR}postcode.csv", usecols=["postcode", "locality", "state"]
    )
    full_suburbs = full_suburbs[full_suburbs["state"] == "VIC"]

    df = pd.read_csv("../data/curated/historical_sales.csv")
    for index, row in full_suburbs.iterrows():
        if index > 6648:
            url, suburb = url_finder(row)
            print(url)
            try:
                table_rows = history_scraper(driver, url)
            except ElementClickInterceptedException as e:
                continue
            df = ingester(table_rows, df, suburb, row["postcode"])
            time.sleep(1)
            df.to_csv("../data/curated/historical_sales.csv")


if __name__ == "__main__":
    main()
