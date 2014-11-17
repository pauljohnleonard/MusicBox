from MB import MB
import subprocess

context=MB.Context()
melody_player=context.create_player(chan=1,pipe_to_beat=False)
melody_player.set_instrument('Piano')

map={"melody":melody_player.play}
        
context.start(map)  

pid=subprocess.Popen([MB.PYTHON_CMD, "pg_ui.py"])

