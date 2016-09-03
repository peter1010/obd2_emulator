import os
import pty
import select
import time

class Emulator:
    def __init__(self, fd):
        self._fd = fd

    def run(self):
        data = b""
        while 1:
            time.sleep(1)
            poll = select.poll()
            poll.register(self._fd, select.POLLHUP)
            events = poll.poll(10)
            if len(events) == 0:
                break
        print("Slave has arrived")
        while True:
            data = data + os.read(self._fd, 512)
            while True:
                idx = data.find(b"\r")
                if idx >= 0:
                    cmd = data[:idx]
                    data = data[idx+1:]
                    self.process(cmd)

    def process(self, cmd):
        print(cmd)


def main():
    master_fd, slave_fd = pty.openpty()
    slave_name = os.ttyname(slave_fd)
    os.close(slave_fd)
    print(slave_name)
#    fp = open(slave_name, "wb")
    app = Emulator(master_fd)
    app.run()


if __name__ == "__main__":
    main()
