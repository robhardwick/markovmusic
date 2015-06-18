#!/usr/bin/env python2
import os
from collections import deque
from random import choice, randint

from mido import MidiFile


class Generator:
    """ Generate music """
    MSG_TYPES = ('note_on', 'note_off',)

    def __init__(self, log, input_path, chain_len):
        """ Get MIDI messages and chains from input """
        self.log = log
        self.chain_len = chain_len

        if os.path.isfile(input_path):
            files = [input_path]
        elif os.path.isdir(input_path):
            files = []
            for f in os.listdir(input_path):
                path = os.path.join(input_path, f)
                if os.path.isfile(path):
                    files.append(path)
        else:
            self.log.error('Unknown input "%s"', input_path)
            raise Exception('Unknown input')

        self.msgs = []
        for f in files:
            try:
                with MidiFile(f) as midi:
                    self.log.info('Opened input file "%s"', f)
                    self.msgs.extend(msg for msg in midi if msg.type in self.MSG_TYPES)
            except IOError:
                self.log.error('Unable to open input file "%s"', f)
                raise Exception('Unable to open input')

        # Get total messages
        self.msg_count = len(self.msgs)

        # Build chains
        self.chains = {}
        for t in self.get_chains():
            key = self.chain_key(t[0:-1])
            if key in self.chains:
                self.chains[key].append(t[-1])
            else:
                self.chains[key] = [t[-1]]

    def get_chains(self):
        """ Generator for message chains """
        if self.msg_count < self.chain_len:
            return
        for i in xrange(self.msg_count - self.chain_len):
            yield tuple(self.msgs[i : i + self.chain_len + 1])

    def chain_key(self, msgs):
        """ Get tuple key for chains """
        return tuple(m.note for m in msgs)

    def generate_messages(self):
        """ Generate messages """
        seed = randint(0, self.msg_count - (self.chain_len - 1))
        q = deque(self.msgs[seed : seed + self.chain_len], self.chain_len + 1)
        while True:
            q.append(choice(self.chains[self.chain_key(q)]))
            yield q.popleft()
