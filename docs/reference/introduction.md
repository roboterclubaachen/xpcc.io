# Introduction

All of this code works the same on all platforms, however, the pin and module names may need to be adapted.

See [doxygen API reference][doxygen].

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
