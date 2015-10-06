import test
import multiprocessing
from queue import Empty


def processfunction(mapnumbers):
    print(mapnumbers)
    for number in mapnumbers:
        result = test.run_game(number, test.BOTS["DualBot"])
        result_queue.put(result)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    threadNum = 3

    # Valid mapnumbers 1 to 100
    maps = list(range(1, 101))

    result_queue = multiprocessing.Queue()

    i = 0
    while i < threadNum:
        print(int(i * len(maps) / (threadNum + 1)), int(len(maps) / (threadNum + 1) + i * len(maps) / (threadNum + 1)))
        multiprocessing.Process(target=processfunction,
                                args=([maps[int(i * len(maps) / (threadNum + 1)): int(
                                    len(maps) / (threadNum + 1) + i * len(maps) / (threadNum + 1))]])).run()
        i += 1

    listening = True
    results = []
    while listening:
        try:
            result = result_queue.get(True, 5)
            results.append(result)
        except Empty:
            listening = False

    print(len(results))

    print(results)
