import os
import pty
import select
import time


class Emulator:
    def __init__(self, fd):
        self._fd = fd
        self._echo_on = True

    def wait_for_slave(self):
        """Wait for the slave process to connect

        It appears the one way to detect this is to monitor
        the status of the HUP signal
        """
        poll = select.poll()
        poll.register(self._fd, select.POLLHUP)
        while True:
            time.sleep(1)
            events = poll.poll(10)
            if len(events) == 0:
                break
        print("Slave has arrived")
        self.send_prompt()

    def send_prompt(self):
        os.write(self._fd, b"\r>")
        print("OUT> {}".format(b"\r>"))
#        os.fsync(self._fd)

    def run(self):
        self.wait_for_slave()
        data = b""
        while True:
            data = data + os.read(self._fd, 512)
            print("RAW ", data)
            while True:
                idx = data.find(b"\r")
                if idx >= 0:
                    cmd = data[:idx]
                    data = data[idx+1:]
                    self.process(cmd)
                else:
                    break

    def process(self, cmd):
        if self._echo_on:
            os.write(self._fd, cmd)
            os.write(self._fd, b"\r")
        cmd = cmd.decode("ascii")
        cmd = cmd.upper()
        if cmd.startswith("AT") or cmd.startswith("@"):
            self.action_at_cmd(cmd)
        else:
            squeezed = "".join(cmd.split())
            octets = []
            for i in range(0, len(squeezed), 2):
                octets.append(int(squeezed[i:i+2],base=16))
            self.action_obd_cmd(octets)

    def action_at_cmd(self, cmd):
        tokens = cmd.split(maxsplit=1)
        if len(tokens) > 1:
            param = tokens[1]
        else:
            param = None
        print(cmd)
        func = getattr(self, "_action_{}".format(cmd))
        func(param)

    def send_response(self, response):
        os.write(self._fd, response.encode("ascii"))
        print("OUT> {}".format(response.encode("ascii")))
        self.send_prompt()

    def _action_ATZ(self, param):
        self._echo_on = True
        self.send_response("ELM327 v1.5")

    def _action_ATIGN(self, param):
        self.send_response("ON")

    def _action_ATRV(self, param):
        self.send_response("12.5V")

    def action_obd_cmd(self, octets):
        mode = octets[0]
        getattr(self, "_action_mode{}".format(mode))(octets)

    def _action_mode1(self, octets):
        octets[0] |= 0x40
        if octets[1] == 0x20:
            octets += [0x80, 0x00, 0x00, 0x00]
        else:
            octets += [0xBE, 0x3E, 0xF8, 0x11]
        self.send_response(" ".join(["%02X" % x for x in octets]))
       
    def _action_0101(self, param):
        self.send_response("41 01 BE 3E F8 11")

    def _action_0103(self, param):
        self.send_response("41 03 BE 3E F8 11")

    def _action_0104(self, param):
        self.send_response("41 04 BE 3E F8 11")

    def _action_0105(self, param):
        self.send_response("41 05 BE 3E F8 11")

    def _action_0120(self, param):
        self.send_response("41 20 80 00 00 00")

    def _action_obd_cmd(self):
        """Series of hexadecimal string"""

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
