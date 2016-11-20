# Getting started

## Examples

The best way for you to quickly learn about xpcc's APIs is to look at and experiment with [our examples][examples], especially if you have a development board that xpcc [supports out-of-the-box](../#supported-hardware).
Make sure you have [the toolchain installed](../installation).

Here are our favorite examples for our supported development boards:

- Arduino Uno:
[Blinky](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/arduino_uno/basic/blink/main.cpp),
[Button & Serial](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/arduino_uno/basic/digital_read_serial/main.cpp),
[Analog & Serial](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/arduino_uno/basic/read_analog_voltage/main.cpp).
- NUCLEO-F103RB:
[Blinky & Serial](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/nucleo_f103rb/blink/main.cpp).
- STM32F072 Discovery:
[Blinky](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f072_discovery/blink/main.cpp),
[CAN](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f072_discovery/can/main.cpp),
[Gyroscope](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f072_discovery/rotation/main.cpp).
- STM32F3 Discovery:
[Blinky](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f3_discovery/blink/main.cpp),
[CAN](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f3_discovery/can/main.cpp),
[Accelerometer](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f3_discovery/accelerometer/main.cpp),
[Gyroscope](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f3_discovery/rotation/main.cpp),
[Debugging with GDB](https://github.com/roboterclubaachen/xpcc/tree/develop/examples/stm32f3_discovery/gdb).
- STM32F4 Discovery:
[Blinky](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/blink/main.cpp),
[CAN](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/can/main.cpp),
[Accelerometer](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/accelerometer/main.cpp),
[Timer & LED Animations](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/timer/main.cpp),
[Debugging hard faults](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/hard_fault/main.cpp).
- STM32F469 Discovery:
[Blinky](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f469_discovery/blink/main.cpp),
[Drawing on display](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f469_discovery/display/main.cpp),
[Touchscreen inputs](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f469_discovery/touchscreen/main.cpp),
[Multi-heap with external 16MB memory](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f469_discovery/tlsf-allocator/main.cpp)
- STM32F769 Discovery:
[FPU with double precision](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f769i_discovery/blink/main.cpp)


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
git clone --recursive https://github.com/roboterclubaachen/getting-started-with-xpcc.git
cd getting-started-with-xpcc
tree
.
├── LICENSE
├── README.md
├── hello-world
│   ├── SConstruct
│   ├── main.cpp
│   └── project.cfg
└── xpcc (git submodule)
```

The example contains the xpcc framework as a git submodule, a `SConstruct` file for [our build system](../reference/build-system/#build-commands),
a project configuration file and of course the source code:

```cpp
#include <xpcc/architecture/platform.hpp>

int main()
{
    Board::initialize();
    Board::Leds::setOutput();

    while (1)
    {
        Board::Leds::toggle();
        xpcc::delayMilliseconds(Board::Button::read() ? 250 : 500);
#ifdef XPCC_BOARD_HAS_LOGGER
        static uint32_t counter(0);
        XPCC_LOG_INFO << "Loop counter: " << (counter++) << xpcc::endl;
#endif
    }
    return 0;
}
```

You can change the development board for which you want to compile the example
for in the `project.cfg` file:

```ini
[build]
board = stm32f4_discovery
#board = arduino_uno
#board = nucleo_f103rb
#board = stm32f072_discovery
#board = stm32f1_discovery
#board = stm32f3_discovery
#board = stm32f429_discovery
#board = stm32f469_discovery
#board = stm32f7_discovery
```

When you create you own project, you need to adapt the `xpccpath` inside the
`SConstruct` to point to the location of the xpcc framework.
Note that this allows you to use different versions of the xpcc frameworks
(your own fork?) for your projects.

```python
# path to the xpcc root directory (modify as needed!)
xpccpath = '../xpcc'
# execute the common SConstruct file
execfile(xpccpath + '/scons/SConstruct')
```

## Show me the basics

All of this code works the same on all platforms, however, the pin and module
names may need to be adapted.

### GPIO

```cpp
using Led = GpioOutputB0;
Led::setOutput();
Led::set();    // 1 instruction on AVR
Led::reset();  // 3 instructions on Cortex-M
Led::toggle();

using Button = GpioInputB0;
Button::setInput(Gpio::InputType::PullUp);
bool state = Button::read();
```

### Buffered UART

```cpp
using Uart = Uart0;
// configure and initialize UART to 115.2kBaud
GpioOutputD1::connect(Uart::Tx);
GpioInputD0::connect(Uart::Rx);
Uart::initialize<systemClock, 115200>();

Uart::write('H');  // Ohai there
Uart::write('i');

uint8_t buffer;
while(1) {
    // create a simple loopback
    if (Uart::read(buffer)) {
        Uart::write(buffer);
    }
}
```

### IOStream

```cpp
using Uart = Uart0;
// Create a IODevice with the Uart
xpcc::IODeviceWrapper<Uart> device;
xpcc::IOStream stream(device);

GpioOutputD1::connect(Uart::Tx);
Uart::initialize<systemClock, 115200>();

stream << 42 << " is a nice number!" << xpcc::endl;
```

### Software Timers

```cpp
using Led = GpioOutputB0;
xpcc::Timeout timeout(10000);   // 10s timeout
xpcc::PeriodicTimer timer(250); // 250ms period

Led::setOutput(xpcc::Gpio::High);

while(1) {
    if (timeout.execute()) {
        timer.stop();
        Led::reset();
    }
    if (timer.execute()) {
        Led::toggle();
    }
}
```

Have a look at the [`xpcc/examples/` folder][examples] for more advanced use cases.

[doxygen]: http://xpcc.io/api/modules.html
[examples]: https://github.com/roboterclubaachen/xpcc/tree/develop/examples



[getting-started]: https://github.com/roboterclubaachen/getting-started-with-xpcc
[examples]: https://github.com/roboterclubaachen/xpcc/tree/develop/examples
