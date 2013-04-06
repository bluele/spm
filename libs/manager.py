#-*- coding:utf-8 -*-
__author__ = 'bluele'

from .errors import AlreadyExistsKey, NotExistsKey, NotFoundPasswordFile, AlreadyRunningError
from .config import *
from .utils import sha256, encrypt, decrypt
from getpass import getpass
from os import mkdir
from os.path import isfile, isdir
from shutil import move, copy
import re
try:
    import json
except:
    import simplejson as json


class SnippetManager(object):

    def __init__(self, dat_dir=None):
        self.dat_dir = dat_dir or get_dat_dir_path()
        self.pm = PasswordManager(
            master_path=get_master_path(self.dat_dir)
        )

        if not isdir(self.dat_dir):
            # App initialization
            mkdir(self.dat_dir)
            self.init()
            self.dump_file(self.dat_path, dict())

        if isfile(self.dat_swap_path):
            raise AlreadyRunningError

        try:
            self.dat = self.load_file(self.dat_path)
        except NotFoundPasswordFile, emg:
            print emg
            print u'Create new master file on "%s"' % self.pm.master_path
            self.pm.initialize()
            self.dump_file(self.dat_path, dict())
            self.dat = self.load_file(self.dat_path)

    @property
    def dat_path(self):
        return get_dat_path(self.dat_dir)

    @property
    def log_path(self):
        return get_log_path(self.dat_dir)

    @property
    def dat_swap_path(self):
        return get_dat_swap_path(self.dat_dir)

    @property
    def is_authenticate(self):
        """ 認証する
            初期化されているかどうかを判定する必要がある
        """
        try:
            self.authenticate()
        except Exception, emg:
            print emg
            return False
        else:
            return True

    def init(self):
        self.authenticate()

    def authenticate(self):
        try:
            self.pm.authenticate()
        except NotFoundPasswordFile, emg:
            print "Initialize Master password."
            self.pm.initialize()

    def load_file(self, path):
        """ 指定したパスからdatファイルを読み取り復号化します
        """
        with open(path, 'rb') as f:
            return json.loads(self.decrypt(f.read()))

    def dump_file(self, path, dat=None):
        dat = self.dat if dat is None else dat
        with open(path, 'wb') as f:
            f.write(self.encrypt(json.dumps(dat)))

    def create(self, key, value):
        if key in self.dat:
            raise AlreadyExistsKey(key)
        self.dat[key] = value

    def get(self, key):
        if key not in self.dat:
            raise NotExistsKey(key)
        return self.dat[key]

    def delete(self, key):
        if key not in self.dat:
            raise NotExistsKey(key)
        del self.dat[key]

    def list(self):
        return self.dat.keys()

    def save(self):
        """ 現在の変更状態をsaveします
            swapの内容をmasterにコピー
        """
        self.dump_file(self.dat_swap_path)
        copy(self.dat_swap_path, self.dat_path)

    def clean(self):
        """ 変更内容を保管してswapを削除(mv)
        """
        self.dump_file(self.dat_swap_path)
        move(self.dat_swap_path, self.dat_path)

    def encrypt(self, message):
        return encrypt(self.pm.secret_key, message)

    def decrypt(self, ciphertext, key=None):
        key = key if key else self.pm.secret_key
        return decrypt(key, ciphertext)


class PasswordManager(object):
    valid_pattern = re.compile(ur'^[a-zA-Z0-9]{4,20}$')
    description = '英数字4文字以上20文字以下'

    def __init__(self, master_path):
        self.__password_hash = None
        self.master_path = master_path

    @classmethod
    def to_hash(cls, string):
        return sha256(string)

    @classmethod
    def to_double_hash(cls, string):
        return cls.to_hash(cls.to_hash(string))

    @property
    def secret_key(self):
        if self.__password_hash is None:
            self.authenticate()
        return self.__password_hash

    @classmethod
    def input_password(cls, message, is_valid=True, is_retype=False):
        """ passwordをユーザに入力させます

            :message    入力を促すメッセージ
            :is_retype  入力確認を行うかどうかの真偽値
        """
        password = getpass(message)
        if is_valid and not cls.is_valid_style_password(password):
            raise ValueError('パスワードは"%s"の文字列でなければなりません。' % (cls.description,))
        if is_retype:
            re_password = getpass('Retype master password: ')
            if password != re_password:
                raise Exception("Try again.")
        return password

    def initialize(self):
        """ MasterPasswordの初期化処理を行います
            1. パスワード生成処理
            2. 再パスワード入力
            3. パスワードの保存
            4. パスワード自動認証
        """
        self.__password_hash = self.save(
            self.input_password('New master password: ', is_retype=True)
        )

    def save(self, password):
        """ 指定したパスワードの文字列をハッシュ化して保存します
        """
        password_hash = self.to_hash(password)
        with open(self.master_path, 'wb') as f:
            f.write(self.to_hash(password_hash))
        return password_hash

    def load(self):
        """ パスワードハッシュを読み込みます
        """
        with open(self.master_path, 'rb') as f:
            return f.read()

    def authenticate(self):
        """ ユーザが入力したマスタパスワードの認証を行う
            初めに認証を行うために必須であるmasterファイルの存在確認を行う
        """
        if not isfile(self.master_path):
            raise NotFoundPasswordFile('Not found file: %s' % self.master_path)
        password = self.input_password('Master password: ', is_valid=False)
        password_hash = self.to_hash(password)
        if not self.__is_valid_password_hash(password_hash):
            raise Exception('Incorrect password attempt.')
        self.__password_hash = password_hash

    def __is_valid_password_hash(self, password_hash):
        """ ユーザが入力したパスワードが正しいパスワードかどうかの真偽値を返します
        """
        return self.load() == self.to_hash(password_hash)

    @classmethod
    def is_valid_style_password(cls, password):
        return bool(cls.valid_pattern.search(password))