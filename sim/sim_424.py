
'''
CPU Trace Driven: This simulator directly reads instruction traces
from a file (stored in ../Traces or ../Traces), and simulates a simplified model
of a "core" that generates memory requests. Each line
in the trace file represents a memory request, and can have
one of the following two formats.

<num-cpuinst> <addr-read>: For a line with two tokens, the
first token represents the number of CPU (i.e., non-memory) instructions
before the memory request, and the second token is the decimal address of
a read. These traces can either be artificial or derived from SPEC 2006
suite (https://www.spec.org/) (using PIN Tool from Intel)

<num-cpuinst> <addr-read> <addr-writeback>: For a line with
three tokens, the third token is the decimal address of the
writeback request, which is the dirty cache-line eviction caused
by the read request before it.


Example command line:
python sim_424.py 403.gcc.gz 16384 16 128 1000
'''

from math import log2
import random
import sys
import os
import gzip
import numpy as np
from cache_424_w import Cache
from memory import Memory

if __name__ == "__main__":

    try:

        files = [sys.argv[1]]
        cacheSize = int(sys.argv[2])
        ways = int(sys.argv[3])
        block_size = int(sys.argv[4])
        trace_elements = int(sys.argv[5])

    except:

        print('sim_424.py trace cacheSize(Bytes) #ofWays blockSize(Bytes) trace_elements')



    print(files, cacheSize, ways, block_size)
    cache = Cache(cacheSize, ways, block_size)
    memory = Memory(2048)
    cache.reset()

    for file in files:
        print('python sim_424.py', format(file), cacheSize, ways, block_size, trace_elements, '\n')

        cache.reset()
        compute = 0
        misspenalty = 0
        rowhits = 0

        if format(file).split('.')[-1] == "gz":
            with gzip.open('../Traces/{}'.format(file),'rt') as f:
                trace = f.readlines()
                if (trace_elements > len(trace)):
                    trace_elements = len(trace)
        else:
            with open('../Traces/{}'.format(file)) as f:
                trace = f.readlines()
                if (trace_elements > len(trace)):
                    trace_elements = len(trace)

        for t in range(trace_elements):
            if t % 1000 == 0:
                print('Processing your program trace, progress so far =', int(t / trace_elements * 100), '%')
            compute += int(trace[t].split(' ')[0])
            address = int(trace[t].split(' ')[1])


            found = cache.find(address)

            if found==False:
                cache.load(address)
                print('set and tag of', hex(address), 'is', cache.find_set(address), cache.find_tag(address))
            if found:
                print('address', hex(address), 'CACHE HIT. Good Job.')

            else:
                if (memory.is_row_hit(address)):
                    misspenalty += memory.determine_miss_penalty(address)
                    rowhits += 1
                    #print('address', hex(address), 'CACHE MISS. Loading from memory... it is a ROW BUFFER HIT')
                else:
                    misspenalty += memory.determine_miss_penalty(address)
                    #print('address', hex(address), 'CACHE MISS. Loading from memory... it is a ROW BUFFER MISS (will take more time to load from memory)')

        load_requests = trace_elements
        misses = load_requests - cache.hit
        miss_rate = misses/load_requests
        hit_rate = 1 - miss_rate
        avg_misspenalty = misspenalty/misses

        print('total cache accesses', load_requests)
        print('total cache misses', misses)
        print('total cache hits', (load_requests - misses))
        print('miss_rate', miss_rate)
        print('hit_rate', 1 - miss_rate)

        if (misses!=0):

            print('Row Buffer Hit Rate', rowhits/misses)
            print('Average Miss Penalty', avg_misspenalty)

        amat = cache.hitlatency + miss_rate*avg_misspenalty
        avg_cpi_ideal = 1.0

        print('AMAT', amat)

        print(int((avg_cpi_ideal + miss_rate*avg_misspenalty + (load_requests*miss_rate*avg_misspenalty)/(load_requests + compute))))

        print('Finished processing the specified part of the program trace, progress =', ((t+1) / trace_elements) * 100, '%')
        print('Percentage of the entire program trace executed =', ((t+1) / len(trace)) * 100, '%', '\n')
        print('=====================================')
