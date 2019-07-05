# Iterative 9900 disassembly

Good disassembly can need help identifying entrypoints into a ROM.  Particularly when the
ROM is fronted with some header information. 

The TMS9900 series CPUs expect a table of entrypoint addresses at the beginning of the System ROM.
Cartridges or hardware extension ROMs usually have a list of entrypoints or in the case of the 
TI-99/4A several lists referenced by a header. 

The goal of this disassembler is to output a file that can be used as input again, after the
user marks up known entry points, and data chunks.

The output should assemble again using xas99.py from the xdt99 tool suite.



