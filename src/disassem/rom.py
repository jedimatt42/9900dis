
mne351 = {
    0b101: "A",
    0b100: "C",
    0b011: "S",
    0b111: "SOC",
    0b010: "SZC",
    0b110: "MOV"
}

mne352 = {
    0b001000: "COC",
    0b001001: "CZC",
    0b001010: "XOR",
    0b001110: "MPY",
    0b001111: "DIV"
}

mne353 = {
    0b001011: "XOP"
}

mne354 = {
    0b0000010001: "B",
    0b0000011010: "BL",
    0b0000010000: "BLWP",
    0b0000010011: "CLR",
    0b0000011100: "SETO",
    0b0000010101: "INV",
    0b0000010100: "NEG",
    0b0000011101: "ABS",
    0b0000011011: "SWPB",
    0b0000010110: "INC",
    0b0000010111: "INCT",
    0b0000011000: "DEC",
    0b0000011001: "DECT",
    0b0000010010: "X"
}

mne355 = {
    0b001100: "LDCR",
    0b001101: "STCR"
}

mne356 = {
    0b00011101: "SBO",
    0b00011110: "SBZ",
    0b00011111: "TB"
}

mne357 = {
    0b00010011: "JEQ",
    0b00010101: "JGT",
    0b00011011: "JH",
    0b00010100: "JHE",
    0b00011010: "JL",
    0b00010010: "JLE",
    0b00010001: "JLT",
    0b00010000: "JMP",
    0b00010111: "JNC",
    0b00010110: "JNE",
    0b00011001: "JNO",
    0b00011000: "JOC",
    0b00011100: "JOP"
}

mne358 = {
    0b00001010: "SLA",
    0b00001000: "SRA",
    0b00001011: "SRC",
    0b00001001: "SRL"
}

mne359 = {
    0b00000010001: "AI",
    0b00000010010: "ANDI",
    0b00000010100: "CI",
    0b00000010000: "LI",
    0b00000010011: "ORI"
}

mne3510 = {
    0b00000010111: "LWPI",
    0b00000011000: "LIMI"
}

mne3511 = {
    0b00000010110: "STST",
    0b00000010101: "STWP"
}

mne3512 = {
    0b00000011100: "RTWP"
}

mne3513 = {
    0b00000011010: "IDLE",
    0b00000011011: "RSET",
    0b00000011110: "CKOF",
    0b00000011101: "CKON",
    0b00000011111: "LREX"
}

mne_9995_453 = {
    0b0000000111: "MPYS",
    0b0000000110: "DIVS"
}


def signedByte(value):
    if value > 127:
        return (256-value) * (-1)
    else:
        return value


class ROM:
    def __init__(self, rompath, listpath, aorg):
        self.filename = rompath
        self.output = listpath
        self.pc = aorg.as_int()

    def readword(self, rom):
        bytes = rom.read(2)
        if bytes == b"":
            return None
        self.pc += 2
        return (bytes[0] << 8) + bytes[1]

    def word_to_hex(self, value):
        return ">" + "{0:#0{1}x}".format(value, 6)[2:]

    def deconstruct351(self, word):
        opcode = (word & 0xE000) >> 13
        b = (word & 0x1000) >> 12
        td = (word & 0x0C00) >> 10
        d = (word & 0x03C0) >> 6
        ts = (word & 0x0030) >> 4
        s = word & 0x000F
        return (opcode, b, td, d, ts, s)

    def mneumonic351(self, opcode, b):
        result = mne351[opcode]
        if b:
            result += 'B'
        return result

    def deconstruct352(self, word):
        opcode = (word & 0xFC00) >> 10
        d = (word & 0x03C0) >> 6
        ts = (word & 0x0030) >> 4
        s = (word & 0x000F)
        return (opcode, d, ts, s)

    def deconstruct354(self, word):
        opcode = (word & 0xFFC0) >> 6
        ts = (word & 0x0030) >> 4
        s = word & 0x000F
        return (opcode, ts, s)

    def deconstruct355(self, word):
        opcode = (word & 0xFC00) >> 10
        c = (word & 0x03C0) >> 6
        ts = (word & 0x0030) >> 4
        s = word & 0x000F
        return (opcode, c, ts, s)

    def deconstruct356(self, word):
        opcode = (word & 0xFF00) >> 8
        dis = word & 0x00FF
        return (opcode, dis)

    def deconstruct358(self, word):
        opcode = (word & 0xFF00) >> 8
        c = (word & 0x00F0) >> 4
        w = word & 0x000F
        return (opcode, c, w)

    def deconstruct359(self, word):
        opcode = (word & 0xFFE0) >> 5
        n = (word & 0x0010) >> 4
        w = word & 0x000F
        return (opcode, n, w)

    def deconstruct3510(self, word):
        opcode = (word & 0xFFE0) >> 5
        return opcode
    
    def deconstruct3511(self, word):
        opcode = (word & 0xFFE0) >> 5
        w = word & 0x000F
        return (opcode, w)

    def deconstruct3512(self, word):
        opcode = (word & 0xFFE0) >> 5
        return opcode

    def param351(self, t, v, rom):
        param = ""
        if t == 2:
            param = "@" + self.word_to_hex(self.readword(rom))
            if v != 0:
                param += "(r"
                param += str(v)
                param += ")"
            return param
        if (t == 0 or t == 1 or t == 3):
            if t == 1 or t == 3:
                param += "*"
            param += "r" + str(v)
            if t == 3:
                param += "+"
            return param
        return "error(t_%d)" % t

    def handle351(self, word, listing, rom):
        (opcode, b, td, d, ts, s) = self.deconstruct351(word)
        if opcode not in mne351.keys():
            return False
        src_param = self.param351(ts, s, rom)
        dst_param = self.param351(td, d, rom)
        line = "\t%s\t%s,%s" % (
            self.mneumonic351(opcode, b), src_param, dst_param
        )
        print(line, file=listing)
        return True

    def handle352(self, word, listing, rom):
        (opcode, d, ts, s) = self.deconstruct352(word)
        if opcode not in mne352.keys():
            return False
        src_param = self.param351(ts, s, rom)
        dst_param = "r" + str(d)
        line = "\t%s\t%s,%s" % (mne352[opcode], src_param, dst_param)
        print(line, file=listing)
        return True

    def handle353(self, word, listing, rom):
        # same format as section 3.5.2
        (opcode, d, ts, s) = self.deconstruct352(word)
        if opcode not in mne353.keys():
            return False
        src_param = self.param351(ts, s, rom)
        dst_param = "r" + str(d)
        line = "\t%s\t%s,%s" % (mne353[opcode], src_param, dst_param)
        print(line, file=listing)
        return True

    def handle354(self, word, listing, rom):
        (opcode, ts, s) = self.deconstruct354(word)
        if opcode not in mne354.keys():
            return False
        src_param = self.param351(ts, s, rom)
        line = "\t%s\t%s" % (mne354[opcode], src_param)
        print(line, file=listing)
        return True

    def handle355(self, word, listing, rom):
        (opcode, c, ts, s) = self.deconstruct355(word)
        if opcode not in mne355.keys():
            return False
        src_param = self.param351(ts, s, rom)
        line = "\t%s\t%s,%s" % (mne355[opcode], src_param, str(c))
        print(line, file=listing)
        return True

    def handle356(self, word, listing, rom):
        (opcode, dis) = self.deconstruct356(word)
        if opcode not in mne356.keys():
            return False
        line = "\t%s\t%s" % (mne356[opcode], str(dis))
        print(line, file=listing)
        return True

    def handle357(self, word, listing, rom):
        (opcode, dis) = self.deconstruct356(word)
        if opcode not in mne357.keys():
            return False
        addr = signedByte(dis) + self.pc
        line = "\t%s\t%s" % (mne357[opcode], self.word_to_hex(addr))
        print(line, file=listing)
        return True

    def handle358(self, word, listing, rom):
        (opcode, c, w) = self.deconstruct358(word)
        if opcode not in mne358.keys():
            return False
        line = "\t%s\tr%d,%d" % (mne358[opcode], w, c)
        print(line, file=listing)
        return True

    def handle359(self, word, listing, rom):
        (opcode, n, w) = self.deconstruct359(word)
        if opcode not in mne359.keys():
            return False
        iop = self.readword(rom)
        line = "\t%s\tr%d,%s" % (mne359[opcode], w, self.word_to_hex(iop))
        print(line, file=listing)
        return True

    def handle3510(self, word, listing, rom):
        opcode = self.deconstruct3510(word)
        if opcode not in mne3510.keys():
            return False
        iop = self.readword(rom)
        line = "\t%s\t%s" % (mne3510[opcode], self.word_to_hex(iop))
        print(line, file=listing)
        return True

    def handle3511(self, word, listing, rom):
        (opcode, w) = self.deconstruct3511(word)
        if opcode not in mne3511.keys():
            return False
        line = "\t%s\tr%d" % (mne3511[opcode], w)
        print(line, file=listing)
        return True

    def handle3512(self, word, listing, rom):
        opcode = self.deconstruct3512(word)
        if opcode not in mne3512.keys():
            return False
        line = "\t%s" % mne3512[opcode]
        print(line, file=listing)
        return True

    def handle3513(self, word, listing, rom):
        opcode = self.deconstruct3512(word)
        if opcode not in mne3513.keys():
            return False
        line = "\t%s" % mne3513[opcode]
        print(line, file=listing)
        return True

    def handle_9995_453(self, word, listing, rom):
        (opcode, ts, s) = self.deconstruct354(word)
        if opcode not in mne_9995_453.keys():
            return False
        src_param = self.param351(ts, s, rom)
        line = "\t%s\t%s" % (mne_9995_453[opcode], src_param)
        print(line, file=listing)
        return True

    def handleData(self, word, listing):
        line = "\tDATA\t%s" % self.word_to_hex(word)
        print(line, file=listing)
        return True

    def disassemble(self):
        with open(self.output, "w") as listing:
            with open(self.filename, "rb") as rom:
                word = self.readword(rom)
                while(word is not None):
                    self.handle351(word, listing, rom)
                    self.handle352(word, listing, rom)
                    self.handle353(word, listing, rom)
                    self.handle354(word, listing, rom)
                    self.handle355(word, listing, rom)
                    self.handle356(word, listing, rom)
                    self.handle357(word, listing, rom)
                    self.handle358(word, listing, rom)
                    self.handle359(word, listing, rom)
                    self.handle3510(word, listing, rom)
                    self.handle3511(word, listing, rom)
                    self.handle3512(word, listing, rom)
                    self.handle3513(word, listing, rom)
                    self.handle_9995_453(word, listing, rom)
                    self.handleData(word, listing)

                    word = self.readword(rom)
