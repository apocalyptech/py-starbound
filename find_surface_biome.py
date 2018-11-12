#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import os
import re
import sys
import argparse
import starbound

base_dir = '/usr/local/games/starbound-storage'
player_dir = os.path.join(base_dir, 'player')
universe_dir = os.path.join(base_dir, 'universe')

parser = argparse.ArgumentParser(description='Find surface biomes/dungeons')
parser.add_argument('biome',
    type=str,
    metavar='biome',
    help='Biome/Dungeon to search for')
args = parser.parse_args()
to_find = args.biome

map_files = os.listdir(universe_dir)
#map_files = ['-452761947_-908966365_-76376699_6_2.world']

def strip_colors(input_string):
	"""
	Strips color information from a string
	"""
	return re.sub('\^\w+?;', '', input_string)

for filename in map_files:
    if filename.endswith('.world'):
        with open(os.path.join(universe_dir, filename), 'rb') as df:
            world = starbound.World(df)
            world.read_metadata()
            md = world.metadata
            wt = md['worldTemplate']
            cp = wt['celestialParameters']
            if cp:
                report_name = '{} at ({}, {}) ({})'.format(
                        strip_colors(cp['name']),
                        cp['coordinate']['location'][0],
                        cp['coordinate']['location'][1],
                        filename,
                        )
            else:
                report_name = 'Unknown world ({})'.format(filename)
            wp = wt['worldParameters']
            if 'surfaceLayer' in wp:
                layer = wp['surfaceLayer']
                found = False
                for dungeon in layer['dungeons']:
                    if dungeon == to_find:
                        found = True
                        break
                if not found:
                    for label in ['primaryRegion', 'primarySubRegion']:
                        region = layer[label]
                        if region['biome'] == to_find:
                            found = True
                            break
                if not found:
                    for label in ['secondaryRegions', 'secondarySubRegions']:
                        for layerstruct in layer[label]:
                            if layerstruct['biome'] == to_find:
                                found = True
                                break
                        if found:
                            break
                if found:
                    print(report_name)
