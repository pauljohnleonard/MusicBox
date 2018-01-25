"""
DEPRECATED OR FIX ME
"""
import sys
sys.path.append(sys.path[0] + "/..")

from src.MB.context import Context
from src.MB.setup import PYTHON_CMD

import subprocess

context=Context()
melody_player=context.create_player(chan=1,pipe_to_beat=False)
melody_player.set_instrument('Piano')

map={"melody":melody_player.play}
        
context.start(map)  

pid=subprocess.Popen([PYTHON_CMD, "pg_ui.py"])

