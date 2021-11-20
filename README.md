# cachesim
This simulator directly reads instruction traces
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

navigate to sim then run the simiulator the following way:
  
  python sim_424.py [trace_file] [cacheSize(Bytes)] [#ofWays -optional ] [BlockSize(Bytes)-optional ] [trace_elements]
  
example:
  python sim_424.py 403.gcc.gz 16384 16 128 1000
