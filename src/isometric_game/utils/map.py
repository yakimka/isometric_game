import dataclasses
import json
from pathlib import Path
from typing import List

from pygame.surface import Surface

from .asset import load_image


class Reader:
    def __init__(self, map_name: str, maps_dir: Path):
        self.map_name = map_name
        self.maps_dir = maps_dir

    def read(self) -> 'Map':
        map_data = self._read_map_data()
        return self._convert_map_data(map_data)

    def _read_map_data(self) -> dict:
        with open(self.maps_dir / self.map_name) as fp:
            map_data = json.load(fp)

        if map_data['infinite']:
            raise ValueError('Sorry, infinite maps are not supported yet')
        if map_data['orientation'] != 'isometric':
            raise ValueError('Sorry, supports only isometric maps for now')
        if int(map_data['tilewidth'] / 2) != map_data['tileheight']:
            raise ValueError('tilewidth must be twice as big as tileheight')

        map_data['tilesets'] = [self._read_tileset_data(item) for item in map_data['tilesets']]

        return map_data

    def _read_tileset_data(self, tileset: dict) -> dict:
        if 'source' not in tileset:
            raise ValueError('Sorry, embedded tilesets are not supported yet')

        with open(self.maps_dir / tileset['source']) as fp:
            tileset_data = json.load(fp)

        firstgid = tileset['firstgid']

        for tile in tileset_data['tiles']:
            tile['id'] += firstgid

        return tileset_data

    def _convert_map_data(self, map_data) -> 'Map':
        tile_mapping = {}
        for tileset in map_data['tilesets']:
            for tile in tileset['tiles']:
                if tile['id'] not in tile_mapping:
                    tile_mapping[tile['id']] = Tile(
                        width=tileset['tilewidth'],
                        height=tileset['tileheight'],
                        surface=load_image(self.maps_dir / tile['image']),
                    )

        layers = [
            Layer(
                name=layer['name'],
                data=[tile_mapping.get(tile_id) for tile_id in layer['data']],
                width=layer['width'],
                height=layer['height'],
                **{
                    prop['name']: prop['value']
                    for prop in layer.get('properties', [])
                },
            )
            for layer in map_data['layers']
        ]

        return Map(
            width=map_data['width'],
            height=map_data['height'],
            background_color=map_data['backgroundcolor'],
            layers=layers,
            tile_width=map_data['tilewidth'],
            tile_height=map_data['tileheight'],
        )


@dataclasses.dataclass()
class Map:
    width: int
    height: int
    background_color: str
    layers: List['Layer']
    tile_width: int
    tile_height: int


@dataclasses.dataclass()
class Layer:
    name: str
    data: List['Tile']
    width: int
    height: int
    alignment: str


@dataclasses.dataclass()
class Tile:
    width: int
    height: int
    surface: Surface
