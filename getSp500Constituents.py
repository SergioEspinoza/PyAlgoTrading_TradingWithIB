from datapackage import Package
import pandas as pd

package = Package('https://datahub.io/core/s-and-p-500-companies/datapackage.json')

# print list of all resources:
print(package.resource_names)

csv_str = ''



# print processed tabular data (if exists any)
for resource in package.resources:
    if resource.descriptor['datahub']['type'] == 'derived/csv' and \
    resource.descriptor['name'] == 'constituents_csv':
        data_sp500 = resource.read()
        df = pd.DataFrame(data=data_sp500, columns=['symbol', 'name', 'sector'])
        print(df.head())
        break



if len(df['symbol'] ) > 0:
    df.to_csv('sp500Constituents.csv')
