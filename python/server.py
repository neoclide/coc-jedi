# -*- coding: utf-8 -*-

import sys
import logging
import tempfile
import os

from pynvim import attach

def setup_logging():
    """Setup logging according to environment variables."""
    logfile = os.path.join(tempfile.gettempdir(), 'coc-jedi.log')
    level = logging.INFO
    if 'COC_JEDI_LOG_LEVEL' in os.environ:
        lvl = getattr(logging, os.environ['COC_JEDI_LOG_LEVEL'].strip(), level)
        if isinstance(lvl, int):
            level = lvl
    logging.basicConfig(filename=logfile, level=level, format=(
        '%(asctime)s [%(levelname)s @ '
        '%(filename)s:%(funcName)s:%(lineno)s] %(process)s - %(message)s'))


setup_logging()

from plugin import Plugin

if "VIM_NODE_RPC" in os.environ:
    nvim = attach('socket', path=os.environ['NVIM_LISTEN_ADDRESS'])
else:
    nvim = attach('stdio')

plugin = Plugin(nvim)

IS_PYTHON3 = sys.version_info >= (3, 0)

if IS_PYTHON3:
    unicode_errors_default = 'surrogateescape'
else:
    unicode_errors_default = 'strict'

logger = logging.getLogger(__name__)
error, debug, info, warn = (logger.error, logger.debug, logger.info,
                            logger.warning,)

def decode_if_bytes(obj, mode=True):
    """Decode obj if it is bytes."""
    if mode is True:
        mode = unicode_errors_default
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors=mode)
    return obj


def _on_request(name, args):
    if IS_PYTHON3:
        name = decode_if_bytes(name)
    debug("request: %s, args: %s", name, args)
    fn = getattr(plugin, name, None)
    if fn is None:
        nvim.err_write("Can't find method {}".format(name), async_=True)
        return None
    return fn(*args)


def _on_notification(name, args):
    if IS_PYTHON3:
        name = decode_if_bytes(name)
    debug("notification: %s, args: %s", name, args)
    if name == 'nvim_async_request_event':
        [idx, method, arguments] = args
        fn = getattr(plugin, method, None)
        if fn is None:
            msg = "Can't find method {}".format(method)
            nvim.call('coc#jedi#async_response', idx, msg, 1, async_=True)
            return
        try:
            result = fn(*arguments)
            debug("result: %s", result)
            nvim.call('coc#jedi#async_response', idx, result, False, async_=True)
        except Exception as e:
            nvim.call('coc#jedi#async_response', idx, e, True, async_=True)
        return
    fn = getattr(plugin, name, None)
    if fn is None:
        nvim.err_write("Can't find method {}".format(name), async_=True)
    else:
        fn(*args)


def _on_setup():
    version = {"major": 0, "minor": 1, "patch": 0}
    nvim.api.set_client_info("jedi", version, "remote", {}, {}, async_=True)
    nvim.command("let g:coc_jedi_channel_id={}".format(nvim.channel_id),async_=True)

def _on_error(msg):
    nvim.err_write(msg, async_=True)


nvim.run_loop(
        _on_request,
        _on_notification,
        _on_setup,
        err_cb=_on_error,
        )

# nvim.close()
