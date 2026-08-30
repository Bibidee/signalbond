import atexit
import os
import sys

def warp_to(direct_vm, value: str) -> None:
    direct_vm.warp(value)
    gl = sys.modules.get("genlayer.gl")
    if gl is not None and isinstance(getattr(gl, "message_raw", None), dict):
        gl.message_raw["datetime"] = value

if sys.platform == "win32":
    from gltest.direct import loader as _loader
    _leaked, _unlink = [], os.unlink
    def _tolerant(path, *args, **kwargs):
        try: return _unlink(path)
        except PermissionError: _leaked.append(os.fspath(path))
    _original = _loader._inject_message_to_fd0
    def _inject(vm):
        os.unlink = _tolerant
        try: return _original(vm)
        finally: os.unlink = _unlink
    _loader._inject_message_to_fd0 = _inject
    @atexit.register
    def _sweep():
        for path in _leaked:
            try: _unlink(path)
            except OSError: pass
