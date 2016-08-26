OBD-II
------
The OBD-II standard specifies the type of diagnostic connector, its pinout, the electrical signalling protocols and the
messaging format. 

It also provides a default list of vehicle parameters to monitor along with how to encode the data for each.

J1962
-----
Defines the physical connector, 2 standardized connectors type A and B. type A is for vehicles with 12v supply

EOBD
----
European equivalent of OBD-II

JOBD
----
Japanese version of OBD-II

Signalling overview
-------------------
There are many electical signalling protocols permitted by OBD-II standard. Need to set the OBD-II reader hardware to the
correct one before in functions with the vehicle. Some OBD-II readers can do this automatically. 


- SAE J1850 PWM (41.6 kbit/s)
- SAE J1850 VPW (10.4 kbit/s)
- ISO 9141-2 (5 baud init, 10.4 kbit/s)
- ISO 14230-4 KWP (5 baud init, 10.4 kbit/s)
- ISO 14230-4 KWP (fast init, 10.4 kbit/s)
- ISO 15765-4 CAN (11 bit ID, 500 kbit/s)
- ISO 15765-4 CAN (29 bit ID, 500 kbit/s)
- ISO 15765-4 CAN (11 bit ID, 250 kbit/s)
- ISO 15765-4 CAN (29 bit ID, 250 kbit/s)
- SAE J1939 (250kbps)
- SAE J1939 (500kbps)


My test Cars
------------
Car                          | Protocol        | Mode 1            | Mode 2   | Mode 5(3) | mode 6 | Mode 7 | Mode 9
Citroen C3 1.4 petrol (2003) | KWP FAST        | (BE3EF811/8000000)| 7E380000 | No        | No     | No     | 30000000
Ford KA 1.3 (2005)           | CAN 11bit 500kb | (BE3EB811/8000000)| &E380000 | No        |8000000 | Yes    | 54000000

ELM323
------
A chip that converts OBD-II signals to RS232.

ELM327
------
A customized microcontroller from ELM Electronics that can interface to a OBD-II interface. It supports a Hayes AT like
command set for controlling the device.

