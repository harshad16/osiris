# Osiris: Build log aggregator.

"""Utils module."""

import shlex
import subprocess
import sys
import typing

from functools import wraps
from http import HTTPStatus

from thoth.osiris.exceptions import OCAuthenticationError


def oc_authentication_required(f):
    """Wrap endpoint which requires authentication."""

    @wraps(f)
    def inner(*args, **kwargs):
        out, _, ret_code = execute_command("oc whoami")

        if ret_code > 0:
            raise OCAuthenticationError(out)

        return f(*args, **kwargs)

    return inner


def format_status_message(status: HTTPStatus) -> str:
    """Return formated status message."""
    return f"{status}, {status.phrase}"


def execute_command(command: str) -> tuple:
    """Split safely and execute command as a subprocess."""
    command = shlex.split(command)

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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


from datetime import datetime


def from_resources(resource, build_id: str = None):
    """Create BuildInfo model from kubernetes event."""
    metadata = resource["metadata"]
    status = resource["status"]

    datetime_fmt = "%Y-%m-%dT%H:%M:%SZ"
    try:  # might be missing if build is in Pending state
        start_ts = datetime.strptime(status["startTimestamp"], datetime_fmt)
        end_ts = datetime.strptime(status["completionTimestamp"], datetime_fmt)
    except KeyError:
        start_ts = None
        end_ts = None

    return
