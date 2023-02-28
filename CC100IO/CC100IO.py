#Authors
#Konrad Holsmoelle <konrad.holsmoelle@wago.com>
#Bjarne Zaremba <bjarne.zaremba@wago.com>
#Tobias Pape <tobias.pape@wago.com>
#Tobias Schaekel <tobias.schaekel@wago.com>
#Mattis Schrade <mattis.schrade@wago.com>
#Bekim Imrihor <bekim.imrihor@wago.com>
#Nele Stocksmeyer <nele.stocksmeyer@wago.com>
#Sascha Hahn <sascha.hahn@wago.com> 
#Ansteuern der Ein- und Ausgaenge aus https://github.com/WAGO/cc100-howtos/blob/main/HowTo_Access_Onboard_IO/accessIO_CC100.py

import time
import logging
#Funktionen zum Ansteuern und Auslesen der Ein- und Ausgaenge
def digitalWrite(value, output):
    """
    value: Value which the selected output should be set to
    output: Digital output to be switched
    Function switches the output to the specified value.
    Function does not check the current value of the output
    Function returns True if value is written, returns False if an error occured
    """
    # Reading the outputs current state to calculate the new value in the file
    path ="/home/ea/dout/DOUT_DATA"
    file = open(path, "r")
    currentValue = int(file.read())
    file.close()

    # Addition or rather subtraction to the current state to switch the corresponding output
    # Least Significant Bit corresponds to digital output 1, the 4th bit corresponds to output 8
    # A number from 0 to 15 is written to the file
    if output == 1:
        if value:
            currentValue += 1
        else:
            currentValue -= 1
    elif output == 2:
        if value:
            currentValue += 2
        else:
            currentValue -= 2
    elif output == 3:
        if value:
            currentValue += 4
        else:
            currentValue -= 4
    elif output == 4:
        if value:
            currentValue += 8
        else:
            currentValue -= 8
    else:
        logging.warning("Output is false")

    # Writes the calculated value for the new configuration to the file on the CC100
    file = open(path, "w")
    file.write(str(currentValue))
    file.close()
    # Returns True after completion
    return True


def analogWrite(voltage, output):
    """
    voltage: Voltage which the selected output should be set to
    output: Analog output to be switched
    Function switches the output to the specified voltage
    Function does not check the current value of the output
    Function returns True if value is written, returns False if an error occured
    """
    if (voltage>0 and voltage <10000):
        voltage = calibrateOut(voltage, output)
    if voltage < 0:
        voltage = 0

        # Activates the analog outputs on the CC100
        path = "/home/ea/anout/40017000.dac:dac@1/iio:device0/out_voltage1_powerdown"
        file = open(path, "w")
        file.write("0")
        file.close()

        path = "/home/ea/anout/40017000.dac:dac@2/iio:device1/out_voltage2_powerdown"
        file = open(path, "w")
        file.write("0")
        file.close()

        # Writes the voltage, taken from the calibration for the corresponding output,
        # for the voltage to the file for the output
        # When turning off, zero is written to the file
        if output == 1:
            path="/home/ea/anout/40017000.dac:dac@1/iio:device0/out_voltage1_raw"
            file = open(path, "w")
            file.write(str(voltage))
            file.close()

        elif output == 2:
            path="/home/ea/anout/40017000.dac:dac@2/iio:device1/out_voltage2_raw"
            file=open(path, "w")
            file.write(str(voltage))
            file.close()
            
        # Returns True after completion
        return True

def digitalRead(input):
    """
    input: Digital input to be switched
    Function reads the input
    Function does not check the current value of the output
    Returns True or False depending on the value
    """

    # Reads the state of the digital inputs on the CC100
    path = "/home/ea/din/din"
    datei = open (path, "r")
    value = datei.readline()
    datei.close()

    # Formats the current state into an 8-digit binary code
    value = int(value)
    value0B = format(value, "08b")

    # Calculates the position of the bit from the desired input
    inputBit = 8 - input

    # Returns the value of the state of the desired input
    # Note: Last index(read from left to right) ist the Least Significant Bit.
    if int(value0B[inputBit]) == 1:
        return True
    else:
        return False

def digitalReadWait(input, value):
    """
    input: Digital input to be checked
    value: State to be queried at the input
    Reads the specified input until the desired state is reached,
    by another Function or external factors and then returns True
    Function runs until the state is reached.
    """

    # Converts the given bool into a number
    if value:
        value = 1
    else:
        value = 0

    # Checks the input as long as it reaches the given state
    # Then ends the loop and returns True
    loop_condition = True
    while loop_condition:
        if digitalRead(input) == value:
            loop_condition = False
            return True

def analogRead(input):
    """
    input: Analog input to be switched
    Function reads the input and returns the calibrated value in mV as an Integer.
    """

    # Reads the state of the analog input on the CC100
    if input == 1:
        path="/home/ea/anin/48003000.adc:adc@100/iio:device3/in_voltage3_raw"
    elif input == 2:
        path="/home/ea/anin/48003000.adc:adc@100/iio:device3/in_voltage0_raw"

    file = open(path, "r")
    voltage = int(file.readline())
    file.close()

    return(calibrateIn(voltage, input))

def delay(iTime):
    iTime = iTime/1000
    time.sleep(iTime)

def tempRead(input):
    """
    input: PT input to be switched
    Function reads the input and returns the calibrated value in °C as an Integer.
    """
    
    if input == "PT1":
        path="/sys/bus/iio/devices/iio:device2/in_voltage13_raw"
    elif input == "PT2":
        path="/sys/bus/iio/devices/iio:device2/in_voltage1_raw"
    
    file = open(path, "r")
    voltage = int(file.readline())
    file.close()

    # Calibrates the value and returns it
    return(calibrateTemp(voltage, input))
    
# Output calibration from: https://github.com/WAGO/cc100-howtos/blob/main/HowTo_Access_Onboard_IO/accessIO_CC100.py
def readCalibriationData():
    """
    Reads out the data of the calibrationdata from the CC100
    """
    global calib_data
    filename="/home/ea/cal/calib"
    
    file = open(filename, "r")
    
    calib_data = file.readlines()[1:]    
    file.close()

def getCalibrationData(value):
    """
    Returns the calibrationdata for the required row of the table
    """
    return calib_data[value].rstrip().split(' ', 4)

def calcCalibrate(val_uncal, calib):
    """
    Calcutes the value of the voltage for the required output
    """
    x1=int(calib[0])
    y1=int(calib[1])
    x2=int(calib[2])
    y2=int(calib[3])

    val_cal=(y2-y1)*int(val_uncal-x1)
    val_cal=val_cal/(x2-x1)
    val_cal=val_cal+y1

    return int(val_cal)

def calibrateOut(iVoltage, iOutput):
    """
    iVoltage: Voltage to be applied to the input
    iOutput: Output which should be switched

    Returns the value which is to be written with the specified voltage
    """
    
    readCalibriationData()
    # Takes a different set of calibration data depending on the output
    if iOutput == 1:
        cal_ao = getCalibrationData(4)
    elif iOutput == 2:
        cal_ao = getCalibrationData(5)
    # Calculates and returns the value
    return calcCalibrate(iVoltage, cal_ao)

def calibrateIn(iValue, iInput):
    """
    iValue: Value given for the file from the output
    iInput: Input at which the value was read
    """
    readCalibriationData()
    if iInput == 1:
        cal_ai = getCalibrationData(2)
    if iInput == 2:
        cal_ai = getCalibrationData(3)
    #Returns the calculated value 
    return calcCalibrate(iValue, cal_ai)

def calibrateTemp(iValue, iInput):
    """
    iValue: Value given for the file from the output
    iInput: Input at which the value was read
    """
    readCalibriationData()
    if iInput == "PT1":
        cal_Temp = getCalibrationData(0)
    if iInput == "PT2":
        cal_Temp = getCalibrationData(1)
    #Returns the calculated value in °C
    return (calcCalibrate(iValue, cal_Temp)-1000)/(3.91)
