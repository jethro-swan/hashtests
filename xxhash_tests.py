import datetime, time
import xxhash
#import json
#import secrets.randbits
#import math
import os
#from base64 import b64encode
#import cdblib # pure-cdb
import sys
#from pathlib import Path

import names
import random

n_passes = 1000

#hash_used = '64'
hash_used = 'xxh3_64'
#hash_used = 'xxh3_128'

#------------------------------------------------------------------------------
# Return current date+time in "%Y-%m-%d_%H%M%S" format
# YYYYMMDDhhmmss
def filename_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")


# See https://pypi.org/project/names/
# The "names" package is used to generate a fairly realist namespace name (a
# surname should be close enough).

def invent_name():
    return names.get_last_name()


# Allowing for 100 identities per person (which should be more than enough) and
# a global population of 10^10 (it is currently just over 8*10^9), then we must
# allow for 10^12 human identies.  If we assume a ratio of 100:1 sensors/human
# (which may actually be rather too small), we should probably allow for 10^14
# identities.
#
# If we assume a namespace contains no more than 10,000 names (which is a very
# roomy overestimate - some may contain only a handful, and most should
# probably not exceed 150 to 500), then the number of namespaces required will
# probably be considerably less than 10^9.
#
# If we assume that the namespaces are all quite small (no more than 150 names)
# and that the number of names distributed among them is up to 10^14, the depth
# of the namespace path may be as little as the base 150 logarithm of 10^14, so
# around ceil(log_150(10^14)) = 7.
#
# If we assume that the namespaces are generally similar in size (a far less
# reasonable assumption for which we can compensate by overestimating the
# number of namespaces by at least an order of magnitude), the the maximum
# depth of a namespace might be estimated adequately as log_10(10^9) = 6

def nhash(name, hash_used):
    if hash_used == 'xxh3_64':
        return xxhash.xxh3_64_hexdigest(name.strip())
    elif hash_used == 'xxh3_128':
        return xxhash.xxh3_128_hexdigest(name.strip())
    else:
        return xxhash.xxh64(name.strip()).hexdigest()
    

def invent_namespace_path():
    # To err on the side of caution, let's assume that a realistic depth of a
    # namespace path is between 1 and 7 names ...
    hrns = 'gaia' # root namespaceq
    fip = nhash(hrns, hash_used)
    for n in range(random.randint(1,7)):
        nsname = invent_name()
        # The FIP is extended:
        fip += '/'
        fip += nhash(nsname, hash_used)
        # The HRNS is extended:
        hrns += '.'
        hrns += nsname
    time_before = time.time()
    fph = nhash(hrns, hash_used)
    time_after = time.time()
    time_taken = time_after - time_before
    return hrns, fip, fph, time_taken


with open(filename_timestamp() + '_' + hash_used + '.csv', 'w') as csv_f:
    # The output is sent to a CSV file:
    csv_f.write('HRNS;FIP;FPH;hash time\n')
    total_hash_time = 0
    for i in range(n_passes):
        hrns, fip, fph, time_taken = invent_namespace_path()
        csv_f.write(hrns + ';' + fip + ';' + fph + ';' + str(time_taken) + '\n')
        total_hash_time += time_taken
    csv_f.write('\n;;mean hash time:;' + str(total_hash_time/n_passes))
