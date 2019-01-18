import threading
import select
import errno

import logging
import socket


class HB(threading.Thread):
    def __init__(self, seconds, publisher):
        super(HB, self).__init__()
        self.seconds = seconds
        self.publisher = publisher
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        while True:
            try:
                r, w, e = select.select([self.sock], [], [], self.seconds)
            except (OSError, select.error) as e:
                if e.args[0] != errno.EINTR:
                    raise

            #logging.warn("heart beat")
            self.publisher.publish('Heart Beat')

if __name__ == '__main__':
    FORMAT = "%(asctime)s %(levelname)s %(filename)s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    hb = HB(5, None)
    hb.start()