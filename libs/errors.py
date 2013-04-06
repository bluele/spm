#-*- coding:utf-8 -*-
__author__ = 'bluele'


class AlreadyExistsKey(Exception):
    """ 既に指定した名前が登録されていた際に呼び出される例外
    """


class NotExistsKey(Exception):
    """ 指定した名前を持つ値が登録されていない際に呼び出される例外
    """


class NotFoundPasswordFile(Exception):
    pass


class AlreadyRunningError(Exception):
    pass