#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import os
import re
import starbound

base_dir = '/usr/local/games/starbound-storage'
player_dir = os.path.join(base_dir, 'player')
universe_dir = os.path.join(base_dir, 'universe')

#map_files = os.listdir(universe_dir)
map_files = ['-452761947_-908966365_-76376699_6_2.world']

def strip_colors(input_string):
	"""
	Strips color information from a string
	"""
	return re.sub('\^\w+?;', '', input_string)

for filename in map_files:
    if filename.endswith('.world'):
        dungeons = set()
        biomes = set()
        with open(os.path.join(universe_dir, filename), 'rb') as df:
            world = starbound.World(df)
            world.read_metadata()
            md = world.metadata
            wt = md['worldTemplate']
            cp = wt['celestialParameters']
            if cp:
                print('{} ({})'.format(strip_colors(cp['name']), filename))
                if 'terrestrialType' in cp['parameters']:
                    print('  * World Types: {}'.format(', '.join(cp['parameters']['terrestrialType'])))
            else:
                print('Unknown world ({})'.format(filename))
            wp = wt['worldParameters']
            for key, layer in wp.items():
                if key.endswith('Layer'):
                    for dungeon in layer['dungeons']:
                        dungeons.add(dungeon)
                    for label in ['primaryRegion', 'primarySubRegion']:
                        region = layer[label]
                        biomes.add(region['biome'])
                    for label in ['secondaryRegions', 'secondarySubRegions']:
                        #if len(layer[label]) > 1:
                        #    print('   * Has {} {}'.format(len(layer[label]), label))
                        for layerstruct in layer[label]:
                            biomes.add(layerstruct['biome'])
                elif key.endswith('Layers'):
                    layerlist = layer
                    for layer in layerlist:
                        for dungeon in layer['dungeons']:
                            dungeons.add(dungeon)
                        for label in ['primaryRegion', 'primarySubRegion']:
                            region = layer[label]
                            biomes.add(region['biome'])
                        for label in ['secondaryRegions', 'secondarySubRegions']:
                            #if len(layer[label]) > 1:
                            #    print('   * Has {} {}'.format(len(layer[label]), label))
                            for layerstruct in layer[label]:
                                biomes.add(layerstruct['biome'])
            if len(dungeons) > 0:
                print('  * Dungeons: {}'.format(', '.join(sorted(dungeons))))
            else:
                print('  * Dungeons: -')
            if len(biomes) > 0:
                print('  * Biomes: {}'.format(', '.join(sorted(biomes))))
            else:
                print('  * Biomes: -')
            print('')
