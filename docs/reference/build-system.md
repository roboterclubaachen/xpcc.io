# Build system

xpcc uses the [SCons build system][scons] to generate, build and program your application.
We've extended it with many utilities to allow a smooth integration of embedded tools.

## Build commands

You can use these command in all our examples to get a feel of how it works.

### Common

- `build`: Generates the HAL and compiles your program into an executable.
- `size`: Displays the static Flash and RAM consumption.
- `program`: Writes the executable onto your target.
<!-- - `doc`: Generates the doxygen documentation for xpcc with your configuration. -->

By default `scons` executes `scons build size`.

- `listing`: Decompiles your executable into an annotated assembly listing.
- `symbols`: Displays the symbol table for your executable.
- `-c`: Cleans the project's build files.
- `verbose=1`: Makes the printout more verbose.


### AVR only:

- `fuse`: Writes the fuse bits onto your target.
- `eeprom`: Writes the EEPROM memory onto your target.

### ARM Cortex-M only:

- `debug`: Starts the GDB debug session of your current application in text UI mode.  
           You must execute `openocd-debug` or `lpclink-debug` before running this command!
- `openocd-debug`: Starts the OpenOCD debug server for your target.
- `lpclink-debug`: Starts the LPC-Link debug server for your target.
- `lpclink-init`: Initialize the LPC-Link with its proprietary firmware.

## Project configuration

Your `project.cfg` file contains configuration information for your target.
For the device identify naming scheme, see the [Device File reference](../reference/device-files/#device-identifier).

```ini
[build]
# use a predefined board config file from xpcc/architecture/platform/board/
# it defines the configuration for a board, which you can overwrite here.
board = stm32f4_discovery

# declare the name of your project. Default is enclosing folder name.
name = blinky
# the target of your project, use the full name of the device here
device = stm32f407vg
# AVR only: declare the clock frequency in Hz
clock = 16000000
# overwrite the default `./build/` folder path
buildpath = ../../build/${name}

# parametrize HAL drivers here, see section on Parameters
[parameters]
uart.stm32.3.tx_buffer = 2048
uart.stm32.3.rx_buffer = 256

# AVR only: declare fuse bits for use with  $ scons fuse
[fusebits]
# only the fuses declared here are written
efuse = 0x41
hfuse = 0x42
lfuse = 0x43

# AVR only: configure avrdude for  $ scons program
# Consult the avrdude documentation for options.
[avrdude]
# using the AVR ISP mk2 programmer
port = usb
programmer = avrispmkII
# or using a serial bootloader
port = /dev/ttyUSB0
programmer = arduino
# baudrate only required for serial bootloaders
baudrate = 115200

# ARM only: configure OpenOCD for  $ scons program
[openocd]
# OpenOCD has predefined configs in its searchpaths
configfile = board/stm32f4discovery.cfg
# but you can also use your own special config file
configfile = openocd.cfg
# the commands to run on  $ scons program. Defaults are:
commands =
	init
	reset halt
	flash write_image erase $SOURCE
	reset run
	shutdown

# LPC targets with LPC-Linkv2 programmer only
[lpclink]
# base path of the lpcxpresso installation
# Default on Linux: /opt/lpcxpresso/
# Default on OS X: /Applications/lcpxpresso_*/ (first match)
basepath = ../lpcxpresso
```

### Parameters

In order to customize drivers further, driver parameters may be declared.
These follow the naming scheme `type.name.instance.parameter` and are restrictive in the values they accept. Here is an overview of the available parameters.

Set the software queue size for CAN messages for peripheral instance `N` in addition to the hardware queues:

- `can.stm32.N.tx_buffer ∈ [0,254] = 32`
- `can.stm32.N.rx_buffer ∈ [0,254] = 32`

Sets the main stack size. Note that the linkerscript may increase this to satisfy alignment requirements, especially with the vector table mapped to RAM. Default size is `3kB - 32B`.

- `core.cortex.0.main_stack_size ∈ [512, 8192] = 3040`

Places the vector table in RAM. When your stack and interrupt vector table reside in the _same_ RAM section, this will _increase_ interrupt response time! The default setting is the fastest setting.

- `core.cortex.0.vector_table_in_ram ∈ bool = false (true on STM32F3/STM32F7)`

Enables the blinking LED inside the hard fault handler.
Use this feature to easily identify a crashed processor!

- `core.cortex.0.enable_hardfault_handler_led ∈ bool = false`
- `core.cortex.0.hardfault_handler_led_port ∈ {A,B,C,D,E,F,G,H,I,J,K}`
- `core.cortex.0.hardfault_handler_led_pin ∈ [0,15]`

Enables the serial logger inside the hard fault handler.
Use `basic` for a minimal failure trace or `true` for a complete trace.
You must provide the peripheral instance of the used serial port as well as a `XPCC_LOG_ERROR` output stream!

- `core.cortex.0.enable_hardfault_handler_log ∈ {false,basic,true} = false`
- `core.cortex.0.hardfault_handler_uart ∈ [1,8]`

Sets the size of the transaction buffer for peripheral instance `N`.
Increase this if you have many connected I2C slaves.

- `i2c.stm32.N.transaction_buffer ∈ [1,100] = 8`

Forces the SPI driver on AVRs to poll for transfer completion rather than to delegate execution back to the main loop. Enabling this only makes sense for very high SPI frequencies.

- `spi.at90_tiny_mega.0.busywait ∈ bool = false`

Set the software buffer for UART data for peripheral instance `N`.
The size is limited on AVRs, due to atomicity requirements!

- `uart.at90_tiny_mega.N.tx_buffer ∈ [1,254] = 64`
- `uart.at90_tiny_mega.N.rx_buffer ∈ [1,254] = 8`

- `uart.lpc.0.tx_buffer ∈ [1,65534] = 250`
- `uart.lpc.0.rx_buffer ∈ [1,65534] = 16`

- `uart.stm32.N.tx_buffer ∈ [1,65534] = 250`
- `uart.stm32.N.rx_buffer ∈ [1,65534] = 16`


[scons]: http://www.scons.org/
