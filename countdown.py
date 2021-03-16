#!/usr/bin/python3
# -*- coding:utf-8 -*-
import logging
import os
import sys
import time

from datetime import datetime
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.INFO)

basedir = Path(__file__).parent
waveshare_base = basedir.joinpath('e-Paper', 'RaspberryPi_JetsonNano', 'python')
libdir = waveshare_base.joinpath('lib')


def set_font_size(font_size):
    logging.info("Loading font...")
    return ImageFont.truetype(f"{basedir.joinpath('Bangers-Regular.ttf').resolve()}", font_size)


def countdown(now):
    piday = datetime(now.year, 3, 14)

    # Add a year if we're past PiDay
    if piday < now:
        piday = datetime((now.year + 1), 3, 14)

    days = (piday - now).days

    logging.info(f"Days till piday: {days}")
    return days


def main():

    if os.path.exists(libdir):
        sys.path.append(f"{libdir}")
        from waveshare_epd import epd2in13_V2
    else:
        logging.fatal(f"not found: {libdir}")
        sys.exit(1)

    logging.info("Starting...")
    try:
        # Create an a display object
        epd = epd2in13_V2.EPD()

        # Initialize the displace, and make sure it's clear
        # ePaper keeps it's state unless updated!
        logging.info("Initialize and clear...")
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        # Create an image object 
        # NOTE: The "epd.heigh" is the LONG side of the screen
        # NOTE: The "epd.width" is the SHORT side of the screen
        # Counterintuitive...
        logging.info(f"Creating canvas - height: {epd.height}, width: {epd.width}")
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)

        logging.info("Set text text...")
        bangers64 = set_font_size(64)
        draw.text((0, 30), 'PI DAY!', font = bangers64, fill = 0)

        logging.info("Set BMP...")
        bmp = Image.open(basedir.joinpath("img", "pie.bmp"))
        image.paste(bmp, (150,2))    

        logging.info("Display text and BMP")
        epd.display(epd.getbuffer(image))

        logging.info("Pi Date countdown; press CTRL-C to exit")
        piday_image = Image.new('1', (epd.height, epd.width), 255)
        piday_draw = ImageDraw.Draw(piday_image)

        # Set some more fonts
        bangers36 = set_font_size(36)
        bangers64 = set_font_size(64)

        # Prep for updating display
        epd.displayPartBaseImage(epd.getbuffer(piday_image))
        epd.init(epd.PART_UPDATE)

        while (True):
            days = countdown(datetime.now())
            unit = get_days_unit(days)
            
            # Clear the bottom half of the screen by drawing a rectangle filld with white
            piday_draw.rectangle((0, 50, 250, 122), fill = 255)

            # Draw the Header
            piday_draw.text((10,10), "Days till Pi-day:", font = bangers36, fill = 0)

            if days == 0:
                # Draw the Pi Day celebration text!
                piday_draw.text((0, 50), f"It's Pi Day!", font = bangers64, fill = 0)
            else:
                # Draw how many days until Pi Day
                piday_draw.text((70, 50), f"{str(days)} {unit}", font = bangers64, fill = 0)

            # Render the screen
            epd.displayPartial(epd.getbuffer(piday_image))
            time.sleep(5)


    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:    
        logging.info("Exiting...")
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)
        time.sleep(1)
        epd2in13_V2.epdconfig.module_exit()
        exit()


def get_days_unit(days):
    if days == 1:
        return "day"
    
    return "days"


if __name__ == "__main__":
    main()
