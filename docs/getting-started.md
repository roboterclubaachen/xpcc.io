# Getting started

Get the source code is by cloning the repository:

	git clone https://github.com/roboterclubaachen/xpcc.git


## Quickstart

If you just want to try out xpcc, we provide you with a [configured headless
virtual machine](https://github.com/roboterclubaachen/rca-vm/) so you only
need to install [Virtualbox](https://www.virtualbox.org/wiki/Downloads) and
[Vagrant](http://www.vagrantup.com/downloads.html) on your system.

	cd xpcc
	vagrant up
	vagrant ssh

Vagrant will download the virtual machine, import it into VirtualBox and boot
it, before logging into to it. There will be a shared folder located at
`/vagrant` which contains the xpcc source code on your local file system.
This means you can use an editor of your choice to view and edit the source
code, and then use the virtual machine to compile it.

So if you have an Arduino Uno lying around, you can then compile and program
the [LED blinking example](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/arduino_uno/basic/blink/main.cpp):
```
cd /vagrant/examples/arduino_uno/basic/blink/
scons program
[...]
AVR Memory Usage
----------------
Device: atmega328p

Program:     192 bytes (0.6% used)
(.data + .text)

Data:          0 bytes (0.0% used)
(.bss + .data + .noinit)
```

You can compile and program every other example the same way.
Here is the output of the STM32F4 Discovery Board [LED blinking example](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/stm32f4_discovery/blink/main.cpp):
```
cd /vagrant/examples/stm32f4_discovery/blink/
scons program
[...]
Memory Usage
------------
Device: stm32f407vg

Program:    1980 bytes (0.2% used)
(.data + .fastdata + .reset + .rodata + .text)

Data:       3352 bytes (1.7% used) = 24 bytes static (0.0%) + 3328 bytes stack (1.7%)
(.bss + .data + .fastdata + .noinit + .stack)

Heap:     131060 bytes (66.7% available)
(.heap1 + .heap2 + .heap3)
```

## Basic APIs

All of this code works the same on all platforms, however, the pin and module names may need to be adapted.

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

stream << 24 << " is a nice number!" << xpcc::endl;
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

## Toolchain installation

Compiling the code in our virtual machine can be slower than compiling it
natively. To install the toolchain on your system, this is the
minimum required software for the xpcc build system:

- [Python 2.7.x](http://www.python.org/)
- [Software Construct](http://www.scons.org/)
- [Jinja2 Template Engine](http://jinja.pocoo.org/)
- AVR toolchain: [avr-gcc](http://www.nongnu.org/avr-libc) and [avrdude](http://www.nongnu.org/avrdude)
- ARM toolchain: [arm-none-eabi-gcc](https://launchpad.net/gcc-arm-embedded) and [openocd](http://openocd.sourceforge.net/)

To start actively developing on xpcc, you will also need these packages:

- [python-lxml](http://lxml.de/)
- [doxygen](http://www.stack.nl/~dimitri/doxygen)


### Installing on Linux

For Ubuntu 14.04LTS, these commands install the basic build system:

	sudo apt-get install python python-jinja2 scons git

Install the AVR toochain:

	sudo apt-get install gcc-avr binutils-avr avr-libc avrdude

And the ARM toolchain as well:

	sudo add-apt-repository ppa:team-gcc-arm-embedded/ppa
	sudo apt-get update
	sudo apt-get install gcc-arm-embedded openocd

To compile programs for x86 systems install the following packets:

	sudo apt-get install gcc build-essential libboost-thread-dev \
	                     libboost-system-dev libasio-dev

For active xpcc development install these packets too:

	sudo apt-get --no-install-recommends install doxygen
	pip install --user lxml

This installs `doxygen` without LaTeX support, which saves ~600MB of disk space.


### Installing on OS X

First install [`homebrew`](http://mxcl.github.com/homebrew/), a great packet
manager for OSX, then use it to install the minimum build system:

	brew install python scons git
	pip install --user jinja2

Install the AVR toochain:

	brew tap osx-cross/avr
	brew install avr-libc avrdude

And the ARM toolchain as well:

	brew tap ARMmbed/homebrew-formulae
	brew install arm-none-eabi-gcc

To program and debug your Cortex-M device, you need to install the latest
[OpenOCD](http://openocd.org) version:

	brew install openocd --HEAD --enable-ft2232_libftdi \
	                     --enable-jlink --enable-stlink

 For active xpcc development install these packets too:

	brew install doxygen
	pip install --user lxml


### Installing on Windows

We're sorry, but since we do not have enough experience with Windows to provide
honest support, we recommend the use of our virtual machine.
Pull requests welcome!

[examples]: https://github.com/roboterclubaachen/xpcc/tree/develop/examples
