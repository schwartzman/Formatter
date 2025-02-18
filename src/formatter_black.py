#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @id           $Id$
# @rev          $Format:%H$ ($Format:%h$)
# @tree         $Format:%T$ ($Format:%t$)
# @date         $Format:%ci$
# @author       $Format:%an$ <$Format:%ae$>
# @copyright    Copyright (c) 2019-present, Duc Ng. (bitst0rm)
# @link         https://github.com/bitst0rm
# @license      The MIT License (MIT)

import logging
from distutils.version import StrictVersion
from . import common

log = logging.getLogger('__name__')
INTERPRETERS = ['python3', 'python']
EXECUTABLES = ['black']


class BlackFormatter:
    def __init__(self, *args, **kwargs):
        self.view = kwargs.get('view', None)
        self.identifier = kwargs.get('identifier', None)
        self.region = kwargs.get('region', None)
        self.is_selected = kwargs.get('is_selected', False)
        self.pathinfo = common.get_pathinfo(self.view.file_name())

    def is_compat(self):
        try:
            python = common.get_intr_exec_path(self.identifier, INTERPRETERS, 'interpreter')
            if python:
                proc = common.exec_cmd([python, '-V'], self.pathinfo[1])
                stdout = proc.communicate()[0]
                string = stdout.decode('utf-8')
                version = string.splitlines()[0].split(' ')[1]
                if StrictVersion(version) >= StrictVersion('3.7.0'):
                    return True
                common.prompt_error('Current Python version: %s\nBlack requires a minimum Python 3.7.0.' % version, 'ID:' + self.identifier)
            return None
        except OSError:
            log.error('Error occurred while validating Python compatibility.')

        return None

    def get_cmd(self):
        cmd = common.get_head_cmd(self.identifier, INTERPRETERS, EXECUTABLES)
        if not cmd:
            return None

        config = common.get_config_path(self.view, self.identifier, self.region, self.is_selected)
        if config:
            cmd.extend(['--config', config])

        cmd.extend(['-'])

        return cmd

    def format(self, text):
        cmd = self.get_cmd()
        log.debug('Current arguments: %s', cmd)
        cmd = common.set_fix_cmds(cmd, self.identifier)
        if not cmd or not self.is_compat():
            return None

        try:
            proc = common.exec_cmd(cmd, self.pathinfo[1])
            stdout, stderr = proc.communicate(text.encode('utf-8'))

            errno = proc.returncode
            if errno > 0:
                log.error('File not formatted due to an error (errno=%d): "%s"', errno, stderr.decode('utf-8'))
            else:
                return stdout.decode('utf-8')
        except OSError:
            log.error('Error occurred while running: %s', ' '.join(cmd))

        return None
