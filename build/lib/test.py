__author__ = 'Jan'

import os
import subprocess
import sys

do_compile = False

for arg in sys.argv:
    if arg == "-c":
        do_compile = True


bots = []
# makes the project directory the working directory
os.chdir(os.path.expanduser("~") + "\IdeaProjects\supersecret\src")

if do_compile:
    print("compiling")
    subprocess.call(["javac", "*.java"])

BOTS = {"BullyBot": "example_bots/BullyBot.jar",
        "DualBot": "example_bots/DualBot.jar",
        "ProspectorBot": "example_bots/ProspectorBot.jar",
        "RageBot": "example_bots/RageBot.jar",
        "RandomBot": "example_bots/RandomBot.jar"
        }

def run_game(map, opponent):
    """
    Runs the game engine
    :param map: Number of the map to play on
    :param opponent: Location of the Jar file containing the opponent
    :return: A tuple containing a boolean descibing if the bot has won and the amount of turns.
    """
    MAP = 'maps/map' + str(map) + ".txt"
    import subprocess
    # call the game engine
    process = subprocess.Popen(["java", "-jar", "tools/PlayGame.jar", MAP ,"1000", "1000", "log.txt", "java MyBot", "java -jar " + opponent + '"']
                           , stderr=subprocess.PIPE
                           , stdout=subprocess.PIPE
                           )

    for line in process.stderr:
        if line.startswith(b"Turn"):
            turn = line
        if line.startswith(b"Player"):
            # Split the turn and keep the number
            turn = turn.decode("utf-8").split(' ')[1]
            # Remove the line ending
            turn = turn[:turn.find('\r\n')]
            # Determine whether the bot has won
            if line.startswith(b"Player 1"):
                won = True
            else:
                won = False
            return (won, int(turn))

mapnumbers = range(1,100)
results = []
for mapnumber in mapnumbers:
    print("test", mapnumber)
    results.append(run_game(mapnumber, BOTS["ProspectorBot"]))

print(results)

