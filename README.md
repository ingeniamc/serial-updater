# README #

Updater tool for summit drives with serial based communication (UART, RS422, RS485, USB)


### How it works ###
    updater.py -c COM1 -i everest.mfu [-n 10] [-sn 1]

### How to generate updater outputs ###



    #!bash
    
    pyinstaller updater.py -c -F
