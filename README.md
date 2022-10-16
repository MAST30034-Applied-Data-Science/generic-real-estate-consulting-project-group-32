# Generic Real Estate Consulting Project

- only datasets not easily reproducible (time sensitive data or time to compute) are included on the git

Run the file in numbered order:
1. `scripts\1_data_download.py`
2. `notebook\2_scrape.ipynb`
3. `notebook\3_api.ipynb`
4. `notebook\3_pre_processing.ipynb`
5. `notebook\5_question_1.ipynb`
6. `notebook\6_question_2.ipynb`
7. `notebook\7_question_3.ipynb`

Or alternatively run the notebook: `summary.ipynb`

#### Please note that files 3 and 4 require a significant amount of time and/or API credentials. We would strongly recommend that you SKIP those 2 files.
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

