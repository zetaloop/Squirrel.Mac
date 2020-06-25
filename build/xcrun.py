#!/usr/bin/env python3
from __future__ import print_function
import os
import subprocess
import sys

SOURCE_ROOT = os.path.dirname(os.path.dirname(__file__))
cmd = "xcrun"
args = [cmd] + sys.argv[1:]
try:
    subprocess.check_output(args, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as e:
    print("xcrun script '" + ' '.join(sys.argv[1:]) + "' failed with code '" + str(e.returncode) + "':\n" + e.output)
    sys.exit(e.returncode)
