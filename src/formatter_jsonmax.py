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
import json
import sublime
from . import common

log = logging.getLogger('__name__')


class JsonmaxFormatter:
    def __init__(self, *args, **kwargs):
        self.view = kwargs.get('view', None)
        self.identifier = kwargs.get('identifier', None)
        self.region = kwargs.get('region', None)
        self.is_selected = kwargs.get('is_selected', False)
        self.pathinfo = common.get_pathinfo(self.view.file_name())

    def format(self, text):
        config = common.get_config_path(self.view, self.identifier, self.region, self.is_selected)
        if config:
            with open(config, 'r', encoding='utf-8') as file:
                cmd = json.load(file)
            log.debug('Current arguments: %s', cmd)

        try:
            obj = sublime.decode_value(text)
            result = json.dumps(obj, **cmd)
            return result
        except ValueError as err:
            log.error('File not formatted due to ValueError: "%s"', err)

        return None
