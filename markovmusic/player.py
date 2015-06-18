#!/usr/bin/env python2
import sys
import logging
from time import sleep
from mido import open_output, get_output_names
from logger import get_logger
from generator import Generator


class Player:
    """ Play generated music """

    def __init__(self, args):
        """ Initialise args and logger """
        self.args = args
        self.log = get_logger()

    def run(self):
        """ Run script """
        if self.args.list_ports:
            self.list_ports()
        else:
            self.play()

    def play(self):
        """ Generate and play music """

        # Initialise generator
        gen = Generator(self.log, self.args.input, self.args.chain_len)

        # Open output port
        with open_output(self.args.port) as output:
            self.log.info('Opened output port "%s"', output.name)

            # Generate messages
            for msg in gen.generate_messages():

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
