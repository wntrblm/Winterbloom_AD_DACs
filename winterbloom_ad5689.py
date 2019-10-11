# The MIT License (MIT)
#
# Copyright (c) 2019 Alethea Flowers for Winterbloom
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

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/theacodes/Winterbloom_CircuitPython_AD5689.git"

"""A driver for the Analog Devices AD5689(R) 16-bit Digital to Analog Converter.

AD5689 wiring expectations (TSSOP-16 package):

* 1: AD5689 = Vref, AD5689R = NC (uses internal reference)
* 2: NC
* 3: Analog output A
* 4: GND
* 5: VDD
* 6: NC
* 7: Analog output B
* 8: NC (optionally can use as serial out for daisy chaining)
* 9: GND (optionally can use as LDAC switch, but the driver doesn't use it)
* 10: GND (optionally can use as GAIN)
* 11: VDD (logic voltage)
* 12: SCLK - connect to board.SCK for hardware SPI or any digital
    pin for bitbang IO.
* 13: CS - connect to any digital pin.
* 14: MOSI - connect to board.MOSI for hardware SPI or any digital
    pin for bitbang IO.
* 15: VDD (optionally can use as hardware reset pin, but the driver doesn't use it)
* 16: GND (optionally can use as reset selection)

"""

import board
import busio
import digitalio
from adafruit_bus_device.spi_device import SPIDevice


class _Commands:
    SOFT_RESET = 0b01100000
    WRITE_AND_UPDATE_DAC = 0b00110000
    DAC_A = 0b0001
    DAC_B = 0b1000


class _AnalogOut:
    """Implements the CircuitPython AnalogIO.AnalogOut interface for this
    driver. You can set the channel's value using ``.value``."""

    def __init__(self, driver, channel):
        self._driver = driver
        self._channel = channel

    def _set_value(self, value):
        """Set the 16-bit integer value."""
        return self._driver._set_channel(self._channel, value)

    value = property(None, _set_value)

    def _set_normalized_value(self, value):
        """Set the 16-bit integer value."""
        if value < 0.0:
            value = 0
        if value > 1.0:
            value = 1
        return self._driver._set_channel(self._channel, int(value * 65535))

    normalized_value = property(None, _set_normalized_value)


class AD5689:
    """A driver for the Analog Devices AD5689(R) Digital to Analog Converter.

    This is a 2-channel analog to digital converter. The driver provides each
    channel as a separate AnalogOut-compatible interface.

    Typical usage::

        dac = winterbloom_ad5689.create_from_pins(
            cs=board.D3)
        dac.reset()
        dac.a.value = 15000
        dac.b.value = 0

    """

    def __init__(self, spi_device):
        """
        Args:
            spi_device (adafruit_bus_device.spi_device.SPIDevice): The SPI device where
                the DAC is connected.
        """
        self.spi_device = spi_device
        self.a = _AnalogOut(self, _Commands.DAC_A)
        self.b = _AnalogOut(self, _Commands.DAC_B)

    @classmethod
    def create_from_pins(cls, cs, sck=board.SCK, mosi=board.MOSI, spi_cls=busio.SPI):
        """Helper constructor for creating an instance using just the pins its connected to.

        Args:
            cs: The pin connected to the DAC's SYNC input.
            sck: The pin connected to the DAC's SCLK input.
            mosi: The pin connected to the DAC's SDIN input.
            spi_cls: The class used to create the SPI interface, typically either
                ``busio.SPI`` or ``bitbangio.SPI``.
        """
        cs_io = digitalio.DigitalInOut(cs)
        cs_io.direction = digitalio.Direction.OUTPUT
        cs_io.value = True

        spi = spi_cls(sck, MOSI=mosi)
        spi_device = SPIDevice(spi, cs_io, polarity=0, phase=1)

        return cls(spi_device)

    def send_command(self, command, param1, param2):
        """Directly send a raw command to the DAC."""
        with self.spi_device:
            self.spi_device.spi.write(bytes([command, param1, param2]))

    def soft_reset(self):
        """Soft reset the DAC."""
        self.send_command(_Commands.SOFT_RESET, 0, 0)

    def _set_channel(self, channel, value):
        """Set the 16bit value for the given DAC channel."""
        cmd_byte = _Commands.WRITE_AND_UPDATE_DAC | channel
        value_msb = value >> 8
        value_lsb = value & 0xFF
        self.send_command(cmd_byte, value_msb, value_lsb)


create_from_pins = AD5689.create_from_pins
