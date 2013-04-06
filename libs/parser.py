#-*- coding:utf-8 -*-
__author__ = 'bluele'

def get_parser():
    from optparse import OptionParser

    parser = OptionParser()
    # @TODO オプションは排他的にする必要がある
    parser.add_option('-d', '--datdir',
                      dest='datdir',
                      help='data file'
                      )
    parser.add_option('-r', '--resetpassword',
                      dest='reset',
                      action='store_true',
                      help='reset password'
                      )
    parser.add_option('-c', '--cleanup',
                      dest='cleanup',
                      action='store_true',
                      )
    return parser


class Parser(object):

    @classmethod
    def execute(cls):
        from libs.cmdline import Command
        parser = get_parser()
        (options, args) = parser.parse_args()
        Command(dat_dir=options.datdir).cmdloop()