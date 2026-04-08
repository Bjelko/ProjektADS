from ctypes import sizeof
import ctypes
import time

import pyads
import struct
import threading

# Konfigurácia
PLC_IP = '192.168.1.52' # IP vášho Windows stroja
PLC_NETID = '192.168.1.52.1.1' # NetID vášho Windows stroja
LINUX_NETID = '192.168.1.51.1.1'

# Identita Linuxu
port=pyads.open_port()
pyads.set_local_address(LINUX_NETID)
pyads.add_route(PLC_NETID, PLC_IP)

plc = pyads.Connection(PLC_NETID, 801)
print(pyads.get_local_address()) # Zobrazíme lokálnu adresu pro kontrolu

# Callback funkcia - zavolá sa pri zmene v PLC
def handle_notification(notification, premenna):
    print("--- Nový balík dát ---")
    print(f"Notification: {notification} (Typ: {type(notification)})")
    #value=ctypes.c_int16.from_buffer_copy(notification.contents.data).value
    value2=notification.contents.data       #<== pre integer uz su data tu, ale pre struct budu data v notification.contents.data a musime ich rozbalit
    print(f"Data: {value2} (Typ: {type(premenna)})")

    raw = notification.contents.data

    if isinstance(raw, int):
        value = raw
    else:
        # fallback pre iné systémy
        import struct
        value = struct.unpack("<h", raw)[0]

    print("Value:", value)
try:
    plc.open()
    if plc.is_open:
        attr = pyads.NotificationAttrib(sizeof(pyads.PLCTYPE_INT))
        handles = plc.add_device_notification('.cislo',attr,handle_notification    )
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            plc.del_device_notification(*handles)
            plc.close()
        
    else:
        print("❌ Spojenie sa nepodarilo otvoriť.")
except pyads.ADSError as err:
    print(f"❌ ADS Chyba: {err}")
    
except Exception as e:
    print(f"❌ Iná chyba: {e}")
finally:
    plc.close()