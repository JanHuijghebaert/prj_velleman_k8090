# Velleman K8090

## Requirements

- Make sure [```python```](https://www.python.org/) is installed
- Make sure ```pyserial``` is available

```bash
$ pip install pyserial
```

- Add you user to the ```dialout``` group

```bash
$ sudo usermod -aG dialout $USER
```

## Info

- The device port appears as a USB CDC/ACM serial device:
    - Linux e.g. /dev/ttyACM0
    - Windows e.g. COM3

## Serial protocol

- Packet structure: 7-byte data packets
    - Byte 1 - 0x04 - Start byte (STX)
    - Byte 2 - 0x__ - Command
    - Byte 3 - 0x__ - Relay mask
    - Byte 4 - 0x__ - Parameter 1 (0x00 if not used)
    - Byte 5 - 0x__ - Parameter 2 (0x00 if not used)
    - Byte 6 - 0x__ - Checksum (two's complement of the sum of the packet bytes)
    - Byte 7 - 0x0F - End byte (ETX)

## Board

### Event jumper PCB

| Set    | Button actions | USB actions |
| ------ | -------------- | ------------|
| On     | Disabled       | Enabled     |
| Off    | Enabled        | Enabled     |

### PCB

![K8090 board](images/k8090.jpg)

## Demo

In the main function, select a demo. The demo with listener is more advanced since it will also register button events and (unsolicited) status updates.

```python
# Select demo
#runWithoutListener(k8090)
runWithListener(k8090)
```
### Output

#### Without listener

```
Serial opened
[TX] CMD Reset factory defaults
[TX] CMD Get firmware
[RX] Firmware: Year 2016, Week 06
[TX] CMD Relay close (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[TX] CMD Relay open (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[TX] CMD Relay close (ID: 3)
[TX] CMD Relay open (ID: 3)
[TX] CMD Relay close (ID: 3)
[TX] CMD Relay open (ID: 3)
[TX] CMD Relay toggle (ID: 5)
[TX] CMD Relay toggle (ID: 5)
[TX] CMD Relay toggle (ID: 5)
[TX] CMD Relay toggle (ID: 5)
[TX] CMD Relay toggle (ID: 5)
[TX] CMD Get status
[RX] Status - Closed: 5
[TX] CMD Relay open (ID: 1, 2, 3, 4, 5, 6, 7, 8)
You can now perform button tests for 10 seconds...
End of test
[TX] CMD Relay open (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[TX] CMD Relay close (ID: 1, 3, 5, 7)
[TX] CMD Get status
[RX] Status - Closed: 1, 3, 5, 7
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[TX] CMD Get status
[RX] Status - Closed: 2, 4, 6, 8
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[TX] CMD Get status
[RX] Status - Closed: 1, 3, 5, 7
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[TX] CMD Get status
[RX] Status - Closed: 2, 4, 6, 8
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[TX] CMD Get status
[RX] Status - Closed: 1, 3, 5, 7
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[TX] CMD Get status
[RX] Status - Closed: 2, 4, 6, 8
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[TX] CMD Relay open (ID: 1, 2, 3, 4, 5, 6, 7, 8)
Serial closed
```

#### With listener

```
Serial opened
Serial listener running...
[TX] CMD Reset factory defaults
[RX] Factory defaults - [4, 112, 0, 0, 0, 140, 15]
[TX] CMD Get firmware
[RX] Firmware: Year 2016, Week 06
[TX] CMD Relay close (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[RX] Status - Closed: 1, 2, 3, 4, 5, 6, 7, 8
[TX] CMD Relay open (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[RX] Status - Closed: None
[TX] CMD Relay close (ID: 3)
[RX] Status - Closed: 3
[TX] CMD Relay open (ID: 3)
[RX] Status - Closed: None
[TX] CMD Relay close (ID: 3)
[RX] Status - Closed: 3
[TX] CMD Relay open (ID: 3)
[RX] Status - Closed: None
[TX] CMD Relay toggle (ID: 5)
[RX] Status - Closed: 5
[TX] CMD Relay toggle (ID: 5)
[RX] Status - Closed: None
[TX] CMD Relay toggle (ID: 5)
[RX] Status - Closed: 5
[TX] CMD Relay toggle (ID: 5)
[RX] Status - Closed: None
[TX] CMD Relay toggle (ID: 5)
[RX] Status - Closed: 5
[TX] CMD Get status
[RX] Status - Closed: 5
[TX] CMD Relay open (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[RX] Status - Closed: None
You can now perform button tests for 10 seconds...
[RX] Button 1 pushed
[RX] Status - Closed: 1
[RX] Button 1 released
[RX] Button 2 pushed
[RX] Status - Closed: 1, 2
[RX] Button 2 released
[RX] Button 3 pushed
[RX] Status - Closed: 1, 2, 3
[RX] Button 3 released
[RX] Button 3 pushed
[RX] Status - Closed: 1, 2
[RX] Button 3 released
[RX] Button 2 pushed
[RX] Status - Closed: 1
[RX] Button 2 released
[RX] Button 1 pushed
[RX] Status - Closed: None
[RX] Button 1 released
[RX] Button 4 pushed
[RX] Status - Closed: 4
[RX] Button 4 released
End of test
[TX] CMD Relay open (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[RX] Status - Closed: None
[TX] CMD Relay close (ID: 1, 3, 5, 7)
[RX] Status - Closed: 1, 3, 5, 7
[TX] CMD Get status
[RX] Status - Closed: 1, 3, 5, 7
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[RX] Status - Closed: 2, 4, 6, 8
[TX] CMD Get status
[RX] Status - Closed: 2, 4, 6, 8
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[RX] Status - Closed: 1, 3, 5, 7
[TX] CMD Get status
[RX] Status - Closed: 1, 3, 5, 7
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[RX] Status - Closed: 2, 4, 6, 8
[TX] CMD Get status
[RX] Status - Closed: 2, 4, 6, 8
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[RX] Status - Closed: 1, 3, 5, 7
[TX] CMD Get status
[RX] Status - Closed: 1, 3, 5, 7
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[RX] Status - Closed: 2, 4, 6, 8
[TX] CMD Get status
[RX] Status - Closed: 2, 4, 6, 8
[TX] CMD Relay toggle (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[RX] Status - Closed: 1, 3, 5, 7
[TX] CMD Relay open (ID: 1, 2, 3, 4, 5, 6, 7, 8)
[RX] Status - Closed: None
Serial listener stopped
Serial closed
```
