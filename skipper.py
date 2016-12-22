import logging
from datapackage_pipelines.wrapper import ingest, spew


_, datapackage, resource_iterator = ingest()

def intTryParse(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def process(res):
  for row in res:
    if intTryParse(row['1.0']):
      yield row

spew(datapackage,  (process(res) for res in resource_iterator))
