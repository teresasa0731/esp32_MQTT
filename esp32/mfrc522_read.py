import mfrc522
from os import uname
import time

def do_read():
    rdr = mfrc522.MFRC522(19, 2, 4, 5, 18)
    index = True
    try:
        while True:
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    print("card detected")
                    print("uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    return raw_uid
                    index = False
                    if rdr.select_tag(raw_uid) == rdr.OK:
    
                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                            print("Address 8 data: %s" % rdr.read(8))
                            rdr.stop_crypto1()
                        else:
                            print("Authentication error")

    except KeyboardInterrupt:
        print("Bye")
