# Kaynak bilgisi ve uygulama varsayımları

| Konu | Makalede açık olan / eksik olan | Seçim ve etkisi |
|---|---|---|
| Üyelik | Gaussian adı var, denklemde exp ve eksi yok | exp(-((x-c)/sigma)^2); geçerli [0,1] üyelik |
| Kural işlemi | Minimum ve normalizasyon var | Min t-norm korunur, toplam sıfırsa eşit ağırlık |
| Girdiler | Engel, hedef uzaklığı/açısı anlatılır; kesin boyut yok | Ön/sol/sağ açıklık, açı hatası, hedef uzaklığı: 5 girdi |
| Üyelik sayısı | Verilmemiş | 2×2×2×5×2 = 80 kural; 160 çıkış ağırlığı |
| Merkezler | Verilmemiş | Mesafe girdileri 0,1; açı -1,-0.5,0,0.5,1 |
| Genişlikler | Verilmemiş | Engel 0.42, açı 0.30, hedef 0.55; sabit |
| Sensör | Donanım/menzil belirsiz | 3 m, üç açısal sektör; engelin açısal yarıçapı dahil; gürültüsüz |
| Duvar | Belirsiz | Dünya sınırı çarpışmaya ve açıklık cezasına dahil; sensör vektöründe yok. Sınıra yakın başarısızlık yaratabilir |
| Çıkış | Tekerlek sürme kuvvetleri deniyor | Doğrusal hız 0..0.8 m/s, açısal hız -1..1 rad/s. Kuvvet öğrenmiyoruz |
| Fizik | dt, kütle, dingil açıklığı eksik | θ'=θ+ωdt, p'=p+vdt(cosθ',sinθ'); dt=0.2 s. Parçalı doğrusal sayısal model |
| Robot | Boyutu yok | Disk yarıçapı 0.18 m; süpürülen disk çarpışması |
| Bitiş | Eşik/timeout belirsiz | Hedef 0.30 m, 250 adım = 50 simülasyon saniyesi |
| Harita | Bozuk hedef (570570570) | 10×10 m, yeni tohumlu statik daire haritaları; birebir depo deneyi değil |
| GA kromozomu | Ağırlık ve yol tanımları çelişkili | 80×2 gerçek ağırlık; her kuralın iki çıkışı bir blok |
| Başlatma | Rastgele [-1,1] ve uzman kuralları ayrı anlatılır | Uzman öncülü + N(0,0.25), [-1,1]'e kırpma. Saf rastgele ağırlık deneyinden sapma |
| GA seçilim | Turnuva 4 | Korundu; 2 elit, 20 birey, 20 nesil proje seçimi |
| Çaprazlama | İki noktalı ve tek noktalı açıklama var | Kural blok sınırlarında iki nokta; iki çıkış birlikte taşınır |
| Mutasyon | Sınırlı, üniform olmayan deniyor | Gen olasılığı .12, nesille azalan maksimum adım; özgün dağılım bilinmiyor |
| Uygunluk | Denklem (9), qv/qs ayrımı belirsiz | t=adım; başarısızsa 7000. d=60×son uzaklık(m); qv=çarpışmasız ve |Δθ|<.1 adımlar; qs=çarpışmasız adımlar |
| d ölçeği | 1200 sabiti dışında açıklık yok | 60 proje ölçeğidir; makale birimini temsil ettiği ileri sürülmez |
| Güvenlik | Çarpışmasızlık ödülü zaten var | Yakın geçişin sürekli kareli cezası eklenir; dünya ölçeğinde algoritmik yenilik iddiası yok |

Makaledeki tekerlek çıktılarıyla ilişki: ideal diferansiyel sürüşte tekerlek doğrusal hızları vL=v-bω/2 ve vR=v+bω/2 olur. Örneğin b=0.36 m seçilebilir. Uygulama bu dönüşümü ihtiyaç duymadığı için kullanmaz, tekerlek dinamiğini modellemez.

İstatistik: Aynı modele ait 30 harita bağımsız eğitim tekrarı değildir. Beş eğitim tohumu için başarı oranı ortalaması ve örnek standart sapma verilir. Başarısızlıklar tüm koşul oranlarında tutulur. Yol ve süre başarıya koşullu tabloda, ortak başarılar ayrı eşleşmiş tabloda raporlanır. Çarpışma adımı dahil yol uzunluğu bütün koşular için ham dosyada mevcuttur.
