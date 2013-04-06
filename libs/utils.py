#-*- coding:utf-8 -*-
__author__ = 'bluele'

from bundle.Padding import appendPadding as _appendPadding, \
                    removePadding as _removePadding, \
                    AES_blocksize
try:
    import Crypto.Cipher.AES as AES
    from Crypto.Hash import SHA256
    def sha256(string):
        hs = SHA256.new()
        hs.update(string)
        return hs.digest()
except:
    import bundle.CryptoPlusLite.Cipher.python_AES as AES
    from hashlib import sha256 as SHA256
    def sha256(string):
        return SHA256(string).digest()
try:
    import json
except:
    import simplejson as json


def appendPadding(string):
    return _appendPadding(string, blocksize=AES_blocksize, mode='CMS')


def removePadding(string):
    return _removePadding(string, blocksize=AES_blocksize, mode='CMS')


def encrypt(hash_key, message):
    """ messageをhash_keyで暗号化したもの返します
    """
    message = appendPadding(message)
    c_obj = AES.new(hash_key, AES.MODE_ECB)
    return c_obj.encrypt(message)


def decrypt(hash_key, ciphertext):
    """ cypher_textをhash_keyで復号化したものを返します
    """
    c_obj = AES.new(hash_key, AES.MODE_ECB)
    return removePadding(c_obj.decrypt(ciphertext))


def to_unicode(text):
    """ str型のテキストをunicode型に変換します
    """
    if isinstance(text, unicode):
        return text

    text = str(text)
    encodes = ('utf8', 'shift-jis', 'cp932', 'euc-jp')
    try:
        for encode in encodes:
            return text.decode(encode)
    except:
        pass
    raise ValueError('Cannot decode text "%s".' % text)


def get_dump_path(path, ext='dat'):
    """ dump先のパスを返します
        pathがdirの時はfile
    """
    from .config import APP_NAME
    from os.path import isfile, isdir, join
    if isdir(path):
        return join(path, u'%s.%s' % (APP_NAME, ext))
    return path