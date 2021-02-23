## Setup

1. Enable SPI
2. Install BCM2835 C libraries
3. Install python libraries

### Enable SPI

<!-- markdownlint-disable MD014 -->
```shell
$ sudo raspi-config
```
<!-- markdownlint-enable MD014 -->

From the menu that pops up, select `Interfacing Options` -> `SPI` -> `Yes` to enable the SPI interface, then Reboot.

### Install BCM2835 libraries

Latest RN: bcm2835-1.68.tar.gz
C libraries for the Broadcom BCM 2385 chip, which handles the GPIO on the Raspberry Pis.

```shell
# Download the BCM2853 libraries and extract them
$ curl -sSL http://www.airspayce.com/mikem/bcm2835/bcm2835-1.68.tar.gz -o - | tar -xzf - 

# Change directories into the extracted code
$ pushd bcm2835-1.68/

# Configure, build, check and install the BCM2853 libraries
$ sudo ./configure
$ sudo make check
$ sudo make install

# Return to the original directory
$ popd
```

### Install required Python libraries

```shell
# Install the required Python libraries
$ sudo apt-get update
$ sudo apt-get install python3-pip python3-pil python3-numpy
$ sudo pip3 install RPi.GPIO spidev
```

<!-- markdownlint-disable MD036 -->
_Note: instruction here are for Python3.  Python 2 instructions can be found on the WaveShare website_
<!-- markdownlint-enable MD036 -->

### Download WaveShare's examples and Python libraries

```shell
# Clone the WaveShare e-Paper git repository
$ git clone https://github.com/waveshare/e-Paper.git
```

### References

* [WaveShare ePaper Setup Instructions](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT)
* [WaveShare ePaper Libraries Install Instructions](https://www.waveshare.com/wiki/Libraries_Installation_for_RPi)

## Display Something

### Get a fun Font

```shell
# The "Bangers" font is a Open Fonts License licensed font by Vernon Adams (https://github.com/vernnobile) from Google Fonts
$ mkdir fonts
$ curl -sSL https://github.com/google/fonts/raw/master/ofl/bangers/Bangers-Regular.ttf -o fonts/Bangers-Regular.ttf
```
