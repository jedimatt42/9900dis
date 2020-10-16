# Iterative 9900 disassembly

Good disassembly can need help identifying entrypoints into a ROM.  Particularly when the
ROM is fronted with some header information.

The TMS9900 series CPUs expect a table of entrypoint addresses at the beginning of the System ROM.
Cartridges or hardware extension ROMs usually have a list of entrypoints or in the case of the
TI-99/4A several lists referenced by a header.

The goal of this disassembler is to output a file that can be used as input again, after the
user marks up known entry points, and data chunks.

The output should assemble again using xas99.py from the xdt99 tool suite.

## Usage

```
Usage: main.py [OPTIONS]

  TMS9900 disassembler by Jedimatt42

Options:
  --rom PATH      ROM file to disassemble  [required]
  --listing PATH  listing file to generate  [required]
  --aorg ADDRESS  the address of the first byte in the input ROM. Specified in
                  hex such as 0x0000
  --cpu TEXT      cpu type, one of 9900 or 9995. Defaults to 9900
  --version       Show the version and exit.
  --help          Show this message and exit.
```

## Examples

```
9900dis --aorg 6000 --rom sys.bin --listing sys.asm
```

user may then edit sys.asm, and modifications will be read back and preserved during
subsequent disassembling.

A typical raw output line may be something like:

```
      	SOCB    @>028a,r2        ; pc:>0000 w:>f0a0
```

### Data

The comment line contains the program counter value, and the word at that location in the disassembled ROM.

You may force the disassembly to treat a word as 'DATA' by adding a format code: f:data, as in this example:

```
      	SOCB    @>028a,r2        ; pc:>0000 w:>f0a0 f:data
```

re-running the disassembler will then produce:

```
      	DATA    >f0a0            ; pc:>0000 w:>f0a0 f:data
```

Additional instructions may follow as parameter words are no longer consumed for that instruction.

### Labels

Labels may be inserted, and they will remain associated to the PC for that line

```
RESET 	DATA    >f0a0            ; pc:>0000 w:>f0a0 f:data
```

References will utilized the symbolic label name when re-running the disassembler, such as:

```
      	BLWP    @RESET           ; pc:>0824 w:>0420
```

### Equates

You may define lines for equates such as

```
VDPIO	EQU	>E000
```

When the value is found as a parameter, the equate symbol will be used instead

```
	MOVB	@VDPIO,r8
```

### Comments

Comments may be added after the pc/w/f segment following another ';' semicolon. They will be captured and regenerated.

```
      	BLWP    @RESET           ; pc:>0824 w:>0420   ; Go back to title screen
```

# Running

1. Install pipenv and python3
2. create virtual env

```
pipenv install --python 3.8
```

then:

```
pipenv shell
python src/disassem/main.py --help
```

# TODO

1. Learn setup.py
2. Make it an installable python package with command line tool entry script.
