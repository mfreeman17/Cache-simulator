import os
import subprocess

file_list = ["462.libquantum.gz",
             "464.h264ref.gz", "403.gcc.gz", "445.gobmk.gz"]
cpi_list = [[[]]]
ways = [1, 4, 8, 16]
blocks = [16, 32, 64, 128, 256]
string= "python3 sim_424.py " + file_list[0] + " 16384 " + str(
    ways[0]) + " " + str(blocks[0]) + " 1000"
cmd = "date"
os.system(string)
returned_output = subprocess.check_output(python3 )
print(returned_output)
