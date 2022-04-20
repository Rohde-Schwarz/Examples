# This example show how to operate an instrument that needs special settings - R&S HM8118
# The instrument requires a non-standard termination character (carriage return) and a delay before each write and read operation

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.22.0.79')
instr = RsInstrument("ASRL4::INSTR", True, False, "TerminationCharacter='\r', WriteDelay=200, ReadDelay=0")
instr.write_str("*RST")
idn = instr.query_str('*IDN?')
print(f"\nHello, I am: '{idn}'")

instr.close()
