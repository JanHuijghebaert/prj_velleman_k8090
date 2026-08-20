# Author : Jan Huijghebaert (2026)

import serial
import threading
import time

class K8090:

    def __init__(self, port='/dev/ttyACM0'):
        self.ser = serial.Serial(
            port     = port,
            baudrate = 19200,
            bytesize = serial.EIGHTBITS,
            parity   = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout  = 0.5
        )
        self.listenerActive = False
        self.listenerThread = None
        print("Serial opened")

    def serialClose(self):
        self.ser.close()
        print("Serial closed")

    def _serialTx(self, cmd, mask=0x00, param1=0x00, param2=0x00):
        stx = 0x04
        etx = 0x0F
        chk = (0x100 - ((stx + cmd + mask + param1 + param2) & 0xFF)) & 0xFF
        packet = bytes([stx, cmd, mask, param1, param2, chk, etx])
        self.ser.write(packet)
        self.ser.flush()
        time.sleep(0.01)

    def serialListenerStart(self):
        self.listenerActive = True
        self.listenerThread = threading.Thread(target=self._serialListenerLoop, daemon=True)
        self.listenerThread.start()
        print("Serial listener running...")

    def serialListenerStop(self):
        self.listenerActive = False
        if self.listenerThread:
            self.listenerThread.join()
        print("Serial listener stopped")

    def _serialListenerLoop(self):
        buffer = bytearray()
        while self.listenerActive:
            if self.ser.in_waiting > 0:
                char = self.ser.read(1)
                if char:
                    buffer.extend(char)
            else:
                time.sleep(0.01) # Avoid 100% CPU usage
                continue
            while len(buffer) >= 7:
                if buffer[0] != 0x04:
                    buffer.pop(0)
                    continue
                if buffer[6] != 0x0F:
                    buffer.pop(0)
                    continue
                packet = bytes(buffer[:7])
                del buffer[:7]
                self._serialHandleResponse(packet)
    
    def _serialHandleResponse(self, packet):
        cmd    = packet[1]
        mask   = packet[2]
        param1 = packet[3]
        param2 = packet[4]
        if cmd == 0x50:
            if mask == 0:
                print(f"[RX] Button {self._translate_mask_to_ids(param2)} released")
            else:
                print(f"[RX] Button {self._translate_mask_to_ids(param1)} pushed")
        elif cmd == 0x51:
            print(f"[RX] Status - Closed: {self._translate_mask_to_ids(param1)}")
        elif cmd == 0x70:
            print(f"[RX] Factory defaults - " + str(list(packet)))
        elif cmd == 0x71:
            print(f"[RX] Firmware: Year 20{param1:02d}, Week {param2:02d}")
        else:
            print(f"[RX] Unknown - CMD 0x{cmd:02X} - " + str(list(packet)))

    def _translate_mask_to_ids(self, mask):
        active = [str(i+1) for i in range(8) if (mask & (1 << i))]
        return ", ".join(active) if active else "None"

    ##################################################
    # Commands
    ##################################################

    def cmdResetFactoryDefault(self):
        print(f"[TX] CMD Reset factory defaults")
        self._serialTx(0x70)

    def cmdGetFirmware(self):
        print(f"[TX] CMD Get firmware")
        if self.listenerActive:
            self._serialTx(0x71)
        else:
            self.ser.reset_input_buffer()
            self._serialTx(0x71)
            self._serialHandleResponse(self.ser.read(7))

    def cmdRelayClose(self, mask):
        print(f"[TX] CMD Relay close (ID: {self._translate_mask_to_ids(mask)})")
        self._serialTx(0x11, mask)

    def cmdRelayOpen(self, mask):
        print(f"[TX] CMD Relay open (ID: {self._translate_mask_to_ids(mask)})")
        self._serialTx(0x12, mask)

    def cmdRelayToggle(self, mask):
        print(f"[TX] CMD Relay toggle (ID: {self._translate_mask_to_ids(mask)})")
        self._serialTx(0x14, mask)
    
    def cmdGetStatus(self):
        print(f"[TX] CMD Get status")
        if self.listenerActive:
            self._serialTx(0x18)
        else:
            self.ser.reset_input_buffer()
            self._serialTx(0x18)
            self._serialHandleResponse(self.ser.read(7))
