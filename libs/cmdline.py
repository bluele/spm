#-*- coding:utf-8 -*-
__author__ = 'bluele'

from .manager import SnippetManager, PasswordManager
from .utils import json, to_unicode, get_dump_path
from .errors import NotExistsKey, AlreadyExistsKey
from bundle.pyperclip import copy as clip_copy
import cmd


class CommandCompleteMixin():

    @staticmethod
    def parse(line):
        """ 行解析を行なってcommand名と引数を取得します
        """
        line = line.strip(' ')
        return line.split(' ')

    def complete_show(self, text, line, start_index, end_index):
        words = self.manager.list()
        if text:
            return [
                w for w in words
                if w.startswith(text)
            ]
        else:
            return words

    complete_delete = complete_clip = complete_show


class Command(CommandCompleteMixin, cmd.Cmd):

    intro = '''
This is an interactive commandline interface for snippets and password texts.
You see document for "http://docs.bluele.jp/spm"
'''
    prompt = '>>> '

    def __init__(self, *args, **kwargs):
        cmd.Cmd.__init__(self)
        try:
            self.manager = SnippetManager(*args, **kwargs)
        except Exception, emg:
            from .config import DEBUG
            import sys
            if DEBUG:
                import traceback
                print traceback.format_exc()
            print to_unicode(emg)
            sys.exit(1)

    def emptyline(self):
        self.do_help(None)

    def precmd(self, line):
        """ unicode変換を行う
        """
        return cmd.Cmd.precmd(self, to_unicode(line))

    def postcmd(self, stop, line):
        return cmd.Cmd.postcmd(self, stop, line)

    def do_create(self, key):
        try:
            if key == '':
                print u'Keyを指定してください.'
            else:
                val = raw_input('Please enter value: ')
                self.manager.create(key, val)
        except AlreadyExistsKey:
            print u'"%s"は既に存在しています.' % key

    def do_clip(self, key):
        try:
            if key == '':
                print u'Keyを指定してください.'
            else:
                value = self.manager.get(key)
                clip_copy(value)
        except NotExistsKey:
            print u'"%s"は存在しません.' % key

    def do_show(self, key):
        try:
            if key == '':
                print u'Keyを指定してください.'
            else:
                print self.manager.get(key)
        except NotExistsKey:
            print u'"%s"は存在しません.' % key

    def do_delete(self, key):
        try:
            if key == '':
                print u'Keyを指定してください.'
            else:
                self.manager.delete(key)
        except NotExistsKey:
            print u'"%s"は存在しません.' % key
    do_del = do_delete

    def do_list(self, *args):
        print u'\t'.join(self.manager.list())
    do_ls = do_list

    def do_export(self, path):
        """ datファイルを指定したパスにセットします
        """
        path = get_dump_path(path, 'dat')
        try:
            self.manager.dump_file(path)
        except Exception, emg:
            print u'Cannot export dat file to "%s"' % path
            print emg
        else:
            print u'Successfully export dat file to "%s"' % path

    def do_export_as_json(self, path):
        """ 指定したパスにjson形式でraw datをダンプします
        """
        path = get_dump_path(path, 'json')
        try:
            with open(path, 'wb') as f:
                json.dump(self.manager.dat, f, ensure_ascii=False)
        except Exception, emg:
            print u'Cannot export dat-json file to "%s"' % path
            print emg
        else:
            print u'Successfully export dat-json file to "%s"' % path

    def do_export_as_csv(self, path):
        """ 指定したパスにcsv形式でraw datをダンプします
        """
        raise NotImplementedError

    def do_import(self, path):
        """ 指定したパスからdatファイルをimportします

            datファイルは当然暗号化されているので、
            パスワード認証を行う必要がある
            @TODO: 要テスト
        """
        with open(path, 'rb') as f:
            ciphertext = f.read()
        # importするdatファイルのpasswordを入力
        key = PasswordManager.hash_method(
            PasswordManager.input_password('Master password for "%s": ' % path)
        )
        try:
            dat = json.loads(self.manager.decrypt(ciphertext, key))
        except Exception, emg:
            print u'Cannot decrypt ciphertext. Perhaps you enter incorrect password?'
            print emg
        else:
            # @TODO: mergeの仕方を考える 競合している場合等
            self.manager.dat.update(dat)
            print u'Successfully import dat file from "%s"' % path

    def do_quit(self, *args):
        self.manager.clean()
        return True
    do_q = do_quit

if __name__ == '__main__':
    Command().cmdloop()