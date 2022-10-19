#!/usr/bin/python3

import sys
from decimal import Decimal

def update_ver(original_ver):
    ver_part1 = int(original_ver[:-4])
    ver_part2 = Decimal(original_ver[-3:])
    if ver_part2 < Decimal('9.9'):
        ver_part2 = ver_part2 + Decimal('0.1')
    else:
        ver_part1 = ver_part1 + 1
        ver_part2 = Decimal('0.0')
    new_ver = str(ver_part1) + '.' + str(ver_part2)
    return new_ver

temp = update_ver(sys.argv[1])
print(temp)
