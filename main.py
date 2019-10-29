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

# ## Northern Ireland Statistics and Research Agency
#
# [2017 Mid Year Population Estimates for Northern Ireland (NEW FORMAT TABLES)
# ](https://www.nisra.gov.uk/publications/2017-mid-year-population-estimates-northern-ireland-new-format-tables)

from gssutils import *
scraper = Scraper('https://www.nisra.gov.uk/publications/'\
                  '2017-mid-year-population-estimates-northern-ireland-new-format-tables')
scraper

# Total observations must be 19580 (14060 + 1008 + 4368 + 144) from four files but final output observations show 16620, 
# main.ipynb file $processors concatinating 
# NISRA Migration MEY17CoC.ipynb and NISRA Migration MYE17 NETMIG AGE BANDS Gender.ipynb but not 
#     other two files, 
# And concat 
#     MID-2017 POPULATION ESTIMATES: Net migration by type, age bands and gender and 
#     MID-2017 POPULATION ESTIMATES: Migration flows and net migration
#     source files data directly not from ipynb data??
# But CSVlint error should not be `duplicates`! because there are no duplicates in out put??

# Disabled `Northern Ireland - Migration flows by type` due to duplicates

# +
processors = [
    ('All areas - Components of population change', 'NISRA Migration MEY17CoC.ipynb'),
    ('Northern Ireland - Net migration by sex and age bands', 'NISRA Migration MYE17 NETMIG AGE BANDS Gender.ipynb'),
    ('Northern Ireland - Net migration by sex and single year of age', 'NISRA Migration MYE17 NETMIG AGE.ipynb')
#     ('Northern Ireland - Migration flows by type', 'NISRA Migration MYE17 NETMIG FLOW.ipynb')
]

tidy_list = []
metadata_tabs = []
for title, processor in processors:
    book = scraper.distribution(title=lambda x: x.startswith(title)).as_pandas(sheet_name=None, header=None)
    flat = book['Flat']
    flat = flat.rename(columns=flat.iloc[0]).drop(flat.index[0])
    %run "$processor"
    tidy_list.append(tidy)
    metadata_tabs.append(book['Metadata'])
all_tidy = pd.concat(tidy_list)
all_tidy
# -

# Metadata is provided in the 'Metadata' tabs.
#
# We're merging the data from these spreadsheets into the same cube, by making implicit dimensions explicit. The metadata should be the same for each, but it differs slightly: the description for the first table is a bit less verbose; the reference area for the first is a specialization of the rest.

md = metadata_tabs[1]
md.drop(md.index[0], inplace=True)
md.drop(columns=[0], inplace=True)
md

# +
name2prop = {
    'National Statistics Theme:': 'theme',
    'Data Subset:': 'subtheme',
    'Dataset Title:': 'title',
    'Coverage:': 'spatial',
    'Source:': 'publisher',
    'Contact:': 'contactPoint',
    'National Statistics Data?': 'nationalStatistics',
    'Responsible Statistician:': 'contactPoint'
}

from numpy import isnan

section = 'metadata'
current_prop = None
add_section = False
description = []
for i, row in md.iterrows():
    if section == 'metadata':
        if row[1] in name2prop:
            current_prop = name2prop[row[1].strip()]
        elif row[1] == 'Description of Data':
            section = 'description'
            continue
        if current_prop == 'publisher':
            assert row[2].strip() == 'NISRA'
            scraper.dataset.publisher = metadata.GOV['northern-ireland-statistics-and-research-agency']
        elif current_prop == 'spatial':
            assert row[2].strip() == 'Northern Ireland'
            scraper.dataset.spatial = 'http://statistics.data.gov.uk/id/statistical-geography/N92000002'
        elif current_prop == 'contactPoint':
            pass
        elif current_prop == 'theme':
            scraper.dataset.theme = metadata.THEME[pathify(row[2].strip())]
        elif current_prop is not None:
            setattr(scraper.dataset, current_prop, row[2].strip())
    else:
        if type(row[1]) != str:
            description.append('')
            add_section = True
        else:
            if add_section:
                description.append('## ' + row[1].strip())
                description.append('')
                add_section = False
            else:
                description.append(row[1].strip())
            
scraper.dataset.description = '\n'.join(description)
scraper
# -

all_tidy.count()

all_tidy.rename(columns={'Area': 'Area of Destination or Origin'}, inplace=True)
all_tidy

all_tidy['Population Change Component'] = all_tidy['Population Change Component'].str.strip(' ').apply(pathify)

# +
from pathlib import Path
out = Path('out')
out.mkdir(exist_ok=True)
all_tidy.to_csv(out / 'observations.csv', index = False)

scraper.dataset.family = 'migration'
scraper.dataset.license = 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'

with open(out / 'dataset.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

scraper.dataset

csvw = CSVWMetadata('https://gss-cogs.github.io/ref_migration/')
csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')


