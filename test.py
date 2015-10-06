from os import chdir
from os.path import expanduser
from subprocess import call, Popen, PIPE
from sys import argv

# Dictionary containing all opponent bots.
BOTS = {"BullyBot": "example_bots/BullyBot.jar",
        "DualBot": "example_bots/DualBot.jar",
        "ProspectorBot": "example_bots/ProspectorBot.jar",
        "RageBot": "example_bots/RageBot.jar",
        "RandomBot": "example_bots/RandomBot.jar"
        }


chdir(expanduser("~") + "\IdeaProjects\supersecret\src")


def check_compile_java():
    do_compile = False
    # checks if the -c token has been set.
    for arg in argv:
        if arg == "-c":
            do_compile = True

    # makes the project directory the working directory.
    if do_compile:
        # if the -c token has been set. Compile all java code in the directory.
        print("compiling")
        call(["javac", "*.java"])


def run_game(map_number, opponent):
    """
    Runs the game engine.
    :param map_number: Number of the map to play on.
    :param opponent: Location of the Jar file containing the opponent.
    :return: A tuple containing a boolean descibing if the bot has won and the amount of turns.
    """
    # Turns the map parameter into a string the game engine understands.
    map_file = 'maps/map' + str(map_number) + ".txt"
    # call the game engine
    process = Popen(["java", "-jar", "tools/PlayGame.jar", map_file, "1000", "1000", "log.txt", "java MyBot",
                     "java -jar " + opponent + '"'],
                    stderr=PIPE,
                    stdout=PIPE
                    )

    for line in process.stderr:
        if line.startswith(b"Turn"):
            # stores the amount of turns taken. Only the last one is kept.
            turn = line
        # Checks whether the game is finished
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
            return won, int(turn)


def test100(bot):
    # Make a range going from 1 to 100
    mapnumbers = range(1, 100)
    results = []

    # run MyBot against ProspectorBot in map 1 to map 100.
    for mnumber in mapnumbers:
        print("test", mnumber)
        # Save the results
        results.append(run_game(mnumber, bot))

    return results
