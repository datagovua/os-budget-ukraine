import logging
from datapackage_pipelines.wrapper import ingest, spew
from pyunpack import Archive
import urllib.request


_, datapackage, resource_iterator = ingest()


def create_dir(dir_name):
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)

def remove_dir(dir_name):
  if os.path.exists(dir_name):
    shutil.rmtree(dir_name)

def download(archive_url, download_to):
  logging.info('Downloading file from %s...' % archive_url)
  urllib.request.urlretrieve(archive_url, download_to)
  logging.info('Saved to %s' % download_to)

def unpack(archive_name, extract_dir):
  logging.info('Extracting %s' % archive_name)
  extracted = Archive(archive_name).extractall(extract_dir)
  logging.info('Extracted to %s' % extract_dir)
  return extracted

def download_and_unzip(url, filename):
  download(url, '/tmp/%s' % filename)
  files = unpack('/tmp/%s' % filename, '/tmp/')
  logging.info(files)

resources = []
for res in datapackage['resources']:
  download_and_unzip(res['url'], res['filename'])
  for file_obj in res['files']:
    filename = file_obj['filename']
    for sheet in file_obj['sheets']:
      sheet_id = sheet['id']
      resource_name = sheet['name']
      resources.append({
        'url': 'file:///tmp/%s' % filename,
        'sheet': sheet_id,
        'headers': sheet['headers'],
        'name': resource_name
#      'schema': { 'fields': file_obj['sheets'][sheet['id']]['fields'] }
      })
      datapackage[resource_name] = {'budget_type': sheet['budgetType']}

datapackage['resources'] = resources
datapackage['resource_params'] = resource_params
logging.info(datapackage) 

spew(datapackage, resource_iterator)
