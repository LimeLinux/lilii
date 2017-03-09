#
#
#  Copyright 2017 Metehan Özbek <mthnzbk@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from PIL import ImageDraw, Image
from .parted import *
import os


def mbToGB(size):
    if size < 1024:
        return str(size)+" MB"
    else:
        return str(int(size)//1024)+" GB"


def imageCrop(image):
    width, height = image.size

    if width > height:
        x, y, w, h = ((width - height) // 2), 0, height + ((width - height) // 2), height
        return x, y, w, h

    else:
        x, y, w, h = ((height - width) // 2), 0, width, width + ((height - width) // 2)
        return x, y, w, h


def avatarCreate(image):
    image = image.convert("RGBA")
    width, height = image.size

    im = Image.new("RGBA", image.size, (255, 255, 255, 0))
    paint = ImageDraw.Draw(im)
    paint.ellipse((0, 0, width, height), fill=(0, 0, 0, 255), outline=(0, 0, 0, 255))

    avatar = Image.new("RGBA", image.size, (0, 0, 0, 0))
    avatar.paste(image, mask=im)

    return avatar


def is_efi():
    return os.path.isdir("/sys/firmware/efi")