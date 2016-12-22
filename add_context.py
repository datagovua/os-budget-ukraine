import logging
from datapackage_pipelines.wrapper import ingest, spew


_, datapackage, resource_iterator = ingest()

def process(res):
  name = res.spec['name']
  budget_type = datapackage[name]['budget_type']
  logging.info(budget_type)
  res.spec['schema']['fields'].append({'type': 'string', 'name': 'BUDGET_TYPE'})
  for row in res:
    row['BUDGET_TYPE'] = budget_type
    logging.info(row)
    yield row

spew(datapackage,  (process(res) for res in resource_iterator))
