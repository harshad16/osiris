# Osiris: Build log aggregator.

"""Utils module."""

import shlex
import subprocess
import sys
import typing

from http import HTTPStatus


def format_status_message(status: HTTPStatus) -> str:
    """Return formated status message."""
    return f"{status}, {status.phrase}"


def execute_command(command: str) -> tuple:
    """Split safely and execute command as a subprocess."""
    command = shlex.split(command)

    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    out: bytes
    err: bytes

    out, err = proc.communicate()
    ret_code: int = proc.wait()

    return out, err, ret_code


def suppress_exception(exc_type=Exception):
    """Suppress exception."""

    def _wrapper(fun: typing.Callable):

        def _inner(*args, **kwargs):

            ret = None
            # noinspection PyBroadException
            try:
                ret = fun(*args, **kwargs)
            except exc_type as exc:
                # TODO: log caught exception warnging
                print("[WARNING] Exception caught:", exc, file=sys.stderr)

            return ret

        return _inner

    return _wrapper


def noexcept(fun: typing.Callable):
    """Decorate non-throwing function."""

    def _inner(*args, **kwargs):

        ret = None
        # noinspection PyBroadException
        try:
            ret = fun(*args, **kwargs)
        except Exception as exc:
            # TODO: log caught exception warnging
            print("[WARNING] Exception caught:", exc, file=sys.stderr)

        return ret

    return _inner
