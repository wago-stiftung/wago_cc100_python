# CC100IO

Basic python module to control the input and output ports of a WAGO CC100.

## Contributors
- Konrad Holsmoelle <konrad.holsmoelle@wago.com>
- Bjarne Zaremba <bjarne.zaremba@wago.com>
- Tobias Pape <tobias.pape@wago.com>
- Tobias Schaekel <tobias.schaekel@wago.com>
- Mattis Schrade <mattis.schrade@wago.com>
- Bekim Imrihor <bekim.imrihor@wago.com>
- Nele Stocksmeyer <nele.stocksmeyer@wago.com>
- Sascha Hahn <sascha.hahn@wago.com> 
- Danny Meihoefer <danny.meihoefer@wago.com>

## Installation pip
```bash
pip install CC100IO 
```

## Description of functions

* ### ```digitalWrite (value, output)``` :
  * value: Value which the selected output should be set to
  * output: Digital output to be switched
  * Function switches the output to the specified value.
  * Function does not check the current value of the output.
  * Function returns True if value is written, returns False if an error occured. 
- ___analogWrite (voltage, output) :___  
  * voltage: Voltage which the selected output should be set to
  * output: Analog output to be switched
  * Function switches the output to the specified voltage. 
  * Function does not check the current value of the output. 
  * Function returns True if value is written, returns False if an error occured. 
- ___digitalRead (input) :___ 
  * input: Digital input to be switched
  * Function reads the input. 
  * Function does not check the current value of the output. 
  * Returns True or False depending on the value.
- ___digitalReadWait (input, value) :___   
  * input: Digital input to be checked
  * value: State to be queried at the input
  * Reads the specified input until the desired state is reached, by another Function or external factors and then returns True.
  * Function runs until the state is reached.
- ___analogRead (input) :___
  * input: Analog input to be switched
  * Function reads the input and returns the calibrated value in mV as an Integer.
- ___delay (iTime) :___
  * Function makes the programm in a period of time late or slow.
- ___tempRead (input) :___ 
  *  input: PT input to be switched
  *  Function reads the input and returns the calibrated value in °C as an Integer.
- ___readCalibrationData () :___
  *  Reads out the data of the calibrationdata from the CC100.
- ___getCalibrationData (value) :___
  *  Returns the calibrationdata for the required row of the table.
- ___calcCalibrate (val_uncal, calib):___
  * Calculates the value of the voltage for the required output.
- ___calibrateOut (iVoltage, iOutput) :___
  *  Returns the value which is to be written with the specified voltage.

