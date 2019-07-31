#!/usr/bin/env python

import sys

words = open('./PSE/training_data_higherstruct.txt').read().split()

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
