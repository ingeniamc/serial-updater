# README #

Updater tool for summit drives with serial based communication (UART, RS422, RS485, USB)

## Enter bootloader mode ##
Summit devices can enter in bootloader mode following the next sequence:

1. Write password **0x426F6F74** into register ***0x6DE Boot Mode***
2. Write password **0x72657365** into register ***0x6DF System reset***

In case that the application burned into the flash is corrupted and communication with the device cannot be opened, follow the [MCB start-up sequence](http://doc.ingeniamc.com/display/SS/MCB+start-up) to enter in boot mode


### Run updater ###

Once the drive is in bootloader mode, execute the next command:

    updater.py -c COM<X> -i everest.mfu [-n <Y>] [-sn <Z>]

Where:

- X is the number of the COM port where the serial to SPI bridge is connected
- Arguments -n and -sn are optional parameters and by default take the value 10 and 1 respectively
-  Y is the node of the drive
-  Z is the subnode of the drive


### How to generate executable updater outputs ###



    #!bash
    
    pyinstaller updater.py -c -F
