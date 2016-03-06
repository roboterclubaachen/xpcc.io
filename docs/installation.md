# Installation

## Virtual machine

If you just want to try out xpcc or do not want to install the build tools on
your machine just yet, we provide you with a [configured headless
virtual machine](https://github.com/roboterclubaachen/rca-vm/) running Ubuntu
14.04LTS with all the build tools installed.

You only need to install [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
and [Vagrant](http://www.vagrantup.com/downloads.html) on your system, and can
then easily boot the VM and ssh into it:

	git clone https://github.com/roboterclubaachen/xpcc.git
	cd xpcc
	vagrant up
	vagrant ssh

Vagrant will download the virtual machine (~1.2GB), import it into VirtualBox
and boot it, before logging into to it. There will be a shared folder located
at `/vagrant` which contains the xpcc source code on your local file system.
This means you can use an editor of your choice to view and edit the source
code on you native OS, and then use the virtual machine to compile it.

So if you have an Arduino Uno lying around, you can then compile and program
the [LED blinking example](https://github.com/roboterclubaachen/xpcc/blob/develop/examples/arduino_uno/basic/blink/main.cpp):
```sh
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
```sh
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


## Native installation

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
manager for OS X, then use it to install the minimum build system:

	brew install python scons git
	pip install --user jinja2

Install the AVR toochain:

	brew tap larsimmisch/avr
	brew install avr-libc avrdude

And the ARM toolchain as well:

	brew tap ARMmbed/homebrew-formulae
	brew install arm-none-eabi-gcc

To program and debug your ARM Cortex-M device, you need to install the latest
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
