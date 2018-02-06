import binascii
import re
import sys


def hexdump(filename):
    offset = 0
    bytesInFile = 0
    asciiString = ""

    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(16), b''):
            rawBytes = binascii.hexlify(block)

            # hex spacing
            readBlock = re.sub('(..)', r'\1 ', rawBytes.decode('utf-8'))
            readBlockList = readBlock.split()
            bytesInFile += len(readBlockList)
            formattedBlock = ""
            for x in range(0, len(readBlockList)):
                if x == 8:
                    formattedBlock += " "
                formattedBlock += readBlockList[x] + " "

            # ascii text
            byteList = [rawBytes[i:i + 2] for i in range(0, len(rawBytes), 2)]
            for byte in byteList:
                try:
                    if 32 <= int(byte, 16) < 127:
                        asciiString += chr(int(byte, 16))
                    else:
                        asciiString += "."
                except ValueError:
                    asciiString += "."

            # offset, line formatting, last line spacing (to many magic numbers...)
            hexDumpLine = format(offset, '08x') + "  " + formattedBlock + " |" + asciiString + "|"
            if len(hexDumpLine) is 77:  # what the length of the line should be
                print(hexDumpLine)
            else:  # fixes spacing if the line is not what its supposed to be.
                hexDumpLineShort = len(format(offset, '08x') + " " + formattedBlock)
                spacingAmount = 59 - hexDumpLineShort
                hexDumpLine = format(offset, '08x') + "  " + formattedBlock + (" " * spacingAmount) + "|" + asciiString + "|"
                print(hexDumpLine)
            asciiString = ""
            offset += 16
        if bytesInFile > 0:
            print(format(bytesInFile, '08x'))


def main():
    hexdump(sys.argv[1])


if __name__ == "__main__":
    main()

