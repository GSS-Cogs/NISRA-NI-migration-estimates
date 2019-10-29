# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # MID-2017 POPULATION ESTIMATES: Components of population change

# +
from gssutils import *

if is_interactive():
    scraper = Scraper('https://www.nisra.gov.uk/publications/'\
                      '2017-mid-year-population-estimates-northern-ireland-new-format-tables')
    dist = scraper.distribution(
        title='All areas - Components of population change',
        mediaType=Excel
    )
    flat = dist.as_pandas(sheet_name='Flat')

flat
# -

tidy = pd.DataFrame()
tidy["Value"] = flat["MYE"]
tidy['Mid Year'] = flat["year"]
tidy['Area'] = flat["area_code"]
tidy['Population Change Component'] = flat["category"]
tidy['Measure Type'] = "Count"
tidy['Unit'] = "People"
tidy['Age'] = 'all'
tidy['Sex'] = 'T'
tidy

tidy['Mid Year'].unique()

tidy['Mid Year'] = tidy['Mid Year'].map(lambda x: str(x)[0:4] + '-06-30T00:00:00/P1Y')

tidy = tidy[['Mid Year','Area','Age','Sex','Population Change Component','Measure Type','Value','Unit']]

tidy.head()

tidy['Value'] = tidy['Value'].astype(int)

tidy.count()

tidy.dtypes
