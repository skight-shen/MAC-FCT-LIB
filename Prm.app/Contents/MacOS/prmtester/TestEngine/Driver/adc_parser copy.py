import sys
import socket
import time
import os
import platform
import argparse

log_path = "/vault/PRM_Log/"


class AdcParser(object):
    def __init__(self):
        self.sock = None
        # self.adc_convert_func = adc_convert_func
        self.frame_id = 0
        self.payload_width = 0

    def connect_to_server(self, server_ip, server_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((server_ip, server_port))
        except Exception as e:
            print("connect error: %r" % e)
            return False
        return True

    def get_cur_dir_path(self):
        spit = '/'
        cur_dir = os.getcwd()
        if 'Windows' == platform.system():
            spit = "\\"
        log_file_path = cur_dir + spit
        return log_file_path

    def adc_data_convert_2_voltage(self, data):
        gain = 0x555555
        offset = 0x800000
        vref = 5000.0
        vin = ((data - 0x80000000) * 0x400000 / gain + offset - 0x800000) \
              * vref / (2 ** 23 * 0.75)
        return vin  # mV

    def show_recv_speed(self):
        pass

    def convert_time(self, utc_time_s, utc_time_ms):
        local_time = time.localtime(utc_time_s)
        date_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        time_stamp = "%s.%03d" % (date_head, utc_time_ms)

        return time_stamp

    def recv_data_and_save_log(self, log_file_name):
        # log_file_path = self.get_cur_dir_path()
        file = log_path + str(log_file_name).strip()
        buf = []
        buf += [int(ord(i)) for i in self.sock.recv(16)]
        print(buf)
        self.frame_id = buf[3] << 8 | buf[2]
        print("frame_id: ", self.frame_id)
        with open(file, "w") as f:
            print(file)
            # csvwriter = csv.writer(f, delimiter=',')
            while True:
                data = self.sock.recv(1024000)
                print('len' + str(len(data)))
                buf += [int(ord(i)) for i in data]
                payload_len = buf[15] << 8 | buf[14]
                if (payload_len * 4 + 16 + 4) < len(buf):
                    self.payload_width = (buf[1] >> 4) & 0xF
                    if self.frame_id != buf[3] << 8 | buf[2]:
                        print("frame_id error!")
                        exit()
                    else:
                        self.frame_id += 1
                    sample_rate = buf[5] | buf[6] << 8 | buf[7] << 16
                    step = 1000.0 / sample_rate * 2
                    utc_time_s = (buf[8] | buf[9] << 8 | buf[10] << 16 | \
                                  buf[11] << 24)
                    utc_time_ms = (buf[12] | buf[13] << 8)
                    adc_data_list = buf[:payload_len + 16 + 4]
                    buf = buf[payload_len + 16 + 4:]
                    adc_data_list = adc_data_list[16:-4]
                    while adc_data_list:
                        adc_data = 0
                        for i in range(self.payload_width):
                            adc_data |= adc_data_list.pop(0) << (i * 8)
                        voltage = self.adc_data_convert_2_voltage(adc_data)
                        # calculate timestamp for log
                        # utc_time_ms_ = utc_time_ms + step * index
                        utc_time_ms += step
                        if utc_time_ms >= 1000:
                            utc_time_ms -= 1000
                            utc_time_s += 1
                        time_stamp = self.convert_time(utc_time_s, utc_time_ms)
                        # index += 1
                        f.write(time_stamp + "," + str(voltage) + "\n")
                else:
                    print('payload:' + str(payload_len * 4 + 16 + 4))
                    print('buflen' + str(len(buf)))

def sync_time(server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(server_ip, server_port)
        sock.connect((server_ip, server_port))
    except Exception as e:
        print("connect error: %r" % e)
        return False
    utc = time.time()
    utc_s = str(int(utc))
    utc_ms = str(int(utc * 1000 % 1000))

    cmd = "[1]synctime(-w,%s,%s)\r\n" % (utc_s, utc_ms)
    sock.send(cmd.encode("utf-8"))
    # time.sleep(1)
    # sock.send('[11]datalogger open(all)\r\n')

    recv_data = sock.recv(1024)
    print(recv_data)
    sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', default='169.254.1.33')
    parser.add_argument('-p', '--port', type=int, default=7610)
    parser.add_argument('-a', '--addr', default='datalog.csv')
    args = parser.parse_args()


    adc_parser = AdcParser()
    sync_time(args.ip, 7600)
    ret = adc_parser.connect_to_server(args.ip, args.port)
    if ret is False:
        exit()

    adc_parser.recv_data_and_save_log(args.addr)
