#!/usr/bin/env python2
import logging
import resource


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


def get_logger():
    """ Create logger """
    formatter = MemLogFormatter('[%(created)f][%(mem)s][%(name)s][%(levelname)s] %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    log = logging.getLogger('markovmusic')
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    return log
