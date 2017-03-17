# RustPagerLED
Front panel status LED

A software that connects to the websocket interface of RustPager and controls front panel LED with function
* RustPager running (means Websocket connection is up and running)
* Connected to DAPNET-Core
* Transmitting

Configuration parameters on the command line should be:
* Websocket Hostname (Default: localhost) --hostname
* Websocket Port (Default: 8055) --port
* GPIO Pin in Wiring Pi style for "Running LED"  --gpioRun
* GPIO Pin in Wiring Pi style for "Connected LED" --gpioConn
* GPIO Pin in Wiring Pi style for "Transmitting LED" --gpioTX
* For all GPIOs an seperate invert option to be flexible if the LEDs common Pin is Ground or 3.3V. Maybe by putting a __-__ in front of the pin number; e.g. --gpioTX -29

Websocket connection should be opened once and kept open. React on update comming from the Rustpager. If connection is closed, reconnect.

Libraries needed for C++ Program:
sudo apt-get install libssl-dev
sudo apt-get install libboost-all-dev
