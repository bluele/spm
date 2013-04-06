#-*- coding:utf-8 -*-
__author__ = 'bluele'

import os
from os.path import expanduser, join

APP_NAME = 'spm'
DEBUG = bool(os.environ.get('%s_DEBUG' % APP_NAME.upper(), False))

CONFIG_DIR_NAME = '.%s' % APP_NAME
DAT_NAME = '%s.dat' % APP_NAME
DAT_SWAP_NAME = DAT_NAME + '.swap'
MASTER_NAME = 'master'
LOG_NAME = '%s.log' % APP_NAME


__dat_dir_path = None
def get_dat_dir_path():
    global __dat_dir_path
    if __dat_dir_path is None:
        __dat_dir_path = join(
            expanduser('~'),
            CONFIG_DIR_NAME
        )
    return __dat_dir_path


def get_dat_path(dat_dir):
    return join(dat_dir or get_dat_dir_path(), DAT_NAME)


def get_dat_swap_path(dat_dir):
    return join(dat_dir or get_dat_dir_path(), DAT_SWAP_NAME)


def get_log_path(dat_dir):
    return join(dat_dir or get_dat_dir_path(), LOG_NAME)


def get_master_path(dat_dir):
    return join(dat_dir or get_dat_dir_path(), MASTER_NAME)