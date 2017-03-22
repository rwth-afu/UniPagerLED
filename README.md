# UniPagerLED
Front panel status LED

A software that connects to the websocket interface of RustPager and controls front panel LED with function
* UniPager running (means Websocket connection is up and running)
* Connected to DAPNET-Core
* Transmitting

Configuration parameters on the command line are be:
* Websocket Hostname (Default: localhost) --hostname
* Websocket Port (Default: 8055) --port
* GPIO Pin in Wiring Pi style for "Running LED"  --gpioRun
* GPIO Pin in Wiring Pi style for "Connected LED" --gpioConn
* GPIO Pin in Wiring Pi style for "Transmitting LED" --gpioTX
* For all GPIOs an seperate invert option to be flexible if the LEDs common Pin is Ground or 3.3V. Maybe by putting a __-__ in front of the pin number; e.g. --gpioTX -29

Websocket connection should be opened once and kept open. React on update comming from the UniPager. If connection is closed, reconnect.

Packages needed for the Python Program:
* sudo apt install python3 python3-websocket
