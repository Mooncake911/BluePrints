import serial
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo

from threading import Lock
from queue import Queue, Empty

from PySide6.QtCore import QThread, Signal


from db.redis_db import redis_manager


def string_to_dict(line: str):
    # TODO: этой функции быть не должно, всё из-за пустых пакетов без доп-информации
    import json
    start_index = line.find('{')
    end_index = line.rfind('}')

    # Check if { and } were found
    if start_index != -1 and end_index != -1:
        json_str = line[start_index:end_index + 1]

        try:
            json_dict = json.loads(json_str)
            if json_dict.get('id') and json_dict.get('name'):
                return json_dict.get('name'), json_dict
            else:
                return None, None

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON {e}")
            return None, None

    else:
        return None, None


class SerialPort(QThread):
    stop_flag = False

    new_data = Signal(str)
    encoding = 'utf-8'

    def __init__(self, port=None, baud_rate=115200, timeout=1):
        super().__init__()
        self.serial = serial.Serial()
        self.initSerial(port, baud_rate, timeout)
        self.queue = Queue()
        self.lock = Lock()

    def initSerial(self, port, baud_rate=115200, timeout=1):
        self.stop_flag = False
        self.serial.port = port
        self.serial.baudrate = baud_rate
        self.serial.timeout = timeout

    def run(self):
        while not self.stop_flag:
            if self.serial.is_open:
                # Writing
                try:
                    with self.lock:
                        self.write()
                except serial.SerialTimeoutException as e:
                    print(f"Serial timeout error while writing: {e}")
                except serial.SerialException as e:
                    print(f"Error while writing: {e}")
                except Exception as e:
                    print(f"Unexpected error while writing: {e}")

                # Reading
                try:
                    with self.lock:
                        self.read()
                except serial.SerialTimeoutException as e:
                    print(f"Serial timeout error while reading: {e}")
                except serial.SerialException as e:
                    print(f"Error while reading: {e}")
                except Exception as e:
                    print(f"Unexpected error while reading: {e}")
            else:
                try:
                    self.serial.open()
                except serial.SerialException as e:
                    print(f"Error while opening serial port: {e}")
                except Exception as e:
                    print(f"Unexpected error while opening serial port: {e}")

    def is_open(self):
        return self.serial.is_open

    def close(self):
        self.stop_flag = True
        self.serial.close()

    def put(self, data):
        self.queue.put(data)

    def write(self):
        try:
            data = self.queue.get(timeout=0.1)
            self.serial.write(data.encode(self.encoding))
            self.queue.task_done()
            # print(f'Write: {data}')
        except Empty:
            pass

    def read(self):
        while self.serial.in_waiting:
            data = self.serial.readline().decode(self.encoding).strip()
            if data:
                self.new_data.emit(data)
                key, data = string_to_dict(data)
                if data:
                    redis_manager.set(key=key, data=data)
                # add_device_config(data)
                # print(f'Read: {data}')

    @staticmethod
    def listSerialPort() -> list[ListPortInfo]:
        ports_list = []
        ports = list_ports.comports()
        for port, desc, hwid in sorted(ports):
            ports_list.append(port)
        return ports_list


serial_port = SerialPort()  # Serial Port is common for all widgets
