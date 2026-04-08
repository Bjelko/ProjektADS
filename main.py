import pyads

# Konfigurácia
PLC_IP = '192.168.1.52' # IP vášho Windows stroja
PLC_NETID = '192.168.1.52.1.1' # NetID vášho Windows stroja
LINUX_NETID = '192.168.1.51.1.1'

# Identita Linuxu
port=pyads.open_port()
pyads.set_local_address(LINUX_NETID)
pyads.add_route(PLC_NETID, PLC_IP)

# Použijeme Connection s explicitným portom 801 (TwinCAT 2 PLC Runtime 1)
plc = pyads.Connection(PLC_NETID, 801,PLC_IP)
#pyads.set_timeout(5000)  # Nastavíme timeout na 5 sekund
print(pyads.get_local_address())  # Zobrazíme lokálnu adresu pre kontrolu
try:
    plc.open()
    if plc.is_open:
        print("✅ TCP Port otvorený. Skúšam ADS komunikáciu...")
        
        # Skúsime prečítať stav systému namiesto Device Info (je to jednoduchšie)
        ads_state, device_state = plc.read_state()
        print(f"✅ ADS State: {ads_state}, Device State: {device_state}")
        # State 5 znamená RUN
        
    else:
        print("❌ Spojenie sa nepodarilo otvoriť.")
    precitane = plc.read_by_name(".cislo", pyads.PLCTYPE_INT)  # Skúsime čítať premennú
    print(f"✅ Prečítaná hodnota: {precitane}")
except pyads.ADSError as err:
    print(f"❌ ADS Chyba: {err}")
    
except Exception as e:
    print(f"❌ Iná chyba: {e}")
finally:
    plc.close()