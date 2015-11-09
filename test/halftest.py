#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os.path
from halfORM.model import Model

dirname = os.path.dirname(__file__)
halftest = Model('{}/halftest.ini'.format(dirname))

person = halftest.relation("actor.person")
print(person)
person.delete(no_clause=True)
post = halftest.relation("blog.post")
print(post)
post.delete(no_clause=True)
comment = halftest.relation("blog.comment")
print(comment)
comment.delete(no_clause=True)

person = halftest.relation("actor.person")
print(type(person.last_name))
# just in case
#person.delete(no_clause=True)

@person.Transaction
def insert0(person):
    person(
        last_name='Lagaffe',
        first_name='Gaston',
        birth_date='1957-02-28').insert()
    person(
        last_name='Fricotin',
        first_name='Bibi',
        birth_date='1924-10-05').insert()
@person.Transaction
def insert1(person):
    insert0(person)
    person(
        last_name='Maltese',
        first_name='Corto',
        birth_date='1975-01-07').insert()
    person(
        last_name='Talon',
        first_name='Achile',
        birth_date='1963-11-07').insert()
def insert2(person):
    insert1(person)
    person(
        last_name='Jourdan',
        first_name='Gil',
        birth_date='1956-09-20').insert()
# TEST NESTED TRANSACTIONS
insert2(person)

print(person.json())
assert len(person) == 5

oo = person(first_name=('_o__o', 'like'))
print(oo)
assert len(oo) == 1

for p in person.get():
    assert len(p) == 1

_a = person(last_name=('_a%', 'like'))
a_count = len(_a)
print(_a.json())

@person.Transaction
def update(person):
    for pers in _a.get():
        pers.update(last_name=pers.last_name.value.upper())

update(person)

_A = person(last_name=('_A%', 'like'))
assert len(_A) == a_count

print(_A.json())

@person.Transaction
def update_rb(person):
    for pers in _A.get():
        print(pers.json())
        pers.update(first_name='A', last_name='A', birth_date='1970-01-01')

try:
    update_rb(person)
except Exception as err:
    pass

print(_A.json())

gaston = person(first_name="Gaston")
corto = person(first_name="Corto").getone()
corto_post = halftest.relation("blog.post", author=corto)
gaston_comment_on_corto_post = halftest.relation(
    "blog.comment",
    content=("%m'enfin%", "ilike"), author=gaston, post=corto_post)

print(gaston_comment_on_corto_post)
print('AVANT')
print("autocommit {}".format(gaston.model.connection.autocommit))
corto_post.select()
gaston_comment_on_corto_post.select()
print('APRÈS')

#person().delete(no_clause=True)

corto = halftest.relation("actor.person", first_name="Corto").getone()
post = halftest.relation("blog.post")
post.author = corto
post.title = 'Vaudou pour Monsieur le Président'
post.content = """Vaudou pour Monsieur le Président, qui se déroule à la Barbade (Antilles), puis sur l’île de Port-ducal (introuvable sur les cartes, mais que Pratt situe au sud-ouest de la Guadeloupe)."""
if len(post) == 0:
    post.insert()

post = post(title=('Vaudou%', 'like'))
#post.title.value = 'Vaudou pour Monsieur le Président'
post.author_fkey = corto
print(post)
post.mogrify()
