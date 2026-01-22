import can
import time

# 1. Sanal ECU (Dinleyici) Sınıfı
# Bu sınıf, bir mesaj geldiğinde ne yapacağını bilir
class SanalECU(can.Listener):
    def __init__(self):
        super().__init__()
        print("Sanal ECU (dinleyici) başlatıldı. Saldırı bekleniyor...")
        print("="*40)

    def on_message_received(self, msg):
        # Her mesaj alındığında bu fonksiyon otomatik olarak çalışır
        print(f"\n>>> MESAJ ALINDI (ECU): ID={hex(msg.arbitration_id)} Veri={list(msg.data)}")
        print(f"    (Timestamp: {msg.timestamp})")
        # GERÇEK DOKÜMANDAKİ ML MODELİ BU NOKTADA DEVREYE GİRERDİ
        # Model, bu mesajın zamanlamasını (timestamp) analiz ederdi.


# === ANA SİMÜLASYON ===

def simulate_replay_attack():
    # 1. BİRLİKTE KULLANILACAK OLAN Sanal Veriyolunu (Bus) oluştur
    # receive_own_messages=True, aynı script içindeki dinleyicinin,
    # göndericinin mesajını alabilmesini sağlar.
    bus = can.interface.Bus(bustype='virtual', channel='simulasyon_kanali', receive_own_messages=True)

    # 2. Saldırganın yakaladığı "Şarj Başlat" komutunu tanımla
    sarj_baslat_mesaji = can.Message(
        arbitration_id=0x123,
        data=[0x11, 0x22, 0x33, 0x44]
    )

    # 3. Dinleyiciyi (Sanal ECU) oluştur ve veriyoluna bağla
    ecu = SanalECU()
    notifier = can.Notifier(bus, [ecu])

    print("Simülasyon Başlıyor...\n")

    # --- MEŞRU GÖNDERİM ---
    print(f"--- (1) MEŞRU GÖNDERİM: Kullanıcı arabayı şarja takıyor...")
    bus.send(sarj_baslat_mesaji)
    # Notifier'ın mesajı işlemesi için kısa bir bekleme
    time.sleep(1)

    print("\n... 3 saniye bekleniyor (Saldırgan komutu yakaladı, araç şarjı durdurdu) ...\n")
    time.sleep(3)

    # --- REPLAY SALDIRISI ---
    print(f"--- (2) REPLAY SALDIRISI: Saldırgan aynı komutu tekrar gönderiyor...")
    # Saldırgan, yakaladığı AYNI mesajı (veya kopyasını) tekrar gönderir
    bus.send(sarj_baslat_mesaji)
    time.sleep(1)

    # 4. Simülasyonu bitir
    print("\n"*2 + "="*40)
    print("Simülasyon Bitti.")
    notifier.stop()
    bus.shutdown()

# Script'i çalıştır
if __name__ == "__main__":
    simulate_replay_attack()

