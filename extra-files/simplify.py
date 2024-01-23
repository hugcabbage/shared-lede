#!/usr/bin/env python3
import sys

from tools.process_text import simplify_config

if __name__ == '__main__':
    simplify_config(sys.argv[1])
    print('Done')
