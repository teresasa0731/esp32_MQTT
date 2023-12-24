import mfrc522
from os import uname
def do_write():
    rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
    try:
        while True:
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    print(" - uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                            stat = rdr.write(8, b"这里输入你要写入的数据,16进制")
                            rdr.stop_crypto1()
                            if stat == rdr.OK:
                                print("数据已写入")
                            else:
                                print("数据写入失败")
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        print("Bye")