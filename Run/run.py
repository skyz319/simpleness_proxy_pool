#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   LogHandler.py
@Time    :   2019-06-18 16:45
@Author  :   Sky.z
@Version :   1.0
@Contact :   skyz319@gmail.com
@License :   (C)Copyright 2017-2018, Sky.z
@Desc    :   None
"""
from Api.api import app
from Schedule.schedule import Schedule

def main():

    s = Schedule()
    s.run()
    app.run()


if __name__ == '__main__':
    main()


