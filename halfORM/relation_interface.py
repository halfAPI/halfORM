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

from .model import relation

def __init__(self, **kwargs):
    self.__cursor = self.model.connection.cursor()
    self.__cons_fields = []
    dct = self.__class__.__dict__
    [dct[field_name].set(value)for field_name, value in kwargs.items()]

def __call__(self, **kwargs):
    """__call__ method for the class Relation

    Instanciate a new object with all fields unset.
    """
    return relation(self.__fqrn, **kwargs)

def __str__(self):
    """XXX TEST Should be called json
    """
    import json, datetime
    def handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        #elif isinstance(obj, ...):
        #    return ...
        else:
            raise TypeError(
                'Object of type {} with value of '
                '{} is not JSON serializable'.format(type(obj), repr(obj)))
    return json.dumps([elt for elt in self.select()], default=handler)

def __repr__(self):
    rel_kind = self.__kind
    ret = [60*'-']
    ret.append("{}: {}".format(rel_kind, self.__fqrn))
    ret.append(('- cluster: {dbname}\n'
                '- schema:  {schemaname}\n'
                '- {__kind}:   {relationname}').format(**vars(self.__class__)))
    ret.append('FIELDS:')
    mx_fld_n_len = 0
    for field in self.__fields:
        if len(field.name) > mx_fld_n_len:
            mx_fld_n_len = len(field.name)
    for field in self.__fields:
        ret.append('- {}:{}{}'.format(
            field.name, ' ' * (mx_fld_n_len + 1 - len(field.name)), field))
    for fkey in self.__fkeys:
        ret.append(repr(fkey))
    return '\n'.join(ret)

def desc(self):
    return repr(self)

@property
def fqrn(self):
    return self.__fqrn

@property
def is_set(self):
    """return True if one field at least is set"""
    for field in self.__fields:
        if field.is_set:
            return True
    return False

@property
def fields(self):
    for field in self.__fields:
        yield field

def __where(self):
    where = ''
    values = ()
    set_fields = [field for field in self.__fields if field.is_set]
    where_clause = ''
    if set_fields:
        where_clause = [
            '{} {} %s'.format(field.name, field.comp) for field in set_fields]
        where_clause = 'where {}'.format(" and ".join(where_clause))
        values = [field.value for field in set_fields]
    return where_clause, values

def select(self, *args, **kwargs):
    """Generator. Yiels result of query on dictionary form.

    - @args are fields names to restrict the returned attributes
    - @kwargs: limit, order by, distinct... options
    """
    dct = self.__class__.__dict__
    what = '*'
    if args:
        what = ', '.join([dct[field_name].name for field_name in args])
    where, values = self.__where()
    self.__cursor.execute(
        "select {} from {} {}".format(what, self.__fqrn, where), tuple(values))
    for elt in self.__cursor.fetchall():
        yield elt

def count(self, *args, **kwargs):
    """Better, still naive implementation of select

    - @args are fields names to restrict the returned attributes
    - @kwargs: limit, distinct, ...

    """
    dct = self.__class__.__dict__
    what = '*'
    if args:
        what = ', '.join([dct[field_name].name for field_name in args])
    where, values = self.__where()
    self.__cursor.execute(
        "select count({}) from {} {}".format(
            what, self.__fqrn, where), tuple(values))
    return self.__cursor.fetchone()['count']

def __update(self, **kwargs):
    what = []
    new_values = []
    for field_name, new_value in kwargs.items():
        what.append(field_name)
        new_values.append(new_value)
    return ", ".join(["{} = %s".format(elt) for elt in what]), new_values

def update(self, no_clause=False, **kwargs):
    """
    kwargs represents the values to be updated {[field name:value]}
    The object self must be set unless no_clause is false.
    """
    if not kwargs:
        return # no new value update. Should we raise an error here?
    assert self.is_set or no_clause
    where, values = self.__where()
    what, new_values = self.__update(**kwargs)
    query = "update {} set {} {}".format(self.__fqrn, what, where)
#    print(query, tuple(new_values + values))
    self.__cursor.execute(query, tuple(new_values + values))

def __what_to_insert(self):
    fields_names = []
    values = ()
    set_fields = [field for field in self.__fields if field.is_set]
    if set_fields:
        fields_names = [field.name for field in set_fields]
        values = [field.value for field in set_fields]
    return ", ".join(fields_names), values

def insert(self, **kwargs):
    dct = self.__class__.__dict__
    [dct[field_name].set(value)for field_name, value in kwargs.items()]
    fields_names, values = self.__what_to_insert()
    what_to_insert = ", ".join(["%s" for i in range(len(values))])
    self.__cursor.execute(
        "insert into {} ({}) values ({})".format(
            self.__fqrn, fields_names, what_to_insert),
        tuple(values))

def delete(self, no_clause=False, **kwargs):
    """
    kwargs is {[field name:value]}
    The object self must be set unless no_clause is false.
    """
    dct = self.__class__.__dict__
    [dct[field_name].set(value)for field_name, value in kwargs.items()]
    assert self.is_set or no_clause
    where, values = self.__where()
    self.__cursor.execute(
        "delete from {} {}".format(self.__fqrn, where), tuple(values))

def get(self, **kwargs):
    for dct in self.select(**kwargs):
        elt = self(**dct)
        yield elt

def __iter__(self):
    raise NotImplementedError

def __getitem__(self, key):
    return self.__cursor.fetchall()[key]

table_interface = {
    '__init__': __init__,
    '__call__': __call__,
    '__str__': __str__,
    '__iter__': __iter__,
    '__getitem__': __getitem__,
    '__repr__': __repr__,
    'desc': desc,
    'fields': fields,
    'fqrn': fqrn,
    'is_set': is_set,
    '__where': __where,
    'insert': insert,
    '__what_to_insert': __what_to_insert,
    'select': select,
    'count': count,
    'update': update,
    '__update': __update,
    'delete': delete,
    'get': get,
}

view_interface = {
    '__init__': __init__,
    '__str__': __str__,
    '__iter__': __iter__,
    '__getitem__': __getitem__,
    '__repr__': __repr__,
    'desc': desc,
    'fields': fields,
    'is_set': is_set,
    '__where': __where,
    'select': select,
    'count': count,
    'get': get,
}

class Relation():
    pass
