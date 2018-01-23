# Installation

This is the minimum required software for the xpcc build system:

- [Python 3](http://www.python.org/)
- [Software Construct](http://www.scons.org/)
- [Jinja2 Template Engine](http://jinja.pocoo.org/)
- AVR toolchain: [avr-gcc](http://www.nongnu.org/avr-libc) and [avrdude](http://www.nongnu.org/avrdude)
- ARM toolchain: [arm-none-eabi-gcc](https://launchpad.net/gcc-arm-embedded) and [openocd](http://openocd.org/)

To start actively developing on xpcc, you will also need these packages:

- [python-lxml](http://lxml.de/)
- [doxygen](http://www.stack.nl/~dimitri/doxygen)

Note that xpcc requires C++14, so you need a reasonably new compiler (at least GCC 5).

*Please help us keep these instructions up-to-date by [opening a Pull Request](https://github.com/roboterclubaachen/xpcc.io/pulls)!*

## Installing on Linux

For Ubuntu 16.04LTS, these commands install the basic build system:

	sudo apt-get install python python-pip python-jinja2 scons git

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

First install [`homebrew`](http://brew.sh/), a great packet
manager for OS X, then use it to install the minimum build system:

	brew install python3 scons git
	pip3 install --user jinja2 future
	# Unless you use virtualenv (which you should!)
	# you may need to default your python to python3
	# ln -s /usr/local/bin/python3 /usr/local/bin/python

Install the [upstream (!) AVR toolchain](https://github.com/osx-cross/homebrew-avr):

	brew tap osx-cross/avr
	brew install avr-gcc

And the [official ARM toolchain](https://github.com/armmbed/homebrew-formulae) as well:

	brew tap ARMmbed/formulae
	brew install arm-none-eabi-gcc

To program and debug your ARM Cortex-M device, you need to install the latest
[OpenOCD](http://openocd.org) version:

	brew install openocd --HEAD

 For active xpcc development install these packets too:

	brew install doxygen
	pip install --user lxml


## Installing on Windows

First thing you need is Python 2.7. On Windows it is strongly recommended to use a Python enviroment manager instead of plain Python/pip, e.g. Anaconda.

### Installation with Anaconda
First we create a new Python 2.7 enviroment and install all nescessary packages.

    conda create --name xpcc python=2.7
    activate xpcc
    conda install -c conda-forge jinja2 scons git

For now you will also need the following packages:

    conda install -c conda-forge configparser future

For ARM development you will need the Windows 32-bit build of the [GNU Arm Embedded Toolchain](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads). The binary sources of this toolchain (.../bin) have to be added to your PATH variable.

For programming and debugging ARM Cortex-M devices you will also need prebuild [OpenOCD binaries](http://gnutoolchains.com/arm-eabi/openocd/). The binary sources (.../bin) have to be added to your PATH variable as well.

### Current bugs
As for now, you cant use project and build paths, that contain non-ASCII characters (ä,ö, ...), since they are not parsed correctly.

[examples]: https://github.com/roboterclubaachen/xpcc/tree/develop/examples