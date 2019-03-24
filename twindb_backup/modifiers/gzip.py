# -*- coding: utf-8 -*-
"""
Module defines modifier that compresses a stream with gzip
"""
from contextlib import contextmanager
from subprocess import Popen, PIPE

from twindb_backup.modifiers.base import Modifier


class Gzip(Modifier):
    """
    Modifier that compresses the input_stream with gzip.
    """
    suffix = ".gz"

    def __init__(self, input_stream, level=9):
        """
        Modifier that uses gzip compression

        :param input_stream: Input stream. Must be file object
        :param level: compression level from 1 to 9 (fastest to best)
        :type level: int|string
        """
        super(Gzip, self).__init__(input_stream)

        if level is None or level == '':
            level = 9

        self._level = int(level)

    def get_compression_cmd(self):
        """get compression program cmd"""
        return ['gzip', '-{0}'.format(self._level), '-c', '-']

    def get_decompression_cmd(self):
        """get decompression program cmd"""
        return ['gunzip', '-c']

    @contextmanager
    def get_stream(self):
        """
        Compress the input stream and return it as the output stream

        :return: output stream handle
        :raise: OSError if failed to call the gzip command
        """
        with self.input as input_stream:
            proc = Popen(self.get_compression_cmd(),
                         stdin=input_stream,
                         stdout=PIPE)
            yield proc.stdout
            proc.communicate()

    def revert_stream(self):
        """
        Decompress the input stream and return it as the output stream

        :return: output stream handle
        :raise: OSError if failed to call the gpg command
        """
        return self._revert_stream(self.get_decompression_cmd())
