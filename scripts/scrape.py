import re
from bs4 import BeautifulSoup
import requests
from json import dump
from datetime import datetime


BASE_URL = "https://www.domain.com.au"

SAVE_DIR = "../data/raw/"

PAGES_TO_SCRAPE = 50

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
property_urls = []
for page_num in range(PAGES_TO_SCRAPE):

    #print(f"Requesting page {page_num + 1}")

    page_url = f"{BASE_URL}/rent/?state=vic&page={page_num + 1}"
    content = BeautifulSoup(requests.get(page_url, headers=HEADERS).text, "html.parser")

    #print(f"Retrieved page {page_num + 1}")

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

    content = BeautifulSoup(requests.get(property_url, headers=HEADERS).text, "html.parser")

    content_price = content.find("div", {"data-testid": "listing-details__summary-title"})

    content_address = content.find("h1", {"class": "css-164r41r"})

    content_features = content.find("div", {"data-testid": "property-features"})
    if content_features:
        content_features = content_features.findAll("span", {"data-testid": "property-features-text-container"})

    content_property_type = content.find("div", {"data-testid": "listing-summary-property-type"})

    content_agent = content.find("a", {"data-testid": "listing-details__agent-details-agent-company-name"})

    content_summary = content.find("div", {"data-testid": "strip-content-list"})
    if content_summary:
        content_summary = content_summary.findAll("li")

    content_domain_says = content.find("p", {"data-testid": "listing-details__domain-says-text"})

    content_neighbourhood_insights = content.find("section", {"data-testid": "neighbourhood-insights"})
    if content_neighbourhood_insights:
        content_age = content.findAll("tr", {"data-testid": "neighbourhood-insights__age-brackets-row"})
        content_long_term_residents = content.find("div", {"data-testid": "single-value-doughnut-graph"})
        content_type = content.findAll("div", {"class": "css-14hea9r"})
    else:
        content_age = content_long_term_residents = content_type = None

    content_stats = content.find("div", {"data-testid": "listing-details__suburb-insights"})
    if content_stats:
        content_values = content_stats.findAll("div", {"class": "css-35ezg3"})

        content_occupancy = content_stats.find("div", {"data-testid": "suburb-insights__occupancy"})
        content_household = content_stats.find("div", {"data-testid": "suburb-insights__household"})
    else:
        content_values = content_occupancy = content_household = None

    content_coordinates = content.find("a", {"target": "_blank", 'rel': "noopener noreferer"})

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
            bond_found = re.findall(r"([bB]ond \$[0-9,\.]+)",  entry.getText())
            internal_area_found = re.findall(r"([iI]nternal area .+)",  entry.getText())
            land_area_found = re.findall(r"([lL]and area .+)",  entry.getText())

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
        neighbourhood_owners = content_type[0].find("span", {"data-testid": "left-value"}).getText()
        neighbourhood_renter = content_type[0].find("span", {"data-testid": "right-value"}).getText()
        neighbourhood_family = content_type[1].find("span", {"data-testid": "left-value"}).getText()
        neighbourhood_single = content_type[1].find("span", {"data-testid": "right-value"}).getText()

    if content_values:
        performance_median_price = content_values[0].getText()
        performance_auction_clearance = content_values[1].getText()
        performance_sold_this_year = content_values[2].getText()
        performance_avg_days_on_market = content_values[3].getText()

        demographic_population = content_values[4].getText()
        demographic_average_age = content_values[5].getText()

    if content_occupancy:
        demographic_owner = content_occupancy.find("span", {"data-testid": "left-value"}).getText()
        demographic_renter = content_occupancy.find("span", {"data-testid": "right-value"}).getText()

    if content_occupancy:
        demographic_owner = content_occupancy.find("span", {"data-testid": "left-value"}).getText()
        demographic_renter = content_occupancy.find("span", {"data-testid": "right-value"}).getText()

    if content_household:
        demographic_family = content_household.find("span", {"data-testid": "left-value"}).getText()
        demographic_single = content_household.find("span", {"data-testid": "right-value"}).getText()

    if content_coordinates:
        coordinates = re.findall(r"destination=([-\s,\d\.]+)", content_coordinates.attrs["href"])
        if coordinates:
            coordinates = coordinates[0].split(",")
            latitude = coordinates[0]
            longitude = coordinates[1]

    data.append({"url": property_url,
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
                 "longitude": longitude})

print(f"{len(data)} properties scraped")

# save all data scraped with time code
time_utc = str(datetime.utcnow()).replace(" ", "_").replace(":", "-").replace(".", "-")
with open(f"{SAVE_DIR}/scrape_{time_utc}.json", "w") as file:
    dump(data, file)

print(f"data saved")
