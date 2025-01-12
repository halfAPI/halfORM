#!/usr/bin/env python
#-*- coding:  utf-8 -*-

from random import randint
import psycopg2
import sys
from unittest import TestCase
from datetime import date

from ..init import halftest
from half_orm import relation_errors, model
from half_orm.relation import singleton
from half_orm.relation_errors import NotASingletonError

def name(letter, integer):
    return f"{letter}{chr(ord('a') + integer)}"

class Test(TestCase):
    def setUp(self):
        self.pers = halftest.pers
        self.post = halftest.post
        self.today = halftest.today

    def test_singleton_ok(self):
        """name method is decorated with @singleton in halftest.actor.person.Person class"""
        print(type(self.pers))
        aa = self.pers(last_name='aa')
        aa.name()

    def test_not_a_singleton_raised_after_field_set(self):
        """Should raise NotASingletonError after setting a field on an OK singleton"""
        aa = self.pers(last_name='aa')
        aa.name()
        with self.assertRaises(NotASingletonError):
            aa.last_name = 'abc'
            aa.name()

    def test_not_a_singleton_raised_not_found(self):
        """Should raise NotASingletonError on empty set"""
        with self.assertRaises(NotASingletonError):
            aa = self.pers(last_name='abcdefg')
            aa.name()

    def test_not_a_singleton_raised_whole_set(self):
        """Should raise NotASingletonError on whole set if it has more than one element"""
        with self.assertRaises(NotASingletonError):
            aa = self.pers()
            aa.name()
