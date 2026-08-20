from k8090 import K8090
import time

def runDemo(k8090):
    # Checks
    k8090.cmdResetFactoryDefault()
    k8090.cmdGetFirmware()
    # All relays open
    k8090.cmdRelayClose(0xFF)
    time.sleep(0.5)
    k8090.cmdRelayOpen(0xFF)
    # Counter
    cnt = 0
    # Loop relay 3 on/off
    while cnt < 3:
        k8090.cmdRelayClose(0x04)
        time.sleep(0.2)
        k8090.cmdRelayOpen(0x04)
        time.sleep(0.2)
        cnt = cnt + 1
    cnt = 0
    # Loop relay 5 toggle
    while cnt < 7:
        k8090.cmdRelayToggle(0x10)
        time.sleep(0.2)
        cnt = cnt + 1
    cnt = 0
    # Get relay status
    k8090.cmdGetStatus()
    time.sleep(0.3)
    # Open all relays (for button test)
    k8090.cmdRelayOpen(0xFF)
    print(f"You can now perform button tests for 10 seconds...")
    time.sleep(10) # <Perform button test>
    print(f"End of test")
    k8090.cmdRelayOpen(0xFF)
    time.sleep(0.3)
    # Loop all relays
    k8090.cmdRelayClose(0x55)
    while cnt < 10:
        k8090.cmdGetStatus()
        time.sleep(0.15)
        k8090.cmdRelayToggle(0xFF)
        time.sleep(0.15)
        cnt = cnt + 1
    cnt = 0
    time.sleep(0.3)
    # Reset
    k8090.cmdRelayOpen(0xFF)

def runWithoutListener(k8090):
    runDemo(k8090)
    k8090.serialClose()

def runWithListener(k8090):
    k8090.serialListenerStart()
    try:
        runDemo(k8090)
        k8090.serialListenerStop()
        k8090.serialClose()
    except KeyboardInterrupt:
        print("Terminated by user")

if __name__ == "__main__":
    # Edit port if needed (/dev/ttyACM0 or /dev/ttyUSB0 or COMx)
    k8090 = K8090(port='/dev/ttyACM0')
    # Select demo
    runWithoutListener(k8090)
    #runWithListener(k8090)
