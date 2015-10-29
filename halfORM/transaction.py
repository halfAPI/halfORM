"""This module provides the Transaction class."""

import sys

class Transaction():
    """The Transaction class is intended to be used as a class attribute of
    relation.Relation class:

    Relation.transaction = Transaction

    The Relation.transaction can be used as a decorator of any method of a
    sub class of Relation class or any function receiving a Relation object
    as its first argument.

    Example of use:

    ```python
    gaston = halftest.relation("actor.person", first_name="Gaston")
    @gaston.transaction
    def do_something(person):
        #... code to be done
    do_somethin(person)
    ```
    Every SQL commands executed in the do_something function will be put in a
    transaction and commited or rolled back at the end of the function.

    Functions decorated by a transaction can be nested:

    ```python
    @gaston.transaction
    def second(gaston):
        # ... do something else
    @gaston.transaction
    def first(gaston):
        # ... do something
        second(gaston)
    first()
    ```
    Here second is called by first and both function are played in the same
    transaction.
    """

    __level = 0
    def __init__(self, func):
        self.__func = func

    def __call__(self, relation, *args, **kwargs):
        """Each time a transaction is hit, the level is increased.
        The transaction is commited when the level is back to 0 after
        the return of the function.
        """
        res = None
        try:
            Transaction.__level += 1
            if relation.model.connection.autocommit:
                relation.model.connection.autocommit = False
            res = self.__func(relation, *args, **kwargs)
            Transaction.__level -= 1
            if Transaction.__level == 0:
                relation.model.connection.commit()
                relation.model.connection.autocommit = True
        except Exception as err:
            sys.stderr.write(
                "Transaction error: {}\nRolling back!\n".format(err))
            self.__level = 0
            relation.model.connection.rollback()
            relation.model.connection.autocommit = True
            raise err
        return res
