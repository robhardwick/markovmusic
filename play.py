#!/usr/bin/env python2
from argparse import ArgumentParser
from markovmusic.player import Player


parser = ArgumentParser()
parser.add_argument('--input',
                    default='input/bach', metavar='PATH',
                    help='MIDI input, either a single file or a directory')
parser.add_argument('--chain-len',
                    type=int, default=4, metavar='LENGTH',
                    help='Length of Markov chains to generate')
parser.add_argument('--time-scale', metavar='SCALE',
                    type=int, default=1,
                    help='Temporal scale')
parser.add_argument('--port',
                    default=None, metavar='NAME',
                    help='Output MIDI port name')
parser.add_argument('--list-ports',
                    action='store_true',
                    help='List available MIDI ports')

player = Player(parser.parse_args())
player.run()
