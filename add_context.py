import logging
from datapackage_pipelines.wrapper import ingest, spew


_, datapackage, resource_iterator = ingest()

for res in datapackage['resources']:
  res['schema']['fields'].append({'type': 'string', 'name': 'budget type'})
  res['schema']['fields'].append({'type': 'string', 'name': 'date'})

def process(res):
  name = res.spec['name']
  budget_type = datapackage[name]['budget_type']
  date = datapackage[name]['date']
  for row in res:
    row['budget type'] = budget_type
    row['date'] = date
    yield row

spew(datapackage,  (process(res) for res in resource_iterator))

logging.info(datapackage)
