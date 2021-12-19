import dataclasses
import json
from pathlib import Path
from typing import List, Tuple

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
        layers = []
        for layer in map_data['layers']:
            layers.append(
                Layer(
                    name=layer['name'],
                    data=layer['data'],
                    width=layer['width'],
                    height=layer['height'],
                    x=layer['x'],
                    y=layer['y'],
                    offset=(layer.get('offsetx', 0), layer.get('offsety', 0)),
                )
            )

        tilesets = []
        for tileset in map_data['tilesets']:
            tiles = []
            for tile in tileset['tiles']:
                tiles.append(
                    Tile(
                        id=tile['id'],
                        image=self.maps_dir / tile['image'],
                        width=tile['imagewidth'],
                        height=tile['imageheight'],
                        offset=(tileset['tileoffset']['x'], tileset['tileoffset']['y']),
                    )
                )
            tilesets.append(
                Tileset(
                    name=tileset['name'],
                    margin=tileset['margin'],
                    spacing=tileset['spacing'],
                    tile_width=tileset['tilewidth'],
                    tile_height=tileset['tileheight'],
                    tile_offset=(tileset['tileoffset']['x'], tileset['tileoffset']['y']),
                    tiles=tiles,
                )
            )

        return Map(
            width=map_data['width'],
            height=map_data['height'],
            background_color=map_data['backgroundcolor'],
            layers=layers,
            tile_width=map_data['tilewidth'],
            tile_height=map_data['tileheight'],
            tilesets=tilesets,
        )


# TODO: add from_dict method for dataclasses
#   maybe delete tilesets, tiles_mapping and replace ids in layers with tile objects

@dataclasses.dataclass()
class Map:
    width: int
    height: int
    background_color: str
    layers: List['Layer']
    tile_width: int
    tile_height: int
    tilesets: List['Tileset']
    tile_mapping: dict = dataclasses.field(init=False)

    def __post_init__(self):
        self.tile_mapping = {}
        for tileset in self.tilesets:
            for tile in tileset.tiles:
                self.tile_mapping[tile.id] = tile


@dataclasses.dataclass()
class Layer:
    name: str
    data: List[int]
    width: int
    height: int
    x: int
    y: int
    offset: Tuple[int, int]


@dataclasses.dataclass()
class Tileset:
    name: str
    margin: int
    spacing: int
    tile_width: int
    tile_height: int
    tile_offset: Tuple[int, int]
    tiles: List['Tile']


@dataclasses.dataclass()
class Tile:
    id: int
    image: Path
    width: int
    height: int
    offset: Tuple[int, int]
    surface: Surface = dataclasses.field(init=False)

    def __post_init__(self):
        self.surface = load_image(self.image)
