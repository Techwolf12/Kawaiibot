#!/usr/bin/env python
# Author: mvdw
# Mail: <mvdw at airmail dot cc>
# Distributed under terms of the MIT license.

class MyClass(object):

    """Docstring for MyClass. """

    def __init__(self):
        """TODO: to be defined1. """
        pass
    def memes(self):
        print(self.__class__.__name__)


a = MyClass()

a.memes()
