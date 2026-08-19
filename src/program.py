# Brief  : Velleman K8090 Python command script
# Author : Jan Huijghebaert
import serial
import time

class K8090:

    ##################################################
    # Serial functions
    ##################################################

    # Open serial terminal
    def __init__(self, port='/dev/ttyACM0'):
        self.ser = serial.Serial(
            port     = port,
            baudrate = 19200,
            bytesize = serial.EIGHTBITS,
            parity   = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout  = 1
        )
    
    # Close serial terminal
    def serialClose(self):
        self.ser.close()

    # Send serial command
    def _serialSend(self, cmd, mask=0x00, param1=0x00, param2=0x00):
        stx = 0x04
        etx = 0x0F
        chk = (0x100 - ((stx + cmd + mask + param1 + param2) & 0xFF)) & 0xFF
        packet = bytes([stx, cmd, mask, param1, param2, chk, etx])
        self.ser.write(packet)
        self.ser.flush()
        time.sleep(0.01)
    
    # Send and receive serial command
    def _serialSendAndReceive(self, cmd, mask=0x00, param1=0x00, param2=0x00):
        self.ser.reset_input_buffer()
        self._serialSend(cmd)
        response = self.ser.read(7)
        print(list(response))
        return response

    ##################################################
    # Board functions
    ##################################################

    def boardResetFactoryDefaults(self):
        self._serialSend(0x70)

    def boardGetFirmware(self):
        response = self._serialSendAndReceive(0x71)

    ##################################################
    # Relay functions
    ##################################################

    def relayOn(self, mask):
        self._serialSend(0x11, mask)

    def relayOff(self, mask):
        self._serialSend(0x12, mask)

    def relayToggle(self, mask):
        self._serialSend(0x14, mask)
    
    # Return a list of status booleans
    def relayGetStatus(self):
        response = self._serialSendAndReceive(0x18)
        if len(response) == 7 and response[0] == 0x04 and response[6] == 0x0F:
            mask = response[2]
            bool_list = []
            for i in range(8):
                bool_list.append(bool(mask & (1 << i)))
            return bool_list
        else:
            print("Error, no valid query response")
            return [False] * 8

if __name__ == "__main__":

    # Edit port if needed (/dev/ttyACM0 or /dev/ttyUSB0 or COMx)
    k8090 = K8090(port='/dev/ttyACM0')

    k8090.boardResetFactoryDefaults()
    k8090.boardGetFirmware()
    
    # Example
    # All off
    k8090.relayOff(0xFF)

    # Test relay 3 with on/off
    cnt = 0
    while cnt < 3:
        k8090.relayOn(0x04)
        time.sleep(0.3)
        k8090.relayOff(0x04)
        time.sleep(0.3)
        cnt = cnt + 1
    
    # Test relay 7 with toggle
    cnt = 0
    while cnt < 6:
        k8090.relayToggle(0x40)
        time.sleep(0.3)
        cnt = cnt + 1
    
    # Test get relay status
    print(k8090.relayGetStatus())
    time.sleep(0.3)
    k8090.relayOn(0x55)
    time.sleep(0.3)
    cnt = 0
    while cnt < 6:
        print(k8090.relayGetStatus())
        time.sleep(0.3)
        k8090.relayToggle(0xFF)
        time.sleep(0.3)
        cnt = cnt + 1
    k8090.relayOff(0xFF)
    time.sleep(0.3)
    
    k8090.serialClose()
