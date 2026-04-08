import ctypes
import time
import pyads

# Konfigurácia
PLC_IP      = '192.168.1.52' # IP vášho Windows stroja
PLC_NETID   = '192.168.1.25.1.1' # NetID vášho Windows stroja
LINUX_NETID = '192.168.1.51.1.1' # (NetID Linuxu musí byť v tej istej triede ako PLC, ale s iným číslo hosta, napríklad .25.1.1 pre PLC a .51.1.1 pre Linux)
LINUX_IP    = '192.168.1.51' # (IP Linuxu musí byť v tej istej podsieťi ako PLC, napríklad 192.168.1.x)

class ST_to_Jetson(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("id",    ctypes.c_int16),
        ("uhol",  ctypes.c_float),
        ("sirka", ctypes.c_float),
        ("scan",  ctypes.c_bool),
    ]

STRUCT_SIZE = ctypes.sizeof(ST_to_Jetson)
DATA_OFFSET = pyads.structs.SAdsNotificationHeader.data.offset
print(f"Struct size : {STRUCT_SIZE}")
print(f"Data offset : {DATA_OFFSET}")

def struct_callback(notification, data):
    contents  = notification.contents
    data_addr = ctypes.addressof(contents) + DATA_OFFSET
    buf = (ctypes.c_ubyte * STRUCT_SIZE)()
    ctypes.memmove(buf, data_addr, STRUCT_SIZE)
    parsed = ST_to_Jetson.from_buffer(buf)
    print(f"id={parsed.id}  uhol={parsed.uhol:.4f}  sirka={parsed.sirka:.4f}  scan={parsed.scan}")

# ✅ Správny vzor pyads pre Linux:
# open_port() zostáva otvorený — Connection znovu používa ten istý port interno
pyads.open_port()
pyads.set_local_address(LINUX_NETID)

# Použite objekt AmsAddr pre add_route (spoľahlivejšie ako reťazec NetID)
remote_addr = pyads.AmsAddr(PLC_NETID, 801)
pyads.add_route(remote_addr, PLC_IP)

print(f"Local address: {pyads.get_local_address()}")


plc = pyads.Connection(PLC_NETID, 801,PLC_IP)

try:
    with plc:
        if plc.is_open:
            print("✅ Spojenie otvorené")

            attr    = pyads.NotificationAttrib(STRUCT_SIZE)
            handles = plc.add_device_notification('.Lavy', attr, struct_callback)

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("🛑 Zastavené užívateľom")
            finally:
                plc.del_device_notification(*handles)
        else:
            print("❌ Spojenie sa nepodarilo otvoriť.")

except pyads.ADSError as err:
    print(f"❌ ADS Chyba: {err}")
except Exception as e:
    print(f"❌ Iná chyba: {e}")
finally:
    pyads.close_port()  # ✅ zatvor globálny port len na úplný koniec