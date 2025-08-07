import serial

BAUDRATE = 115200


def find_mbot_port(self):
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "CH340" in port.description:
            return port.device
    return None
