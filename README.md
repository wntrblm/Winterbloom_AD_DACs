# Winterbloom Analog Devices DAC drivers

This is a [CircuitPython](https://circuitpython.org) driver for the Analog Devices AD5689(R) and AD5686(R) 16-bit DACs

## Installation

Install this library by copying [winterbloom_ad_dacs](winterbloom_ad_dacs) to your device's `lib` folder.

## Connecting your device to the AD5689

The AD5689 is connected over [SPI](https://learn.adafruit.com/circuitpython-basics-i2c-and-spi/spi-devices). You should wire up the devices as follows (TSSOP-16 package):

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
* 12: SCLK - connect to `board.SCK` for hardware SPI or any digital
    pin for bitbang IO.
* 13: CS - connect to any digital pin.
* 14: MOSI - connect to `board.MOSI` for hardware SPI or any digital 
    pin for bitbang IO.
* 15: VDD (optionally can use as hardware reset pin, but the driver doesn't use it)
* 16: GND (optionally can use as reset selection)

## Example usage

```python
import board
from winterbloom_ad_dacs import ad5689

# Using hardware SPI with D3 wired to CS.
dac = ad5689.create_from_pins(
    cs=board.D3)
dac.reset()

# 16-bit values, so 0-65535
dac.a.value = 15000
dac.b.value = 0
```

## License and contributing

This is available under the [MIT License](LICENSE). I welcome contributors, please read the [Code of Conduct](CODE_OF_CONDUCT.md) first. :)