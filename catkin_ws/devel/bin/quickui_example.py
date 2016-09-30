#!/usr/bin/env python
# creates a relay to a python script source file, acting as that file.
# The purpose is that of a symlink
with open("/home/ubuntu/catkin_ws/src/quickui/scripts/quickui_example.py", 'r') as fh:
    exec(fh.read())
