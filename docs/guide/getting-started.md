# Getting started

The best way for you to quickly learn about xpcc's APIs is to look at and experiment with [our examples][examples], especially if you have a development board that xpcc supports out-of-the-box.

Here are our favorite examples for supported development boards:

- Arduino Uno:
[Blinky](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/arduino_uno/basic/blink/main.cpp),
[Button & Serial](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/arduino_uno/basic/digital_read_serial/main.cpp),
[Analog & Serial](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/arduino_uno/basic/read_analog_voltage/main.cpp)
- NUCLEO-F103RB:
[Blinky & Serial](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/nucleo_f103rb/blink/main.cpp)
- STM32F072 Discovery:
[Blinky](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f072_discovery/blink/main.cpp),
[CAN](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f072_discovery/can/main.cpp),
[Gyroscope](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f072_discovery/rotation/main.cpp)
- STM32F3 Discovery:
[Blinky](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f3_discovery/blink/main.cpp),
[CAN](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f3_discovery/can/main.cpp),
[Accelerometer](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f3_discovery/accelerometer/main.cpp),
[Gyroscope](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f3_discovery/rotation/main.cpp),
[Debugging with GDB](https://github.com/roboterclubaachen/xpcc/tree/develop/examples/stm32f3_discovery/gdb)
- STM32F4 Discovery:
[Blinky](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/blink/main.cpp),
[CAN](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/can/main.cpp),
[Accelerometer](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/accelerometer/main.cpp),
[Timer & LED Animations](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/timer/main.cpp),
[Debugging hard faults](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/hard_fault/main.cpp),

Here are some additional examples of displays and sensors we like:

- [SSD1306 OLED display](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/oled_display/main.cpp): Draws text and graphics via I2C.
- [BMP085/BMP180 barometer](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/barometer_bmp085_bmp180/main.cpp): Reads atmospheric pressure and temperature via I2C.
- [VL6180 time-of-flight distance sensor](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/distance_vl6180/main.cpp): Reads distance and ambient light via I2C.
- [TCS3414 color sensor](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/colour_tcs3414/main.cpp): Reads RGB color via I2C.
- [HD44780 over I2C-GPIO expander](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/display/hd44780/main.cpp): Draws text via native GPIO port or I2C-GPIO expander port.


## Build system basics

xpcc uses the [SCons][] build system to generate, build and program your application.
We've extended it with many utilities to allow a smooth integration of embedded tools.

You can use these command in all our examples to get a feel of how it works.

### Common

- `build`: Generates the HAL and compiles your program into an executable.
- `size`: Displays the static Flash and RAM consumption.
- `program`: Writes the executable onto your target.

By default `scons` executes `scons build size`.

- `listing`: Decompiles your executable into an annotated assembly listing.
- `symbols`: Displays the symbol table for your executable.


### AVR only:

- `fuse`: Writes the fuse bits onto your target.
- `eeprom`: Writes the EEPROM memory onto your target.

### ARM Cortex-M only:

- `debug`: Starts the GDB debug session of your current application in text UI mode. You must execute `openocd-debug` or `lpclink-debug` in before running this command!
- `openocd-debug`: Starts the OpenOCD debug server for your target.
- `lpclink-debug`: Starts the LPC-Link debug server for your target.
- `lpclink-init`: Initialize the LPC-Link with its proprietary firmware.

## Your own project

Start your own project by forking and cloning our `blinky` project on GitHub:

```sh
git clone --recursive https://github.com/roboterclubaachen/xpcc-blinky.git
```

```
├── Vagrantfile
├── src
│   ├── SConstruct
│   ├── main.cpp
│   └── project.cfg
└── xpcc
```


```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "xpcc"
  config.vm.box_url = "http://box.xpcc.io/xpcc-vm.box"
end
```

```python
# path to the xpcc root directory (modify as needed!)
xpccpath = '../xpcc'
# execute the common SConstruct file
execfile(xpccpath + '/scons/SConstruct')
```

```ini
[general]
name = blinky

[build]
device = stm32f407vg

[parameters]
uart.stm32.3.tx_buffer = 2048
uart.stm32.3.rx_buffer = 256

[defines]
YOUR_AMAZING_DEFINE = 42

[openocd]
configfile = board/stm32f4discovery.cfg
```


```cpp
#include <xpcc/architecture/platform.hpp>
using namespace xpcc::stm32;

using Led = GpioOutputB0;

int main()
{
	Led::setOutput(xpcc::Gpio::Low);

	while (1)
	{
		Led::toggle();
		xpcc::delayMilliseconds(500);
	}
	return 0;
}
```

[scons]: http://www.scons.org/
[examples]: https://github.com/roboterclubaachen/xpcc/tree/develop/examples
