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

# # MID-2017 POPULATION ESTIMATES: Net migration by type, age bands and gender

# +
from gssutils import *

if is_interactive():
    scraper = Scraper('https://www.nisra.gov.uk/publications/'\
                      '2017-mid-year-population-estimates-northern-ireland-new-format-tables')
    dist = scraper.distribution(
        title='Northern Ireland - Net migration by sex and age bands (2001-2017)',
        mediaType=Excel
    )
    flat = dist.as_pandas(sheet_name='Flat')

flat
# -

tidy = pd.DataFrame()
tidy["Value"] = flat["NETMIG"]
tidy['Mid Year'] = flat["year"]
tidy['Age'] = flat["age"]
tidy['Area'] = flat["area_code"]
tidy['Sex'] = flat["gender"]
tidy['Population Change Component'] = flat["type"]
tidy['Measure Type'] = "Count"
tidy['Unit'] = "People"
tidy

tidy['Mid Year'].unique()

tidy['Mid Year'] = tidy['Mid Year'].map(lambda x: str(x)[0:4] + '-06-30T00:00:00/P1Y')

tidy['Mid Year'].unique()

tidy.dtypes

tidy['Age'] = tidy['Age'].map(lambda cell: cell.replace('65+', '65-plus'))

tidy['Age'] = 'nisra5/' + tidy['Age'].map(str)

tidy['Sex'] = tidy['Sex'].map(
    lambda x: {
        'All persons' : 'T', 
        'Females' : 'F',
        'Males': 'M' 
    }.get(x, x))

tidy['Population Change Component'] = tidy['Population Change Component'].str.lstrip('123.')

tidy = tidy[['Mid Year','Area','Age','Sex','Population Change Component','Measure Type','Value','Unit']]

tidy.head()

tidy.tail()

tidy['Value'] = tidy['Value'].astype(int)

tidy['Population Change Component'] = tidy['Population Change Component'].map(lambda cell: cell.replace(' Rest of World Net','Rest of world Net'))

tidy.count()

tidy.dtypes
