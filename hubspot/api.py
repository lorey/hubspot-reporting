import json
import urllib

import requests

import config
from hubspot.deals import Deal, Stage

BASE_URL = 'https://api.hubapi.com/'


def fetch_pipelines():
    url = BASE_URL + 'deals/v1/pipelines?hapikey=%s' % config.HUBSPOT_HAPIKEY
    response = requests.get(url)
    response_decoded = response.content.decode('utf-8')
    data = json.loads(response_decoded)
    return data


def fetch_deal_properties():
    deal_properties_url = BASE_URL + 'properties/v1/deals/properties?hapikey=%s' % config.HUBSPOT_HAPIKEY
    response = requests.get(deal_properties_url)
    response_decoded = response.content.decode('utf-8')
    data = json.loads(response_decoded)
    return data


def fetch_deals():
    parameters = {
        'hapikey': config.HUBSPOT_HAPIKEY,
        'includeAssociations': 'true',
         'limit': 250,
        'properties': ['name', 'pipeline', 'dealstage', 'amount'],
    }

    special_parameter_keys = ['properties']
    special_parameters_encoded = '&'.join([('properties=%s' % p) for p in parameters['properties']])

    plain_parameters = {k: v for k, v in parameters.items() if k not in special_parameter_keys}
    plain_parameters_encoded = urllib.parse.urlencode(plain_parameters)

    parameters_encoded = plain_parameters_encoded + '&' + special_parameters_encoded
    url = BASE_URL + 'deals/v1/deal/paged?' + parameters_encoded
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError('Response %d, not 200: %s' % (response.status_code, response.content))
    content_decoded = response.content.decode('utf-8')
    deal_result = json.loads(content_decoded)
    deals = [Deal(deal_data) for deal_data in deal_result['deals']]
    return deals


def execute_request(endpoint, parameters):
    if 'hapikey' not in parameters:
        parameters['hapikey'] = config.HUBSPOT_HAPIKEY

    encoded_parameters = urllib.parse.urlencode(parameters)
    url = BASE_URL + endpoint + '?%s' % encoded_parameters
    response = requests.get(url)
    response_decoded = response.decode('utf-8')
    data = json.loads(response_decoded)
    return data


def fetch_stage(id):
    pipeline_data = fetch_pipelines()  # replace
    stages_with_id = [stage for pipeline in pipeline_data for stage in pipeline['stages'] if
                      stage['stageId'] == id]
    data = next(iter(stages_with_id), None)
    return Stage(data)
