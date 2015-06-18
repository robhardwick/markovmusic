#!/usr/bin/env python2
import os
import sys
import logging
import resource
from collections import deque
from random import choice, randint
from time import sleep
from argparse import ArgumentParser

from mido import MidiFile, open_output, get_output_names


class MemLogFormatter(logging.Formatter):
    UNITS = ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']

    def mem_fmt(self, mem, suffix='B'):
        for unit in self.UNITS:
            if abs(mem) < 1024.0:
                return "%3.1f%s%s" % (mem, unit, suffix)
            mem /= 1024.0
        return "%.1f%s%s" % (mem, 'Yi', suffix)

    def format(self, record):
        mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        record.mem = self.mem_fmt(mem)
        return super(MemLogFormatter , self).format(record)


class Music:
    """ Generate music """
    MSG_TYPES = ('note_on', 'note_off',)

    def __init__(self, args):
        """ Initialise """
        self.args = args

        # Init logger
        formatter = MemLogFormatter('[%(created)f][%(mem)s][%(name)s][%(levelname)s] %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.log = logging.getLogger('music')
        self.log.addHandler(handler)
        self.log.setLevel(logging.INFO)

    def read_input(self):
        """ Get MIDI messages and chains from input """

        if os.path.isfile(self.args.input):
            files = [self.args.input]
        elif os.path.isdir(self.args.input):
            files = []
            for f in os.listdir(self.args.input):
                path = os.path.join(self.args.input, f)
                if os.path.isfile(path):
                    files.append(path)
        else:
            self.log.error('Unknown input "%s"', self.args.input)
            sys.exit(1)

        msgs = []
        for f in files:
            try:
                with MidiFile(f) as midi:
                    self.log.info('Opened input file "%s"', f)
                    msgs.extend(msg for msg in midi if msg.type in self.MSG_TYPES)
            except IOError:
                self.log.error('Unable to open input file "%s"', f)
                sys.exit(1)

        # Get total messages
        msg_count = len(msgs)

        # Build chains
        chains = {}
        for t in self.get_chains(msgs, msg_count):
            key = self.chain_key(t[0:-1])
            if key in chains:
                chains[key].append(t[-1])
            else:
                chains[key] = [t[-1]]

        return msgs, msg_count, chains

    def get_chains(self, msgs, msg_count):
        """ Generator for message chains """
        if msg_count < self.args.chain_len:
            return
        for i in xrange(msg_count - self.args.chain_len):
            yield tuple(msgs[i : i + self.args.chain_len + 1])

    def chain_key(self, msgs):
        """ Get tuple key for chains """
        return tuple(m.note for m in msgs)

    def generate_messages(self, msgs, msg_count, chains):
        """ Generate messages """
        seed = randint(0, msg_count - (self.args.chain_len - 1))
        q = deque(msgs[seed : seed + self.args.chain_len], self.args.chain_len + 1)
        while True:
            q.append(choice(chains[self.chain_key(q)]))
            yield q.popleft()

    def play(self):
        """ Generate and play music """

        # Open input file(s)
        msgs, msg_count, chains = self.read_input()

        # Open output port
        with open_output(self.args.port) as output:
            self.log.info('Opened output port "%s"', output.name)

            # Generate messages
            for msg in self.generate_messages(msgs, msg_count, chains):

                # Sleep
                sleep(msg.time * self.args.time_scale)

                # Play message
                output.send(msg)

                # Log message
                self.log.info('msg(c=%d, n=%d, v=%d, t=%f)',
                    msg.channel, msg.note, msg.velocity, msg.time)

    def list_ports(self):
        """ List MIDI ports """
        ports = get_output_names()
        if len(ports) < 1:
            self.log.error('No open MIDI ports')
            sys.exit(1)
        print 'Open Ports'
        print '----------'
        print '\n'.join(ports)

    def run(self):
        """ Run script """
        if self.args.list_ports:
            self.list_ports()
        else:
            self.play()


if __name__ == '__main__':
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

    music = Music(parser.parse_args())
    music.run()
