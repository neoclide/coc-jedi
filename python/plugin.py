# -*- coding: utf-8 -*-
from __future__ import print_function
import logging
import sys
import os

jedi_path = os.path.join(os.path.dirname(__file__), 'jedi')
sys.path.insert(0, jedi_path)
parso_path = os.path.join(os.path.dirname(__file__), 'parso')
sys.path.insert(0, parso_path)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

try:
    import jedi
except ImportError:
    jedi = None
    eprint('jedi module not found')
else:
    try:
        version = jedi.__version__
    except Exception as e:  # e.g. AttributeError
        eprint("Error when loading the jedi python module ({0}). "
            "Please ensure that Jedi is installed correctly (see Installation "
            "in the README.".format(e))
        jedi = None
    else:
        if isinstance(version, str):
            # the normal use case, now.
            from jedi import utils
            version = utils.version_info()
        if version < (0, 7):
            eprint('Please update your Jedi version, it is too old.')
finally:
    sys.path.remove(jedi_path)
    sys.path.remove(parso_path)


class Plugin(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.current_environment = (None, None)
        self.completions = []

    def echo(self, msg, hl="MoreMsg"):
        self.nvim.call('coc#util#echo_messages', hl, msg.split('\n'))

    def _get_environment(self, use_cache=True):
        vim_force_python_version = self.nvim.vars.get("g:jedi#force_py_version", 'auto')
        if use_cache and vim_force_python_version == self.current_environment[0]:
            return self.current_environment[1]

        environment = None
        if vim_force_python_version == "auto":
            environment = jedi.api.environment.get_cached_default_environment()
        else:
            force_python_version = vim_force_python_version
            if '0000' in force_python_version or '9999' in force_python_version:
                # It's probably a float that wasn't shortened.
                try:
                    force_python_version = "{:.1f}".format(float(force_python_version))
                except ValueError:
                    pass
            elif isinstance(force_python_version, float):
                force_python_version = "{:.1f}".format(force_python_version)

            try:
                environment = jedi.get_system_environment(force_python_version)
            except jedi.InvalidPythonEnvironment as exc:
                environment = jedi.api.environment.get_cached_default_environment()
                self.echo("force_python_version=%s is not supported: %s - using %s." % (
                        vim_force_python_version, str(exc), str(environment)))

        self.current_environment = (vim_force_python_version, environment)
        return environment

    def _get_script(self, source=None, line=None, column=None, path=None):
        vim = self.nvim
        jedi.settings.additional_dynamic_modules = [
            b.name for b in vim.buffers if (
                b.name is not None and
                b.name.endswith('.py') and
                b.options['buflisted'])]
        if source is None:
            source = '\n'.join(vim.current.buffer)
        if line is None:
            line = vim.current.window.cursor[0]
        if column is None:
            column = vim.current.window.cursor[1] - 1
        if  path is None:
            path = vim.current.buffer.name

        return jedi.Script(
            source, line, column, path,
            encoding=vim.eval('&encoding') or 'latin1',
            environment=self._get_environment(),
        )

    # line start 1, column start 0
    def completion(self, line, column, source, path):
        script = self._get_script(source=source, line=line, column=column, path=path)
        completions = script.completions()
        self.completions = completions

        idx = 0
        result = []
        for c in completions:
            if not c.in_builtin_module():
                followed = list(c._name.infer())
            d = dict(name=c.name,
                        index=idx,
                        name_with_symbols=c.name_with_symbols,
                        type=c.type,
                        description=c.description,
                        docstring=c.docstring(),  # docstr
                        )
            idx = idx + 1
            result.append(d)
        return result

    def comletionResolve(self, index):
        completion = self.completions[index]
        if completion is None:
            return None
        doc = completion.docstring(raw=False, fast=False)
        return None
