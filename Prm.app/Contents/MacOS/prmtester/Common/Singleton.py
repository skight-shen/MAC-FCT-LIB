#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'prmeasure'


class Singleton(type):
    """
    This is a meta class to access singleton
    """
    # def __init__(self, *args, **kwargs):
    #    self.__instance = None
    #    super(Singleton, self).__init__()
    __instance = None

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.__instance

