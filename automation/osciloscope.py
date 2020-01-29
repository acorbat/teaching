# -*- coding: utf-8 -*-
"""
Basic example for controlling a TBS1052B-EDU oscilloscope using USB port.

For more commands go to: https://download.tek.com/manual/TBS1000-B-EDU-TDS2000-B-C-TDS1000-B-C-EDU-TDS200-TPS2000-Programmer.pdf
Requirements
------------
pyvisa
"""
import visa
import time

# Instantiate the Resource Manager
rm = visa.ResourceManager()

# Use this command to list all the resources connected to the pc
instruments = rm.list_resources()
print(instruments)

# Choose oscilloscope in this list
osc_address = instruments[1]

# With environment executes the open magic function at the start and always
# finishes with close, avoiding leaving open communication
with rm.open_resource(osc_address) as osc:
    # The first step is to ask for identification in order to test that
    # everything is working as expected
    print("IDN: " + osc.query('*IDN?'))
    input('Press any key to continue')

    # 1) We can start by specifying something. This is done with write commands
    # Let's say we want to read the Frequency of a signal
    osc.write('MEASU:MEAS1:SOUrce CH1')
    osc.write('MEASU:MEAS1:TYPE FREQuency')
    input('Press any key to continue')

    # 2) Now we want to ask for it's value
    osc.write('MEASU:MEAS1?')
    input('Press any key to continue')
    # After asking we need to listen to the answer
    print(osc.read())

    # 5) Let's say we want the peak to peak value, and we know it's a question
    # with an answer, so we could use query command (internally it's read and
    # write)
    osc.write('MEASU:MEAS2:SOURCE CH1')
    osc.write('MEASU:MEAS2:TYPE PK2pk')
    # we should wait for the measurement to stabilize
    time.sleep(0.7)
    print("Pk2Pk: " + osc.query('MEASU:MEAS2:VAL?'))
