# The MIT License (MIT)
#
# Copyright (c) 2020 Alethea Flowers for Winterbloom
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""A driver for the Analog Devices AD5687(R) 16-bit Digital to Analog Converter."""

from winterbloom_ad_dacs import _common


class _Commands:
    DAC_A = 0b0001
    DAC_B = 0b0010
    DAC_C = 0b0100
    DAC_D = 0b1000


class AD5686(_common.AD568x):
    """A driver for the Analog Devices AD5686(R) Digital to Analog Converter.

    This is a 4-channel analog to digital converter. The driver provides each
    channel as a separate AnalogOut-compatible interface.

    Typical usage::

        dac = ad5686.create_from_pins(
            cs=board.D3)
        dac.reset()
        dac.a.value = 15000
        dac.b.value = 0
        dac.c.value = 65355
        dac.d.value = 0

    """

    def __init__(self, spi_device):
        """
        Args:
            spi_device (adafruit_bus_device.spi_device.SPIDevice): The SPI device where
                the DAC is connected.
        """
        super().__init__(spi_device)
        self.a = _common.AnalogOut(self, _Commands.DAC_A)
        self.b = _common.AnalogOut(self, _Commands.DAC_B)
        self.c = _common.AnalogOut(self, _Commands.DAC_C)
        self.d = _common.AnalogOut(self, _Commands.DAC_D)


create_from_pins = AD5686.create_from_pins
