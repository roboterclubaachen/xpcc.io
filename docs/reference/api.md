# API reference

xpcc is a relatively large framework with many APIs and advanced concepts.

We are annotating our APIs using Doxygen and are trying to provide conceptual
design documentation on [our project blog](blog.xpcc.io).
However, this is a slow and difficult process, and the results are not perfect.

The most complete and most up-to-date API documentation is definitely the

- [Doxygen API reference][doxygen].

Unfortunately the generated HAL for our many devices confuses Doxygen.
We therefore chose to only include the HAL API for `ATtiny85`, the `ATmega328p`
and the `STM32F407vg` online.
The rest of the xpcc API is available without limitations.

## Your device

We recommend that you generate the documentation for your own device locally.

To do so, simply execute `scons doc device`, for example `scons doc stm32f303cc`.
This will build the xpcc documentation in `doc/build/stm32f303cc/`.

If you are stuck, don't hesitate to [send us an email with your questions](mailing_list).

[doxygen]: http://xpcc.io/api/modules.html
[examples]: https://github.com/roboterclubaachen/xpcc/tree/develop/examples
[mailing_list]: http://mailman.rwth-aachen.de/mailman/listinfo/xpcc-dev
