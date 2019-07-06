
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
        # todo: track PC, and adjust displacement
        addr = signedByte(dis) + self.pc
        line = "\t%s\t%s" % (mne357[opcode], self.word_to_hex(addr))
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
                    self.handleData(word, listing)

                    word = self.readword(rom)
