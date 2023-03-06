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

## Installation
```bash
pip install CC100IO 
```

## Description of functions

* #### ```digitalWrite (value, output)``` :
  * value: Value which the selected output should be set to (True or False)
  * output: Digital output to be switched (1-4)
  * Function switches the output to the specified value.
  * Function does not check the current value of the output.
  * Function returns True if value is written, returns False if an error occured. 
* #### ```analogWrite (voltage, output)``` : 
  * voltage: Voltage which the selected output should be set to (0 - 10000 mV)
  * output: Analog output to be switched(1 or 2)
  * Function switches the output to the specified voltage. 
  * Function does not check the current value of the output. 
  * Function returns True if value is written, returns False if an error occured. 
* #### ```digitalRead (input)``` :
  * input: Digital input to be read (1-8)
  * Function reads the input. 
  * Function does not check the current value of the output. 
  * Returns True or False depending on the value.
* #### ```digitalReadWait (input, value)``` :  
  * input: Digital input to be checked (1-8)
  * value: State to be queried at the input
  * Reads the specified input until the desired state is reached, by another Function or external factors and then returns True.
  * Function runs until the state is reached.
* #### ```analogRead (input)``` :
  * input: Analog input to be read (1 or 2)
  * Function reads the input and returns the calibrated value in mV as an Integer.
* #### ```delay (iTime)``` :
  * Function makes the programm in a period of time late or slow. (in ms)
* #### ```tempRead (input)``` :
  *  input: PT input to be switched ("PT1" or "PT2")
  *  Function reads the input and returns the calibrated value in °C as an Integer.
