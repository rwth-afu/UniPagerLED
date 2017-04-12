# UniPagerLED
Front panel status LED

A software that connects to the websocket interface of RustPager and controls front panel LED with function
* UniPager running (means Websocket connection is up and running)
* Connected to DAPNET-Core
* Transmitting

Configuration parameters on the command line are:
* Websocket Hostname (Default: localhost) --hostname
* Websocket Port (Default: 8055) --port
* GPIO Pin for "Running LED"  --gpioRun
* GPIO Pin for "Connected LED" --gpioConn
* GPIO Pin for "Transmitting LED" --gpioTX
  * The GPIOs can be inverted to be flexible if the LEDs common Pin is Ground or 3.3V by putting a __-__ in front of the pin number; e.g. --gpioTX -29
* Presets for the LEDs for well known hardware --preset
  * --preset help gives a list of all known presets
* A config file --config
  * See comments in config.py.example

The pin header numbers have top be used, not WiringPi Numbers.

If no pin config is given it tries to guess the config based on the transmittertype supplied by the transmitter config. Currently, only the C9000 with the preset below is supported.

UniPagerLED can be installed by running ''sudo ./install.sh''. That will install
* unipagerled.py to /usr/local/bin
* config.py.example to /etc/unipagerledconfig.py
* unipagerled.service to /usr/local/lib/systemd/system/unipagerled.service

UniPagerLED can then be enabled with ''systemctl enable unipagerled'' and started with ''systemctl start unipagerled''. The configuration goes into ''/etc/unipagerledconfig.py''.

# Common assigments:
__RasPager9000:__
* gpioTX: none
* gpioRun: 24
* gpioConn: 26
* preset: c9000


Websocket connection should be opened once and kept open. React on update comming from the UniPager. If connection is closed, reconnect.

Packages needed for the Python Program:
* sudo apt install python3 python3-websocket python3-rpi.gpio
