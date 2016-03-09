# Getting started

## Examples

The best way for you to quickly learn about xpcc's APIs is to look at and experiment with [our examples][examples], especially if you have a development board that xpcc [supports out-of-the-box](../#supported-hardware).
Make sure you have either our [virtual machine or the native toolchain installed](../installation).

Here are our favorite examples for our supported development boards:

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

- [SSD1306 OLED display](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/oled_display/main.cpp): Draws text and graphics onto I2C display.
- [BMP085/BMP180 barometer](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/barometer_bmp085_bmp180/main.cpp): Reads atmospheric pressure and temperature from I2C sensor.
- [VL6180 time-of-flight distance sensor](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/distance_vl6180/main.cpp): Reads distance and ambient light from I2C sensor.
- [TCS3414 color sensor](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/colour_tcs3414/main.cpp): Reads RGB color from I2C sensor.
- [HD44780 over I2C-GPIO expander](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/display/hd44780/main.cpp): Draws text via native GPIO port or I2C-GPIO expander port onto character display.

Have a look at [the build system commands](../reference/build-system/#build-commands) to see how
to compile and program your targets.

## Your own project

Start your own project by cloning [our `getting-started` project][getting-started] from GitHub:

```sh
git clone --recursive https://github.com/roboterclubaachen/xpcc-getting-started.git
cd xpcc-getting-started
tree
.
├── Readme.md
├── Vagrantfile
├── hello-world
│   ├── SConstruct
│   ├── main.cpp
│   └── project.cfg
└── xpcc (git submodule)
```

The example contains the xpcc framework as a git submodule, a `Vagrantfile`
to enable use of [our virtual machine](../installation/#virtual-machine),
a `SConstruct` file for our build system, a project configuration file and
the source code of course:

```cpp
#include <xpcc/architecture/platform.hpp>

using Led = Board::Led1;

int main()
{
    Board::initialize();

	Led::setOutput(xpcc::Gpio::Low);

	while (1)
	{
		Led::toggle();
		xpcc::delayMilliseconds(500);
	}
	return 0;
}
```

```ini
[build]
target = stm32f4discovery

[parameters]
uart.stm32.3.tx_buffer = 2048
uart.stm32.3.rx_buffer = 256

[defines]
YOUR_AMAZING_DEFINE = 42
```

When you create you own project, you need to adapt the `xpccpath` inside the
`SConstruct` to point to the location of the xpcc framework.
Note that this allows you to use different xpcc frameworks (your own fork?) for
different projects.

```python
# path to the xpcc root directory (modify as needed!)
xpccpath = '../xpcc'
# execute the common SConstruct file
execfile(xpccpath + '/scons/SConstruct')
```




[getting-started]: https://github.com/roboterclubaachen/xpcc-getting-started
[examples]: https://github.com/roboterclubaachen/xpcc/tree/develop/examples
