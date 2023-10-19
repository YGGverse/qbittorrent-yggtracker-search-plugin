# VERSION: 1.00
# LICENSE: MIT
# AUTHORS: https://github.com/YGGverse/qbittorrent-yggtracker-search-plugin

import json
from urllib.parse import urlencode, unquote

from novaprinter import prettyPrinter
from helpers import retrieve_url

class yggtracker(object):

  name = 'YGGtracker'
  url = 'https://github.com/YGGverse/YGGtracker'

  def __init__(self):
    pass

  def search(self, what, cat='all'):

    # get distributed nodes registry
    nodes = retrieve_url("https://raw.githubusercontent.com/YGGverse/qbittorrent-yggtracker-search-plugin/main/nodes.json")
    nodes_json = json.loads(nodes)

    # check empty response
    if len(nodes_json) == 0:
      return

    # parse results
    for node in nodes_json:

      # apply query request
      what = unquote(what)
      params = {
        'query': what
      }

      # apply locales filter
      if len(node['locales']) > 0:
        params['locales'] = '|'.join(node['locales'])

      # apply sensitive filter
      if node['sensitive'] is True:
        params['sensitive'] = '1'
      if node['sensitive'] is False:
        params['sensitive'] = '0'

      # apply yggdrasil filter
      if node['yggdrasil'] is True:
        params['yggdrasil'] = '1'
      if node['yggdrasil'] is False:
        params['yggdrasil'] = '0'

      # send api request
      response = retrieve_url(node['api'] % urlencode(params))
      response_json = json.loads(response)

      # check empty response
      if len(response_json['torrents']) == 0:
        continue

      # parse results
      for item in response_json['torrents']:
        res = {
          'link': item['torrent']['file']['url'],
          'name': item['torrent']['file']['name'],
          'size': str(item['torrent']['file']['size']) + " B",
          'seeds': item['torrent']['scrape']['seeders'],
          'leech': item['torrent']['scrape']['leechers'],
          'engine_url': node['url'],
          'desc_link': item['torrent']['url'][node['locale']]
        }
        prettyPrinter(res)