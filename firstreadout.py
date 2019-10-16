import serial, sys
import binascii
from bitstring import BitArray
import codecs, binascii


ser = serial.Serial()
ser.baudrate = 115200 
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=1
ser.port="/dev/ttyUSB0"
try:
    ser.open()
except:
    sys.exit ("Fout bij het openen van %s. "  % ser.name)

print(ser)

"""
49 = 
50 = (
52 = )
54 = *
5a =
5c = .

60 = 0
62 = 1
64 = 2
66 = 3
68 = 4
6a = 5
6c = 6
6e = 7
70 = 8
72 = 9
74 = :



a6 = 
a9 = 
ae = W
d0 = h
d6 = k
da = m
e6 =
"""

buffer_str = b''

#a row counter, ai ai
row = 1

while True:

    # reading byte by byte is probably very slow
    response = ser.read()
    if response:
        c = BitArray(response)
        # signal is inverted, so let's correct it
        c.invert()
     
        # more stuff to correct the output
        if buffer_str == b'T\\x02':
            buffer_str == b'0-0'
        elif buffer_str == b'LK$':
            buffer_str = b'1-0:'
        elif buffer_str == b'T\n':
            buffer_str = b'0-1'
        if c.hex != 'ff':
            # bitshifting here, one trailing 0 to many. Is the stream 7bits? 7E1?
            c1 = BitArray('0b0'+c.bin[:-1])
            buffer_str += (binascii.unhexlify(c1.hex))
        else:
            print (str(row)+"# "+str(buffer_str.decode('utf-8')))
            buffer_str = b''
            row += 1
            if row == 29:
                row = 1
        #iprint (response, c, c.bin, r.hex )
ser.close()
