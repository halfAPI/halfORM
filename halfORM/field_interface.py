__version__ = "0.0.1"
__author__ = "Joël Maïzi <joel.maizi@lirmm.fr>"
__copyright__ = "Copyright (c) 2015 Joël Maïzi"
__license__ = """
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

def __init__(self, name, metadata):
    self.__name = name
    self.__metadata = metadata
    self.__is_set = False
    self.__value = None
    self.__comp = '='

def __repr__(self):
    md = self.__metadata
    return "({}) {}".format(
        md['fieldtype'], md['pkey'] and 'PK' or ('{}{}'.format(
            md['uniq'] and 'UNIQUE ' or '',
            md['notnull'] and 'NOT NULL' or '')))

@property
def name(self):
    return self.__name

@property
def is_set(self):
    return self.__is_set

def get(self):
    return self.__value

def set(self, value, comp=None):
    if type(value) is tuple:
        assert len(value) == 2
        value, comp = value
    if value is None and comp is None:
        comp = 'is'
    if value is None:
        assert comp == 'is' or comp == 'is not'
    elif comp is None:
        comp = '='
    self.__is_set = True
    self.__value = value
    self.__comp = comp

value = property(get, set)

@property
def comp(self):
    return self.__comp

interface = {
    '__init__': __init__,
    '__repr__': __repr__,
    'is_set': is_set,
    'get': get,
    'set': set,
    'name': name,
    'value': value,
    'comp': comp,
}