# Generic Real Estate Consulting Project

## Steps
#### Only datasets not easily reproducible (time sensitive data or time to compute) are included on the git

Please install packages as per `requirements.txt` before running the following steps.

Please note that `geoplot` may have issues installing on Python3.9+

For an overview of the project go to: `notebooks\summary.ipynb`

#### Please note that scraping and api require a significant amount of time and/or API credentials. We would strongly recommend that you SKIP those 2 files.
#### The data outputted from those 2 files are:
#### - `data/raw/scraped_proeperties.csv`
#### - `data/curated/api_data.csv`

#### These files are saved in GitHub for your convenience

## Team
- Dylan Beaumont, 1052845
- Matthew Rush, 1080100
- Nguyen Duc Le, 1127268
- Jesse Cooper, 1091024
- Yanbo Feng, 1174059

## Data Reference
### SA2 Zones, Population Data, Median Income, and Population Projection
https://api.data.abs.gov.au with various resources and parameters

### School Locations
https://www.education.vic.gov.au/Documents/about/research/datavic/dv309_schoollocations2021.csv

### PTV Stops Location
Requested at https://datashare.maps.vic.gov.au.
Note that data will be emailed to you.

### Listed Properties
https://www.domain.com.au/rent/ {parameters}

### Suburbs Historical Sales
https://www.domain.com.au/suburb-profile/ {suburb_parameters}

### Parks and Shopping Centres
Courtesy of OpenStreetMap
https://www.openstreetmap.org/copyright
