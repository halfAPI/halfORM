# 0.6.1 (2022-05-04)

* [Transaction] Fix #6. Autocommit mode stays at False on rollback. (643f500)

## Breaking change

There is a bug in the previous versions of the Transaction class. 
If you use the Transaction class, **please upgrade to this release**.

# 0.5.14 (2022-05-04)

* [Transaction] Fix #6. Autocommit mode stays at False on rollback. (643f500)

## Breaking change

There is a bug in the previous versions of the Transaction class. 
If you use the Transaction class, **please upgrade to this release**.

# 0.6.0 (2022-04-28)

* [Breaking change] Relation.join. (fdb4be8)
* [WIP] join on reverse fkeys. (73c3233)

## Breaking change

`Relation.join` now accepts either a string or a list of strings.

```
lagaffe.join((Post(), 'posts', ['id']))
```

now returns `[{'id': value1}, {'id': value2}, ...]` instead of `[value1, value2, ...]`. It must be replaced by:

```
lagaffe.join((Post(), 'posts', 'id'))
```

# 0.5.13 (2022-03-30)
* Fix singleton decorator (97dec7e)

# 0.5.12 (2022-03-30)
* Fix #4. Allow args for singleton decorator. (3a3085c)
* fix config file import when HALFORM_CONF_DIR is not absolute (0c54c10)

# 0.5.11 (2022-02-11)
* Add singleton decorator. (9b643cf)
* README: replace . (d075977)

# 0.5.10 (2022-02-08)
* [doc] Add return value on insert. (6a70c56)
* Add warning when trying to call a Field. (86243da)
* [CI] .gitlab-ci.yml. test stage. (364b823)
* Replace format with f strings. (c45463b)

# 0.5.9. (2021-12-01)
* Quote columns names in SQL update. (7056b98)

# 0.5.8. (2021-10-12)
* [model] Add attribute production. (6046432)

# 0.5.7 (2021-09-28)
* [relation] join: only format to string instances of classes listed in TO_PROCESS. (cc81112)
* [relation] join method now raises an exception if the relations are not connected. (9152506)

# 0.5.6. (2021-09-22)
* [relation] join method. (4dd6286)

# 0.5.5 (2021-09-07)
* Add Model.diconnect method. (70af38e)

# 0.5.4 (2021-09-04)
* Add support for partitioned tables. (9106143)
* [relation] _mogrify now triggers the print of the SQL query when a DML method is invoked. (0e66601)
* Add Relation.is_empty method (faster than len(relation) == 0). (08ec57a)

# 0.5.3 (2021-09-01)
* README. (ee2d453)
* Add model.has_relation method. (9490482)

# 0.5.2 (2021-08-26)
* [test] Add HoTest class (model testing). (319ddc2)
* [doc] README. (3b9dea1)

# 0.5.1 Fix wrong url in setup. (2021-07-27)

# 0.5.0 (2021-07-27)
* Remove dependency to .hop/config. (ebe7e71)
* Removal of hop (see halfORM_packager). (7311505)
* [test] Remove nose dependency. Add pytest (13226ea)

# 0.4.7 (2021-07-19)
* [hop][0.0.2] Adds placeholder for class attributes. (bbf2990)
* [module_template_1] Fix typo. (f1466ed)
* [pylint] Remove useless parameters in super. (882a795)
* [hop][pylint] Ignore invalid-name and attribute-defined-outside-init. (10ed373)
* [hop] Remove useless encoding in module_template_1. Put hop release in the first line. (8ab9b14)
* [hop] Fix No space allowed after bracket pylint(bad-whitespace). (bae786b)
* [fkey] Use a sorted list in repr for the referenced columns of a foreign key. (21024cd)

# 0.4.6 (2021-07-08)
* [fkey] Add missing quotes in fields names. (2ff4f5d)
* [test] Replace FKEYS_PROPERTIES by FKEYS (e09ac10). (3c0a6a0)

# 0.4.5 (2021-06-22)
* [hop] hop update - fix warning message in generated files (c048cda)
* [hop] Fix local variable 'model' referenced before assignment. (09ee493)
* [hop] Add hop release in modules. Fix missing warning. (5976ddb)
* [init] if project config does not exist, asks for config creation (6132158)
* [model] Model can be instantiated even if there's no ".hop/config" file, (a1e3cf6)
* [hop][create] fix case when config file already exists but db is not yet created (59bc901)
* [hop][create] Fix ident login (7866b25)
* [hop][breaking] Replace "argparse" with "click". We now use "commands" instead of options : (6a3729f)
* [model] Remove default value for "config_file" (seems to be used all the time) (e8103b5)
* [scripts] set script to half_orm.hop.__init__:main (more precise than before) (b7bbc83)
* [setup.py] set __version__ in half_orm/__init__.py (to use it in hop -v) (a622abc)
* [deps] add click dependency (91684a3)
* [deps] missing dependency : pyYaml (f30cbbf)
* [pipfile] fix deps psycopg2 (fe2bba2)
* [patch][wip] Add missing penultimate_release view. (503816a)
* [patch] Ignore path with uppercase in first letter. (9989913)
* [fix] order in meta.view.last_release (6826178)
* [hop] Add init patch system. (e45e4f4)
* [hop] Skip camel case directories. (f186f06)


# 0.4.4 (2021-05-20)
* [hop][test] Fix wrong reference to package. (2a6a222)
* [hop] Adds a base_test module to the package. (5a27678)
* [hop] Fix error on create. (be4d3ff)

# 0.4.3 (2021-05-11)
* [hop] Add -i argument (ignore-tests) (6559244)
* [hop] Add basic testing. (14db2a0)

# 0.4.2 (2021-05-10)
* [hop/fkeys] Fix missing comma. FKEYS_PROPERTIES is deprecated. Ignore empty strings. (e09ac10)

# 0.4.1 (2021-05-10)
* [hop] Add FKEYS_PROPERTIES template. (131b529)
* Update license/setup. (aaa86dd)
* [hop/patch] Adds Patch class. (e95ca0f)
* [0.4.0] adding Pipfile to the hop package. (95dedf1)
* [setup] Fix missing hop package. (57111e1)
* [hop] Add release number to First release. (dc1056e)
* [Pipfile] Add coverage dev dependency. (2df7273)
* [hop] remove dead code. (c0420dd)
* [hop] Creates connection config file and database if missing. (5327ec3)
* [hop] Adds main/master and devel branches on create. (6a6b4e4)
* [hop] Generates skeleton test files. (b002cc8)
* [hop] Add date to meta.release. (9927a29)
* [hop] Add git project on init. (9f39516)
* [hop] Add patch system to hop. (b24ffd6)
* [0.3.1] new release. (9db30db)
* [template] setup.py README.rst -> README.md. (d7a8c69)
* [wip] Add patch system to the hop command. (0734f5d)
* [hop] Take into account HALFORM_CONF_DIR env variable. (49593e0)
* [relation] Remove None values from update kwargs. (8652909)
* Update CHANGELOG. (ef392a7)

# 0.3 (2020-11-15)

## Features

* Automatic attempt to reconnect to DB in case of execution failure. (2fd8f6d)
* Allow connection with only the database name. (325f712)
* Add HALFORM_CONF_DIR environment variable (defaults to /etc/half_orm). (45e3431)
* Prevent update and test package when creating the package with hop -c. (153cbf6)
* Allow None as a legit value to unset a field. (eb13677)
* hop renames README.rst to README.md and .haflORM to .hop. (307591c)
* Add usage information into the README file generated by hop. (c956339)
* Improve README in the package generated by hop. (00c3743)

## Fixes

* relation.is_set must always retrun a boolean. (942da6c)
* Typos in README. (0caba1c)
* Fix broken unaccent in relation. (9c3d910)

## Breaking Changes

* hop now generates a .hop directory in the package instead of .halfORM. (588c2bf)

# 0.2 (2020-04-29)

## Features

- Columns of a relation are now regular attributs of the Relation class.
  This is a breaking change.
- no more need to install halftest package (pip3) to test half_orm.
- with context on a relation now enters a transaction.

## Bug fixes

- allow weird column names: `a = 1` is a regular column name in PostgreSQL.
  Of course, you can't use the doted notation to handle such column with
  half_orm. Instead, use `rel.__dict__['a = 1']`.
- reverse fkeys 

## Breaking Changes

- Relation class is not inheriting from OrderedDict anymore.
  If `rel` is a Relation object, `rel['col']` must be replaced by `rel.col`.
- A Relation object `rel` is frozen after initialisation (`__init__`),
  meaning you can't add attributes to it. This is to prevent errors due
  to typos in the expression `rel.col = 'a'` vs. `rel.cal = 'a'`. If
  `cal` column doesn't exist in the relation, an exception is raised.
  If you need to add an attribute to a class inheriting from Relation,
  you can use `_unfreeze` and `_freeze` methods.

# 0.1.0-alpha.7 (2016-11-29)

## Features

- **relation:** Inherit foreign keys. (acb51ba)
- **test:** Add halftest package. (f2d91af)
- **model, relation:** Add reverse foreign keys. (50edf5f)
- **relation:** cast method now returns the casted relation. (bbde48a)
- **relation:** Add order_by select parameter. (57791c7)

## Bug fixes

- **fkeys:** Use issubclass instead of hasattr. (2aaf58e)
- **relation, fkey:** Fix relations with multiple foreign keys. (1a69e16)

# 0.1.0-alpha.6 (2016-11-25)

## Bug fixes

- **relation:** Refactoring. Fix fkeys on relation with set operations. Need tests. (bd806f3)
- **relation:** Check if right obj is None in \_\_set__op__. (4cf0b6a)
- **relation:** \_\_neg__ now uses \_\_set__op__ method. (444763c)
- **relation:** Pass the comparison operator with the value in to_dict method. (67e8724)
- **test:** Universe and empty sets are now correctly defined (1 = 1 patch). (2babe1f)

# 0.1.0-alpha.5 (2016-11-22)

## Features

- **halfORM:** Catch error if there is some wierd inheritance in PG that Python MRO can't handle. (aa9543e)
- **field:** Replace \_set_value method by set.
- **relation:** The ugly yet very useful 1 = 1 patch. (fd3d06f)
- **fkey:** Refactoring. Reverse key is now named after the relation it references. (5b98194)

## Bug fixes

- **relation:** Disambiguation of column name when using SQL join request.Disambiguation of column name when using SQL join request. (25f9a48)
- **halfORM:** Fix typo in module_template_1. (664159b)
- **relation:** Fix bug with FKEYS_PROPERTIES and inheritance. (675171f)
- **relation:** count must use distinct. (d6ac16b)
- **relation:** Fix joins with set operators. (e4c885c)

# 0.1.0-alpha.4 (2016-11-14)

## Features

- **halfORM:** Reduce to two the spaces reserved to the developper in relation modules (85c3d6c, 0cd6d5f)
- **model:** raise_error parameter is now passed to \_connect/reconnect. (6bba6dd)
- **relation:** Add attribute \_qrn (<schema name>.<relation name>) without double quotes. (fd6c07d)
- **relation:** Add \_set_fkeys_properties. (2b0335f)

## Bug fixes

- **halfORM:** Reverse the order in inheritance. (d7d4432)
- **halfORM:** Use aliases for imported inherited classes. Add warning in every modules. (e1f9841)

# 0.1.0-alpha.3 (2016-11-12)

## Features

- **Relation:** Add a cast method to cast to another relation type. (d662ccd)
- **halfORM:** The script can now be called without argument inside a half_orm package. (95a4ba0)
- **Model:** Model.relation replaced by get_relation_class now returns a class. (0998253)
- **Relation:** \_\_str__ becomes \_\_repr__. (af6498b)

## Bug fixes

- **halfORM:** Fix problem with curly braces in user's code. (7a02309)
- **Fkey:** The FK now references the class in the good scope. (fc304c7)
- **Relation:** Use field.where_repr to have a correct construct of the request with fkeys. (39116a2)
- **Relation:** remove the display of FOREIGN KEY when there is no FK. (89d9c6b)

# 0.1.0-alpha.2 (2016-11-10)

## Features

- **Fkey:** Add tests for foreign keys. (5158ece)
- **Relation:** attributes fields and fkeys are renamed \_fields and \_fkeys. (2e29af0)
- **Relation:** mogrify is renamed to \_mogrify. (3f3541f)

## Bug fixes

- **Fkey:** Fix bug in fkey introduced in 3c248a29 by fqrn renaming. (5158ece)
- **Fkey:** Fix is_set pb with fkeys and not constrained relations. (1c6e7d9)
- **Relation:** len wasn't working since Fields introduction. (2e29af0)
- **Relation:** Fix pb with isinstance and Relation objects. (51ff1db)

# 0.1.0-alpha.1 (2016-11-08)

- First alpha release
