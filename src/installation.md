# Installation

This is the minimum required software for the xpcc build system:

- [Python 2.7.x](http://www.python.org/)
- [Software Construct](http://www.scons.org/)
- [Jinja2 Template Engine](http://jinja.pocoo.org/)
- AVR toolchain: [avr-gcc](http://www.nongnu.org/avr-libc) and [avrdude](http://www.nongnu.org/avrdude)
- ARM toolchain: [arm-none-eabi-gcc](https://launchpad.net/gcc-arm-embedded) and [openocd](http://openocd.sourceforge.net/)

To start actively developing on xpcc, you will also need these packages:

- [python-lxml](http://lxml.de/)
- [doxygen](http://www.stack.nl/~dimitri/doxygen)


## Installing on Linux

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


## Installing on OS X

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


## Installing on Windows

We're sorry, we do not have enough experience with Windows to provide
honest support.
[Pull requests welcome!](https://github.com/roboterclubaachen/xpcc/pulls)

[examples]: https://github.com/roboterclubaachen/xpcc/tree/develop/examples
