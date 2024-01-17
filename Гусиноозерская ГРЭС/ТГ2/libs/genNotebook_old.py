# -*- encoding: utf-8 -*-

import os
import re
import hashlib

def genHeader():
    return '''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%pylab inline"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "pylab.rcParams[\\"figure.figsize\\"] = (30, 42)\\n",
    "pylab.rcParams[\\"font.size\\"] = 24\\n",
    "pylab.rcParams[\\"font.family\\"] = \\"serif\\"\\n",
    "sys.path.append('C:\\\\\\\\Users\\\\\\\\ivan\\\\\\\\jupyter\\\\\\\\Бурейская ГЭС\\\\\\\\libs')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from plotChart import print_oscilogram as po\\n",
    "from plotChart import scaleForPSS2\\n",
    "from plotChart import getIntervalRamp as getIndex"
   ]
  },'''


def getParametrs(f):
    result = ''
    if f.find("пер") > -1:
        if f.find("пот") > -1:
            result += ", def_scale=1, def_filters=2"
        else:
            result += ", def_scale=2, def_filters=10"
    elif f.find("омв") > -1 or f.find("ОМВ") > -1:
        result += ", add_chart=['omv']"
    #else:
    #    result += ",  "
        
    result += ", img_name='" + f[:-4] + ".png'"
    
    return result

def genBody(end_command, ext="csv"):
    result = ''
    for root, dirs, files in os.walk('.'):
        if root == '.':
            for f in files:
                file_md5_name = hashlib.md5(f.encode()).hexdigest()
                parametrs = getParametrs(f)
                if f[-3:] == "csv":
                    result += '''
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_''' + file_md5_name[:6] + ''' = po(\\"''' + f + '''\\", ''' + end_command + parametrs + ''')"
   ]
  },'''
    return result


def genTail():
    return '''
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    ""
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}'''
    

def genNotebook(end_command='''be=(0, -1) )"'''):
    import os
    current_dir=os.getcwd()
    power = current_dir.split('\\')[-1]
    
    with open("net-{}.ipynb".format(power), "w", encoding="utf-8") as text_file:
        text_file.write(genHeader())
        text_file.write(genBody(end_command))
        text_file.write(genTail())