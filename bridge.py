import atexit
import os
import subprocess
import sys
import random

#IMPORTANT: This is set up for a 7x6 board only. THere is a file called 7x6.book that has a lot of pre determined moves for the start of the game
# because the minimax functions will take a long time otherwise. After the first 2-5 moves for a given board, the process speeds up anyway so
# the "book" isnt needed

#gets path
_SOLVER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "connect4-master") 
#gets file name
_EXE_NAME = "c4solver.exe" if sys.platform.startswith("win") else "c4solver" 
_proc = None


def _start():
    global _proc
    exe = os.path.join(_SOLVER_DIR, _EXE_NAME)
    #none of this matters as long as you have the Pascals folder
    if not os.path.exists(exe): 
        raise FileNotFoundError(
            f"{exe} not found. Build it first:\n"
            #this is in case you dont. It compiles the c4solver referencing the main c++ file and the solver
            f"  cd connect4-master && g++ --std=c++11 -O3 -DNDEBUG -o c4solver main.cpp Solver.cpp" 
        )
    _proc = subprocess.Popen(
        [exe, "-a", "-b", os.path.join(_SOLVER_DIR, "7x6.book")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    ) #opens the process to the thingy. It should keep this open for however long
    atexit.register(_stop)

#self explanatory
def _stop(): 
    if _proc and _proc.poll() is None:
        _proc.kill()

#gets the scores from teh c++ files using th process
def column_scores(moves):
    if _proc is None or _proc.poll() is not None:
        _start()
    #solver uses 1234567 so it changes the columns to that stuff
    seq = "".join(str(c + 1) for c in moves)
    _proc.stdin.write(seq + "\n")
    _proc.stdin.flush()
    reply = _proc.stdout.readline().split()
    #return looks like: "[usless to me, 0, 1, 2, 3, 4, 5, 6]"
    #print(reply)
    #last 7
    scores = reply[-7:] 
    if len(scores) != 7:
        raise RuntimeError(f"Solver rejected move sequence {seq!r} (game already over?)")
    return [int(s) for s in scores]


def best_move(moves):
    scores = column_scores(moves)
    #returns the maximum of the 7 cols for the best column
    highest = scores[0]
    col = 0
    for i in range(1,7):
        if scores[i] > highest:
            highest = scores[i]
            col = i
        elif scores[i] == highest:
            if random.randint(0, 1) == 1:
                highest = scores[i]
                col = i
    return col