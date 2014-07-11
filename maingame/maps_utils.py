# -*- coding: utf-8 -*-

import json

from .models import AvailableMaps

def build_map_from_json(filename, json_file, map_name, commit=False):
    json_map = json.load(json_file)
    layer = json_map['layers'][0]
    future_map = AvailableMaps(name=map_name)
    future_map.width = json_map['width']
    future_map.height = json_map['height']
    future_map.tile_size = json_map['tileheight']
    future_map.map_file = filename
    future_map.sprite_file = layer['properties']['tiles']
    if "author" in json_map['properties']:
        future_map.author = json_map['properties']['author']
    future_map.data = layer['data']
    if commit:
        future_map.save()
    return future_map


def import_map(filename, map_name, commit=False, file_format="json"):
    json_file = open(filename)
    return build_map_from_json(filename, json_file, map_name, commit)


