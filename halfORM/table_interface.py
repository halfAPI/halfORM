def __init__(self, **kwargs):
    self.__cursor = self.model.cursor()
    self.__cons_fields = []
    dct = self.__class__.__dict__
    [dct[field_name].set(value)for field_name, value in kwargs.items()]

def __repr__(self):
    tks = {'r': 'TABLE', 'v': 'VIEW'}
    table_kind = tks.get(self.__kind, "UNKNOWN TYPE")
    ret = [60*'-']
    ret.append("{}: {}".format(table_kind, self.__fqtn))
    ret.append(('- cluster: {dbname}\n'
                '- schema:  {schemaname}\n'
                '- table:   {tablename}').format(**vars(self.__class__)))
    ret.append('FIELDS:')
    mx_fld_n_len = 0
    for field in self.__fields:
        if len(field.name) > mx_fld_n_len:
            mx_fld_n_len = len(field.name)
    for field in self.__fields:
        ret.append('- {}:{}{}'.format(
            field.name, ' ' * (mx_fld_n_len + 1 - len(field.name)), field))
    return '\n'.join(ret)

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
    """Better, still naive implementation of select

    - args are fields names
    - kwargs is a dict of the form {[<field name>:<value>]}
    """
    dct = self.__class__.__dict__
    [dct[field_name].set(value)for field_name, value in kwargs.items()]
    what = '*'
    if args:
        what = ', '.join([dct[field_name].name for field_name in args])
    where, values = self.__where()
    self.__cursor.execute(
        "select {} from {} {}".format(what, self.__fqtn, where), tuple(values))
    return self

def count(self, *args, **kwargs):
    """Better, still naive implementation of select

    - args are fields names
    - kwargs is a dict of the form {[<field name>:<value>]}
    """
    dct = self.__class__.__dict__
    [dct[field_name].set(value)for field_name, value in kwargs.items()]
    what = '*'
    if args:
        what = ', '.join([dct[field_name].name for field_name in args])
    where, values = self.__where()
    self.__cursor.execute(
        "select count({}) from {} {}".format(
            what, self.__fqtn, where), tuple(values))
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
    self.__cursor.execute(
        "update {} set {} {}".format(self.__fqtn, what, where),
        tuple(new_values + values))

def __iter__(self):
    for elt in self.__cursor.fetchall():
        yield elt

def __getitem__(self, key):
    return self.__cursor.fetchall()[key]

interface = {
    '__init__': __init__,
    '__repr__': __repr__,
    '__iter__': __iter__,
    '__getitem__': __getitem__,
    'fields': fields,
    'is_set': is_set,
    '__where': __where,
    'select': select,
    'count': count,
    'update': update,
    '__update': __update,
}
