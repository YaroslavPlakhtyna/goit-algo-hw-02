from threading import Condition, Thread
from queue import Queue, Empty
from uuid import uuid4


queue = Queue()
condition = Condition()


def generateRequests():
    print("Start requests generation.")
    while True:
        new_request = uuid4()
        print("Adding new request:", new_request)
        queue.put(new_request)
        with condition:
            if condition.wait(timeout=1):
                print("Stop requests generation.")
                break


def processRequests():
    print("Start requests processing.")
    while True:
        try:
            print("Processing request:", queue.get(block=False))
        except Empty:
            print("No requests available.")
        with condition:
            if condition.wait(timeout=1):
                print("Stop requests processing.")
                break


def main():
    generator = Thread(target=generateRequests)
    processor = Thread(target=processRequests)

    print("Starting request processing emulation, press any key to stop...")

    generator.start()
    processor.start()

    input()
    with condition:
        condition.notify_all()

    generator.join()
    processor.join()

    print("Finished.")


if __name__ == "__main__":
    main()