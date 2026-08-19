import serial
import time

class K8090:

    def __init__(self, port='/dev/ttyACM0'):
        self.ser = serial.Serial(
            port     = port,
            baudrate = 19200,
            bytesize = serial.EIGHTBITS,
            parity   = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout  = 1
        )

    def _send_command(self, cmd, mask=0x00, param1=0x00, param2=0x00):
        stx = 0x04
        etx = 0x0F
        chk = (0x100 - ((stx + cmd + mask + param1 + param2) & 0xFF)) & 0xFF
        packet = bytes([stx, cmd, mask, param1, param2, chk, etx])
        self.ser.write(packet)
        self.ser.flush()

    def relay_on(self, mask):
        self._send_command(0x11, mask)

    def relay_off(self, mask):
        self._send_command(0x12, mask)

    def relay_toggle(self, mask):
        self._send_command(0x14, mask)

    def close(self):
        self.ser.close()

if __name__ == "__main__":

    # Edit port if needed (/dev/ttyACM0 or /dev/ttyUSB0 or COMx)
    k8090 = K8090(port='/dev/ttyACM0')
    
    # Example
    cnt = 0
    while cnt < 5:
        print("Relay 1 ON")
        k8090.relay_on(0x01)
        time.sleep(1)
        print("Relay 1 OFF and relay 2 ON")
        k8090.relay_off(0x01)
        k8090.relay_on(0x02)
        time.sleep(1)
        print("All relays OFF")
        k8090.relay_off(0xFF)
        time.sleep(0.3)
        print("All relays ON")
        k8090.relay_on(0xFF)
        time.sleep(0.3)
        print("All relays OFF")
        k8090.relay_off(0xFF)
        time.sleep(0.3)
        cnt = cnt + 1
    
    k8090.close()
