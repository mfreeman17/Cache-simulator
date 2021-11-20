
# Matthew Freemany



import numpy as np
from math import log2
import random


class Cache:
    def __init__(self, cSize, ways=1, bSize=4):

        self.cacheSize = cSize  # Bytes
        self.ways = ways        # Default: 1 way (i.e., directly mapped)
        self.blockSize = bSize  # Default: 4 bytes (i.e., 1 word block)
        self.setSize = cSize // bSize // ways

        self.blockBits = 0
        self.setBits = 0

        if (self.blockSize != 1):
            self.blockBits = int(log2(self.blockSize))


        self.cache = np.zeros(
            (self.setSize, self.ways, self.blockSize), dtype=int)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.setSize, self.ways), dtype=int)
        self.metaCache = self.metaCache - 1

        self.hit = 0   # number of cache hits
        self.miss = 0  # number of cache misses
        self.hitlatency = 5  # cycle
        self.misspenalty = 10  # cycle

    def reset(self):
        self.cache = np.zeros(
            (self.setSize, self.ways, self.blockSize), dtype=int)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.setSize, self.ways), dtype=int)
        self.metaCache = self.metaCache - 1

        self.hit = 0
        self.miss = 0


    '''
    Returns the set number of an address

    '''

    def find_set(self, address):
        return address // (self.blockSize) % (self.setSize)

    '''
    Returns the tag of an address 
    '''

    def find_tag(self, address):
        indexSize = int(log2(self.setSize))
        return address // (self.blockSize) >> indexSize

    '''
    Search through cache for address
    return True if found
    otherwise False

    '''

    def find(self, address):
        # [blocks, ways, blockSize]
        set = self.find_set(address)
        tag = self.find_tag(address)
        block = self.cache[set]
        meta_block = self.metaCache[set]
        for i in range(0, self.ways):
            if (block[i][0] == tag): 
                #check if tag in the block
                self.hit += 1 
                for j in range(0, self.ways):
                    if (meta_block[j]==tag):
                        # check if the tag is in the meta block
                        for s in range(j,self.ways-1):
                            if (meta_block[s+1]!= -1):
                                # ensure that this address will remain in cache moves to the back of the metablock 
                                #reverses order in list                                
                                meta_block[[s, s+1]] = meta_block[[s+1, s]]
                        return(True)
        # tag not found in cache
        self.miss += 1
        return False

    '''
    Load data into the cache.
    Something might need to be evicted from the cache and send back to memory

    '''

    def load(self, address):
        set = self.find_set(address)
        tag = self.find_tag(address)
        block = self.cache[set]
        meta_block = self.metaCache[set]

        """
           If the cache is not already full
        """
        for i in range(0, self.ways):
            if (block[i][0] == -1):
                #if block empty place tag in block
                block[i][0] = tag
                for j in range(0, self.ways):
                    #place tag in metablock at the back
                    if (meta_block[j] == -1):
                        meta_block[j] = tag
                        return
        """
        If the cache is full
        """

        tag_2_remove = meta_block[0]
        for i in range(0, self.ways):
            if (block[i][0] == tag_2_remove):
                block[i][0] = tag
                for j in range(1, self.ways):
                    #move everything in meta_cache closer to the begining (the first one will be removed) 
                    meta_block[j - 1] = meta_block[j]
                #end of meta_block (last to be removed) becomes the tag
                meta_block[self.ways - 1] = tag
