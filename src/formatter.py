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
from .formatter_beautysh import BeautyshFormatter
from .formatter_black import BlackFormatter
from .formatter_clangformat import ClangformatFormatter
from .formatter_cleancss import CleancssFormatter
from .formatter_csscomb import CsscombFormatter
from .formatter_eslint import EslintFormatter
from .formatter_htmlminifier import HtmlminifierFormatter
from .formatter_htmltidy import HtmltidyFormatter
from .formatter_jsbeautifier import JsbeautifierFormatter
from .formatter_jsonmax import JsonmaxFormatter
from .formatter_jsonmin import JsonminFormatter
from .formatter_perltidy import PerltidyFormatter
from .formatter_phpcsfixer import PhpcsfixerFormatter
from .formatter_prettier import PrettierFormatter
from .formatter_prettydiffmax import PrettydiffmaxFormatter
from .formatter_prettydiffmin import PrettydiffminFormatter
from .formatter_prettytable import PrettytableFormatter
from .formatter_pythonminifier import PythonminifierFormatter
from .formatter_rubocop import RubocopFormatter
from .formatter_sqlformatter import SqlformatterFormatter
from .formatter_sqlmin import SqlminFormatter
from .formatter_stylelint import StylelintFormatter
from .formatter_terser import TerserFormatter
from .formatter_uncrustify import UncrustifyFormatter
from .formatter_yapf import YapfFormatter
from . import common

log = logging.getLogger('__name__')


class Formatter:
    def __init__(self, view):
        pass

    def run_formatter(self, *args, **kwargs):
        view = kwargs.get('view', None)
        identifier = kwargs.get('identifier', None)
        region = kwargs.get('region', None)
        is_selected = kwargs.get('is_selected', False)
        text = kwargs.get('text', None)

        if view.is_read_only() or not view.window() or view.size () == 0:
            log.error('View is not formattable.')
            return None

        if not text:
            return None

        formatter_map = {
            'beautysh': BeautyshFormatter,
            'black': BlackFormatter,
            'clangformat': ClangformatFormatter,
            'cleancss': CleancssFormatter,
            'csscomb': CsscombFormatter,
            'eslint': EslintFormatter,
            'htmlminifier': HtmlminifierFormatter,
            'htmltidy': HtmltidyFormatter,
            'jsbeautifier': JsbeautifierFormatter,
            'jsonmax': JsonmaxFormatter,
            'jsonmin': JsonminFormatter,
            'perltidy': PerltidyFormatter,
            'phpcsfixer': PhpcsfixerFormatter,
            'prettier': PrettierFormatter,
            'prettydiffmax': PrettydiffmaxFormatter,
            'prettydiffmin': PrettydiffminFormatter,
            'prettytable': PrettytableFormatter,
            'pythonminifier': PythonminifierFormatter,
            'rubocop': RubocopFormatter,
            'sqlformatter': SqlformatterFormatter,
            'sqlmin': SqlminFormatter,
            'stylelint': StylelintFormatter,
            'terser': TerserFormatter,
            'uncrustify': UncrustifyFormatter,
            'yapf': YapfFormatter
        }

        formatter_class = formatter_map.get(identifier)
        if formatter_class:
            syntax = common.get_assigned_syntax(view, identifier, region, is_selected)
            if not syntax:
                common.prompt_error('Syntax out of the scope.', 'ID:' + identifier)
            else:
                file = view.file_name()
                log.debug('Target: %s', file if file else '(view)')
                log.debug('Scope: %s', view.scope_name(0 if not is_selected else region.a))
                log.debug('Syntax: %s', syntax)
                log.debug('Formatter ID: %s', identifier)
                worker = formatter_class(*args, **kwargs)
                result = worker.format(text)
                if result:
                    # Pass the result back to the main thread.
                    args = {'result': result, 'region': [region.a, region.b]}
                    view.run_command('substitute', args)
                    return True
        else:
            log.error('Formatter ID not found: %s', identifier)

        return False
