import json

import requests

import config


def main():
    print('DEALS')
    deals = fetch_deals()
    print(json.dumps(deals, indent=4, sort_keys=True))

    print('DEAL PROPERTIES')
    deal_properties_data = fetch_deal_properties()
    print(json.dumps(deal_properties_data, sort_keys=True, indent=4))

    print('PIPELINES')
    pipeline_data = fetch_pipelines()
    print(json.dumps(pipeline_data, indent=4, sort_keys=True))


def fetch_pipelines():
    url = 'https://api.hubapi.com/deals/v1/pipelines?hapikey=%s' % config.HUBSPOT_HAPIKEY
    response = requests.get(url)
    response_decoded = response.content.decode('utf-8')
    data = json.loads(response_decoded)
    return data


def fetch_deal_properties():
    deal_properties_url = 'https://api.hubapi.com/properties/v1/deals/properties?hapikey=%s' % config.HUBSPOT_HAPIKEY
    response = requests.get(deal_properties_url)
    response_decoded = response.content.decode('utf-8')
    data = json.loads(response_decoded)
    return data


def fetch_deals():
    url = 'https://api.hubapi.com/deals/v1/deal/paged?hapikey=%s&includeAssociations=true&limit=250&properties=pipeline&properties=name&properties=dealstage' % config.HUBSPOT_HAPIKEY
    response = requests.get(url)
    content_decoded = response.content.decode('utf-8')
    deal_result = json.loads(content_decoded)
    deals = deal_result['deals']
    return deals


if __name__ == '__main__':
    main()
