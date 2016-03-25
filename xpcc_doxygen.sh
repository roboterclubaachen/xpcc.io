#!/usr/bin/env sh

# build ATtiny85
cd xpcc/examples/avr/gpio/basic/
scons

# build ATmega328p
cd ../blinking/
scons

# build the STM32F407
cd ../../../stm32f4_discovery/blink/
scons

# build the documenation
cd ../../../
scons doc

# copy the xpcc doc to the right place
cd ../
cp -r xpcc/doc/build/api site/
