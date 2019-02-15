# -*- coding: utf-8 -*-

# Used as part of regex, set it with caution.
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen


DEFAULT_UI_LANGUAGE = 'en_US'
#DEFAULT_UI_LANGUAGE = 'zh_CN'

SERVAL_HEADER_PREFIX_IMAGE='aimg0000'


#ENCRYPT_KEY="GIIA-py-opensource"
ENCRYPT_KEY=""
ZIP_PASS='GIIA-py-opensource'
MAX_ACTION_NUMBER = 999
RECENT_JSON="recent.json"
SUPPORTED_FILE_FORMATS="jpg|png|gif"
SUPPORTED_FILE_FORMATS_LIST=['bmp', 'cur', 'gif', 'icns', 'ico', 'jpeg', 'jpg', 'pbm', 'pgm', 'png', 'ppm', 'svg', 'svgz', 'tga', 'tif', 'tiff', 'wbmp', 'webp', 'xbm', 'xpm']
SUPPORTED_FILE_FORMATS_REGEX = r'^.*\.(' + "jpg|png|gif" + ')$'

LABEL_LINE_REGEX = r'^0:__background__,.*'
MARK_REGION_LOWER_LIMIT = 20
INIT_USER_ACTION_SET_STRING = "0:__background__,"
# print(DEFAULT_USER_ACTION_SET_STRING)

ITEM_NUMBER_STYLE_SELECTED= "font-size: 20px; border: 1px solid #909090; background: #ddeeff;"
ITEM_NUMBER_STYLE_NORMAL= "font-size: 20px; border: 1px solid #e3e3e3; background: #fafafa;"
ITEM_NUMBER_STYLE_LOCKED= "font-size: 20px; border: 1px solid #f3f3f3; background: #e0e0e0;"

"""
# Red	    #e6194b	(230,  25,  75)
Green	#3cb44b	( 60, 180,  75)
Blue	#0082c8	(  0, 130, 200)
Orange	#f58231	(245, 130,  48)
Purple	#911eb4	(145,  30, 180)
Magenta	#f032e6	(240,  50, 230)
Teal	#008080	(  0, 128, 128)
Maroon	#800000	(128,   0,   0)
Olive	#808000	(128, 128,   0)
Navy	#000080	(  0,   0, 128)
"""
ANNOTATION_TAG_COLORS = [
    QColor( 60, 180,  75), QColor(  0, 130, 200), QColor(245, 130,  48),
    QColor(145,  30, 180), QColor(240,  50, 230), QColor(  0, 128, 128),
    QColor(128,   0,   0), QColor(128, 128,   0), QColor(  0,   0, 128)
]

ANNOTATION_TAG_COLOR_COUNT = len(ANNOTATION_TAG_COLORS)

def to_css_format(color: QColor, alpha=255):
    return "rgba({r}, {g}, {b}, {a})".format(r=color.red(), g=color.green(), b=color.blue(), a=alpha)


