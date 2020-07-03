#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""This module provides the Model class.

The Model class allows to load the model of a database:
- model = Model(config_file='<config file name>')
 - model.desc() displays information on the structure of
   the database.
 - model.get_relation_class(<QRN>)
   see relation module for available methods on Relation class.

About QRN and FQRN:
- FQRN stands for: Fully Qualified Relation Name. It is composed of:
  <database name>.<schema name>.<table name>.
  Only the schema name can have dots in it. In this case, you must double
  quote the schema name :
  <database connection filename>."<schema name>".<table name>
  ex:
  - one.public.my_table
  - two."access.role".acces
- QRN is the Qualified Relation Name. Same as the FQRN without the database
  name. Double quotes can be ommited even if there are dots in the schema name.

"""

import sys
import os
from collections import OrderedDict
from configparser import ConfigParser

import psycopg2
from psycopg2.extras import RealDictCursor

from half_orm import model_errors
from half_orm.relation import _normalize_fqrn, _normalize_qrn, _factory

__all__ = ["Model", "camel_case"]

def camel_case(name):
    """Transform a string in camel case."""
    ccname = []
    name = name.lower()
    capitalize = True
    for char in name:
        if not char.isalnum():
            capitalize = True
            continue
        if capitalize:
            ccname.append(char.upper())
            capitalize = False
            continue
        ccname.append(char)
    return ''.join(ccname)

psycopg2.extras.register_uuid()
#from pprint import PrettyPrinter

class Model:
    """Model class

    The model establishes a connection to the database and allows to
    generate a Relation object using model.relation(QRN) method.
    """
    __deja_vu = {}
    __metadata = {}
    _relations_ = {}
    def __init__(self,
                 config_file=None, dbname=None, scope=None, raise_error=True):
        """Model constructor

        Use @config_file in your scripts. The @dbname parameter is
        reserved to the _factory metaclass.
        """
        self.__backend_pid = None

        dbinfo = {}

        # Helper function to convert the string-based dsn to a dict
        dsntodict = lambda dsn: dict(
            map(lambda x:
                map(lambda y: y.strip("'\""),
                x.split('=')
                ),
            dsn.split()))


        if not dbname:
            # If it is user-called

            if os.environ.get('HALFORM_DSN'):
                # If the parameters are in the environment variables,
                # put them into the dict
                dbinfo = dsntodict(os.environ.get('HALFORM_DSN'))

            elif config_file is not None:
                self.__config_file = config_file
                # If the parameters are in a configuration file
                config = ConfigParser()

                # Try to read the data from config_file, or from /etc/half_orm/{config_file}
                if not config.read(
                        [self.__config_file,
                        '/etc/half_orm/{}'.format(self.__config_file)]):
                    raise model_errors.MissingConfigFile(self.__config_file)

                # Conversion of the ini-file configuration to a dict
                dbinfo = dict(config['database'].items())
                if 'name' in dbinfo.keys():
                    dbinfo['dbname'] = dbinfo.pop('name')

            else:
                raise Exception("Missing database configuration")

        elif config_file is not None:
            raise RuntimeError("You can't specify config_file with dbname!")

        else:
            # If it is _factory called, we check if it is already defined in deja_vu

            self.__dbname = dbname
            if Model._deja_vu(dbname):
                Model.__deja_vu['dbname'] = self
                return
            else:
                # @TODO : What to do if there's no existing database and no configuration?
                raise Exception(f'The database {dbname} is not yet defined')

        needed_params = {'dbname', 'user'}
        missing_params = []
        [ (missing_params.append(key) if key not in dbinfo.keys() else None) for key in needed_params ]
        if len(missing_params) > 0:
            raise model_errors.MissingParameters(
                missing_params, filename=config_file)

        self._dbinfo = dbinfo
        self.__dbname = dbinfo['dbname']
        self.__conn = None
        self.__cursor = None
        self._scope = scope and scope.split('.')[0]
        self._relations_['list'] = []
        self._relations_['classes'] = {}
        self.__raise_error = raise_error
        self._connect(raise_error=self.__raise_error)

    @staticmethod
    def _deja_vu(dbname):
        """Returns None if the database hasn't been loaded yet.
        Otherwise, it returns the Model object already loaded.
        The Model object is shared between all_ the relations in the
        database. The Model object is loaded only once for a given database.
        """
        return Model.__deja_vu.get(dbname)

    def ping(self):
        """Returns True if the connection is OK.

        Otherwise attempts a new connection and return False.
        """
        try:
            self.execute_query("select 1")
            return True
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            try:
                self._connect(raise_error=self.__raise_error)
            except psycopg2.OperationalError as err:
                sys.stderr.write('{}\n'.format(err))
                sys.stderr.flush()
            return False

    def _connect(self, raise_error=True):
        """Setup a new connection to the database.

        If a config_file is provided, the connection is made with the new
        parameters, allowing to change role. The database name must be the same.

        The reconnect method is an alias to the connect method.
        """
        if self.__conn is not None:
            if not self.__conn.closed:
                self.__conn.close()

        try:
            self.__conn = psycopg2.connect(**self._dbinfo,
                cursor_factory=RealDictCursor)
        except psycopg2.OperationalError as err:
            if raise_error:
                raise err.__class__(err)
            sys.stderr.write("{}\n".format(err))
            sys.stderr.flush()
        except Exception as e:
            print(self._dbinfo)
            print(e)
        self.__conn.autocommit = True
        self.__cursor = self.__conn.cursor()
        self.__metadata[self.__dbname] = self.__get_metadata()
        self.__deja_vu[self.__dbname] = self
        self.__backend_pid = self.execute_query(
            "select pg_backend_pid()").fetchone()['pg_backend_pid']

    reconnect = _connect

    @property
    def _pg_backend_pid(self):
        "backend PID"
        return self.__backend_pid

    @property
    def _dbname(self):
        """
        property. Returns the database name.
        """
        return self.__dbname

    @property
    def _connection(self):
        """\
        Property. Returns the psycopg2 connection attached to the Model object.
        """
        return self.__conn

    @property
    def _metadata(self):
        """Returns the metadata of the database.
        Uses the Model.__metadata class dictionary.
        """
        return self.__metadata[self.__dbname]

    def __get_metadata(self):
        """Loads the metadata by querying the request in the pg_metaview
        module.
        """
        from .pg_metaview import REQUEST
        metadata = {}
        byname = metadata['byname'] = OrderedDict()
        byid = metadata['byid'] = {}
        with self._connection.cursor() as cur:
            cur.execute(REQUEST)
            all_ = [elt for elt in cur.fetchall()]
            for dct in all_:
                table_key = (
                    self.__dbname,
                    dct['schemaname'], dct['relationname'])
                tableid = dct['tableid']
                description = dct['tabledescription']
                if table_key not in byname:
                    byid[tableid] = {}
                    byid[tableid]['sfqrn'] = table_key
                    byid[tableid]['fields'] = OrderedDict()
                    byid[tableid]['fkeys'] = OrderedDict()
                    byname[table_key] = OrderedDict()
                    byname[table_key]['description'] = description
                    byname[table_key]['fields'] = OrderedDict()
                    byname[table_key]['fkeys'] = OrderedDict()
                    byname[table_key]['fields_by_num'] = OrderedDict()
            for dct in all_:
                tableid = dct['tableid']
                table_key = byid[tableid]['sfqrn']
                fieldname = dct.pop('fieldname')
                fieldnum = dct['fieldnum']
                tablekind = dct.pop('tablekind')
                inherits = [byid[int(elt.split(':')[1])]['sfqrn']
                            for elt in dct.pop('inherits') if elt is not None]
                byname[table_key]['tablekind'] = tablekind
                byname[table_key]['inherits'] = inherits
                byname[table_key]['fields'][fieldname] = dct
                byname[table_key]['fields_by_num'][fieldnum] = dct
                byid[tableid]['fields'][fieldnum] = fieldname
                if (tablekind, table_key) not in self._relations_['list']:
                    self._relations_['list'].append((tablekind, table_key))
            for dct in all_:
                tableid = dct['tableid']
                table_key = byid[tableid]['sfqrn']
                fkeyname = dct['fkeyname']
                if fkeyname and not fkeyname in byname[table_key]['fkeys']:
                    fkeytableid = dct['fkeytableid']
                    ftable_key = byid[fkeytableid]['sfqrn']
                    fields = [byid[tableid]['fields'][num] for num in dct['keynum']]
                    ffields = [byid[fkeytableid]['fields'][num] for num in dct['fkeynum']]
                    fqdn_ = list(filter(lambda x: x is not None, list(table_key) + fields))
                    rev_fkey_name = '_reverse_fkey_{}'.format(
                        "_".join(fqdn_)).replace(".", "_")
                    byname[table_key]['fkeys'][fkeyname] = (ftable_key, ffields, fields)
                    byname[ftable_key]['fkeys'][rev_fkey_name] = (table_key, fields, ffields)

        self._relations_['list'].sort()
        return metadata

    def execute_query(self, query, values=()):
        """Execute a raw SQL query"""
        cursor = self.__conn.cursor()
        cursor.execute(query, values)
        return cursor

    def get_relation_class(self, qtn):
        """Retuns the class corresponding to the fqrn relation in the database.

        @qtn is the <schema>.<table> name of the relation
        @kwargs is a dictionary {field_name:value}
        """
        schema, table = qtn.rsplit('.', 1)
        fqrn = '.'.join([self._dbinfo['dbname'], '"{}"'.format(schema), table])
        fqrn, _ = _normalize_fqrn(fqrn)
        return _factory('Table', (), {'fqrn': fqrn, 'model': self})

    def _import_class(self, qtn, scope=None):
        """Used to return the class from the scope module.
        """
        module_path = '{}.{}'.format(scope or self._scope, qtn.replace('"', ''))
        class_name = camel_case(qtn.split('.')[-1])
        module = __import__(
            module_path, globals(), locals(), [class_name], 0)
        if scope:
            self._scope = scope
        return module.__dict__[class_name]

    def _relations(self):
        """List all_ the relations in the database"""
        for relation in self._relations_['list']:
            yield "{} {}.{}.{}".format(relation[0], *relation[1])

    def desc(self, qrn=None, type_=None):
        """Returns the list of the relations of the model.

        Each line contains:
        - the relation type: 'r' relation, 'v' view, 'm' materialized view,
        - the quoted FQRN (Fully qualified relation name) "<schema name>"."<relation name>"
        - the list of the FQRN of the inherited relations.

        If a qualified relation name (<schema name>.<table name>) is
        passed, prints only the description of the corresponding relation.
        """
        def get_fqrn(key):
            "returns the quoted version of the FQRN"
            return ".".join(['"{}"'.format(elt) for elt in key[1:]])

        if not qrn:
            ret_val = []
            entry = self.__metadata[self.__dbname]['byname']
            for key in entry:
                inh = []
                tablekind = entry[key]['tablekind']
                fqrn = get_fqrn(key)
                if entry[key]['inherits']:
                    inh = [get_fqrn(elt) for elt in entry[key]['inherits']]
                if type_:
                    if tablekind != type_:
                        continue
                ret_val.append((tablekind, fqrn, inh))
            return ret_val
        fqrn = '"{}".{}'.format(self.__dbname, _normalize_qrn(qrn=qrn))
        return str(_factory(
            'Table', (), {'fqrn': fqrn, 'model': self})())

    def __str__(self):
        out = []
        entry = self.__metadata[self.__dbname]['byname']
        for key in entry:
            fqrn = ".".join(['"{}"'.format(elt) for elt in key[1:]])
            out.append('{} {}'.format(entry[key]['tablekind'], fqrn))
        return '\n'.join(out)
