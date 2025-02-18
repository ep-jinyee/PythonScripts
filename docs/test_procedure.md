# Test Procedure

### Auth API test

Can refer to Node-red flow for this test

1. Call GET /network API without login, should return *401 Not Authorised*

2. Login to get token using <url>

3. Call GET /network again, this time should return 200

4. Wait 60s until token expire, call GET /network again to test token expiry, observe and should return *401 Not Authorised*

### System info API Test

Can refer to Node-red flow for this test

1. Login API

2. Use step 1. to login and get token in cookie, store the cookie for later use.

3. Get hardware info.

4. Get network info.

5. Set network info to change ip address, and use the changed ip address for the subsequent request.

6. Get debug memory info.

7. Open a browser, visit the url https://<your edge ip> to observe if the website is displayed properly.

### Card + Car plate Insertion/Retrieval Test

1. Prepare a csv file that consist of 10,000 randomly generated car plates (max 20 chars) and card no (max 10 digits). Column 1 is car plates, column 2 is card no. You can use *resources/skyvouge-10k.csv* as example. 

2. Using *_06_csv_post_lpr_card.py*, get each entry of csv file from 1, form the HTTP POST request to add to Edge LPR. After POST request, immediately initial a GET request to check if car plate + card is saved into Edge LPR.

3. Using *_03_csv_to_lpr_txt.py*, generate a local LPR.TXT (local LPR.TXT) using the CSV from 1.

4. Using <script name>, download the LPR.TXT from DUT (DUT LPR.TXT), compare it with the local LPR.TXT from step 3. They should be the same.

5. Now erase the whole device by calling the cold start api.

6. Using the local LPR.TXT from step 3, upload it using api <api url>.

7. Repeat step 4 and compare, local LPT.TXT and DUT LPR.TXT should be the same.

8. Using <scipt name>, increment the digit of each card by 1, and immediately initial a GET request to see if card is being modified. Result is logged in <result file>

9. Using <script name>, delete each car plate + card one by one, after delete immediately initiate GET request to check if card is deleted. Result is logged in <result file>.

10. Repeat step 4, now the DUT LPR.TXT should be all empty (all set the hex 0xff)

### Sytem Op. API Test

Do this with the Node-red flow

1. Login API

2. Using /restart to restart the device (Can observe P1 Reader Up or OSDP LED blinking)

3. Modify some settings, such as VZ LED, HCB event text and add a few cards into Edge LPR.

4. Login API again. (after restart, session will be cleared, and you will need to login again)

5. Use /coldstart to restart and erase the settings in Edge LPR. Using APIs such as GET card and GET led settings to check if settings are erase and set to default.

6. Login API again, using /factory to factory reset the device. Device should enter discovery mode, by observing the heartbeat or visit https://192.168.4.100 in the browser should confirm the device state.

### Discovery Mode to Operational Mode

You can refer to Node-red flow.

1. Make sure the device is in Discovery mode, by observing the heartbeat LED, or connect ethernet direct to PC and use web browser to visit https://192.168.4.100 to see the device mode.

2. On Window OS, you can use *Serial Debug Assistant*, set the mode as TCP Client, enter the DUT ip (in our case 192.168.4.100) and port 2020, then open the TCP port.

3. Send the following JSON formatted payload to DUT:

`{"model":"EDGELPR","mac":"88:97:DF:FF:FF:FF","ipv4":"192.168.88.247","subnet":"255.255.255.0","dns":["8.8.8.8","8.8.4.4"],"gateway":"192.168.88.1","arp_resp":"192.168.88.169"}`

You should enter the new Ip and subnet for the DUT in operational mode here. Leave arp_resp as your PC ip.

4. After sent, the device should restart and enter Operational Mode

### Hardware Integration (Final Test)

|---------| ==== Ethernet  ==== Test program host (your laptop)
|         |
|         | ==== RS485 (3) ==== VZ CAMERA
|   DUT   |
| (ELPR)  | ==== RS485 (2) ==== VZ LED CTRL BOARD
|         |
|---------| ==== RS485 (1) ==== HCB

1. Make sure each components are wired as aforementioned.

2. Make sure OSDP connection is set up (observing LED or P1 *Reader Up*)

3. Make sure static content is displayed as it should be.

4. Set up HCB, such that it contains at least 5 cards that can simulate antipassback, valid card entry, disabled card, wrong timezone, expired card. Also, hook HCB up with another reader to simulate antipassback.

5. Set up Edge, add cards - car plate to match HCB. Also add some unknown card to test if Edge searching works properly.

6. Observe the LED see if display is correct.

7. Modify HCB event text and static content text to check if funtions are working ok.

8. Enable time display on VZenit web app to see if time is display on idle state.

9. Try pressing push button to cold start/factory reset device.