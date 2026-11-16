# Beş dakikalık demo akışı

Ön hazırlık: README kurulumunu yap. `python -m src.demo` komutuyla aç. models/full dosyaları gerekir; yeniden eğitim yapma. Gösterilen model eğitim tohumu 11'dir; beş tohumun en iyisi seçilmiş değildir. Harita tohumu 2000 ve baseline ile başla.

1. **0:00–0:45:** Dünya, başlangıç, hedef ve robot boyutunu göster. Harita seed değerinin tekrar üretilebilirlik sağladığını açıkla. Başlat düğmesini kullan.
2. **0:45–1:30:** Duraklat. Beş normalize girdiyi, Gaussian üyelik değerlerini ve ilk beş etkin kuralı göster. Kural dizisindeki indeksler sırasıyla ön/sol/sağ/açı/uzaklık kümeleridir. Gerçek kontrolcü core.py ile çalışır.
3. **1:30–2:15:** Sıfırla, proposed seç, aynı haritayı çalıştır. Model değiştirirken sıfırlamak karşılaştırmayı aynı başlangıçtan yapar. Lambda=100 doğrulama sonucudur.
4. **2:15–3:15:** Üstteki düzenleme seçeneğiyle hedefi değiştir, boş alana engel ekle ve engel sil. Geçersiz başlangıç/hedef veya geçişsiz düzenleme uyarı üretir. Engelin yerini değiştirmek için silip yeniden ekle; yarıçap eklemede 0.4 m sabittir.
5. **3:15–4:00:** results/figures/trajectories.png içindeki başarısız harita tohumunu aç. Demo 2000..2029 tohumlarında kaydedilmiş test haritasını aynen yükler; diğer tohumlarda 6 engelli yeni harita üretir. Başarısızlık olasılığını açıkça tartış.
6. **4:00–5:00:** Sonuçları 142/150 ve 140/150 olarak ver. 150'nin 5 model × 30 harita olduğunu belirt. Soru-cevapta güvenli mesafe cezasının neden güvenlik garantisi olmadığını açıkla.

Kontroller: Başlat, Duraklat, Sıfırla, Harita yükle. Yeni hedef/engel düzenlemesi koşuyu sıfırlar. Hazır modeller çalışma sırasında tekrar öğrenmez. Program kapatılınca düzenlenen harita kaydedilmez.

Sunum öncesi kendi ekranında arayüzü dene. Mevcut ortamda Tkinter model yükleme, ilerletme, duraklatma, sıfırlama ve geçerli hedef değiştirme programatik doğrulanmıştır. Ekran görüntüsü alınamadığı için masaüstü arayüzün görsel denetimi tamamlanmış sayılmaz.
