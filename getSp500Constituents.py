from datapackage import Package
import pandas as pd

package = Package('https://datahub.io/core/s-and-p-500-companies-financials/datapackage.json')

df = pd.DataFrame()

# print list of all resources:
print(package.resource_names)

# print processed tabular data (if exists any)
for resource in package.resources:
    if resource.descriptor['datahub']['type'] == 'derived/csv' and \
    resource.descriptor['name'] == 'constituents-financials_csv':
        data_sp500 = resource.read( keyed=True)
        print( type(data_sp500) )
        print( data_sp500[:10] )
        df = pd.DataFrame(data=data_sp500)
        print(df.head())
        break

if len(df['Symbol'] ) > 0:
    df.to_csv('sp500Constituents.csv')
