import sys


def appendPydevRemoteDebugger():
    try:
        sys.path.append(
            "D:\\Kodi\\eclipse-cpp-mars-R-win32-x86_64\\eclipse\\plugins\\org.python.pydev_4.3.0.201508182223\\pysrc")
        import pydevd
        # import pysrc.pydevd as pydevd # with the addon script.module.pydevd, only use `import pydevd`
        # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
        print('pydevd funcou')
        # pydevd.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: "+"You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)