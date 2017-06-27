#!/usr/bin/env sh

rm -r xpcc/build

# build ATtiny85
(cd xpcc/examples/avr/gpio/basic/ && scons)

# build ATmega328p
(cd xpcc/examples/avr/gpio/blinking/ && scons)

# build the STM32F407
(cd xpcc/examples/stm32f4_discovery/blink/ && scons)

# build the documenation
(cd xpcc && scons doc)

# copy the xpcc doc to the right place
cp -r xpcc/doc/build/api docs/
