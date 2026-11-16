# Makale analizi

Öğrenci: Emirhan Efe Demir, 1306230024. Atama: 16.
Jiawei Zhang, Scientific Reports 15, 14656 (2025), DOI: 10.1038/s41598-025-93926-1.
İnceleme: 16 Kasım 2026. Yayıncının 13 sayfalık PDF tam metni okundu; denklem (1) PDF görüntüsünde ayrıca kontrol edildi.

## Problem ve yöntem
Çalışma, robotun engeller arasında hedefe ulaşmasını FNN navigasyonu ve GA yol planlaması ile ele alır. Bulanık ağ beş katmandır: giriş, Gaussian bulanıklaştırma, minimum t-norm ile kurallar, toplam etkinliğe bölme ve ağırlıklı toplam çıkışı. Sayfa 4, denklemler (1)-(4) uygulama çekirdeğidir. Belirli girdi sayısı, tüm dilsel kümeler, merkezler, genişlikler ve kural tablosu verilmez.

## Teknik doğrulama
1. Denklem (1) yalnızca kareli uzaklık/genişlik karesi yazmaktadır. Merkezde sıfır, uzakta sınırsız değer verdiğinden bu ifade tek başına Gaussian üyelik olamaz. Kod exp(-((x-c)/sigma)^2) kullanır. Bu, makaleye ait doğrulanmış bir düzeltme değil, gerekçeli uygulama varsayımıdır.
2. Denklemler (5)-(8) tekerlek kuvvetlerinin farkını açı artışı, toplamını hareket büyüklüğü kabul eder. Kütle, tekerlek aralığı ve zaman adımı yoktur. Denklem (8)'in sinüs ifadesinde açı sembolü eksik görünmektedir. SI birimli fizik modeli için doğrudan kullanılamaz.
3. Sayfa 7'de hedef (570570570) şeklindedir. Bunun (570,570) olduğu tahmin edilebilir fakat kesin kabul edilmez. Yeni haritaların koordinatları ayrı tanımlanır.
4. Sayfa 6 kromozomu bağlantı ağırlıkları olarak tanımlar; sayfa 7 sonraki genel açıklama yol düğümlerinden söz eder. İlk bölüm nöron sınırlarında iki noktalı, sonraki bölüm tek noktalı çaprazlama anlatır.
5. FNN çıktısının GA başlangıç popülasyonu olup GA yolunun FNN'ye geri beslendiği söylenir; veri dönüşümü ve güncelleme denklemleri verilmez. Kod, ayrıntılı ağırlık kromozomu tarifini seçer. Çevrim içi çift yönlü FNN-GA geri beslemesini gerçekleştirdiğini iddia etmez.
6. Denklem (9) f=(7000-t)+(1200-d)+qv/30+qs/20 biçimindedir. qv ve qs'nin ayrı tanımları, t birimi, başarısız koşular ve ölçekler açık değildir. Uygulamadaki yorum assumptions.md içindedir.
7. Makale bazı yerlerde GA için küresel optimum garantisi ima eder. Sonlu popülasyon ve sonlu nesille böyle bir garanti verilmez.

## Deneyler ve sonuçlar
Navigasyon deneyinde 40 statik/dinamik engel ve 500 sensör örneği anlatılır. BPNN, SOM ve ART karşılaştırılır. Şekil 4 doğruluk, Şekil 5 navigasyon zamanı, Tablo 1 açısal sapma yüzdesi sunar. Ham örnekler, harita koordinatları ve ölçütlerin yeterli operasyonel tanımları verilmez.
Yol planlama deneyi Visual C++ 6.0 ortamında GA, karınca kolonisi, benzetimli tavlama ve tabu aramayı karşılaştırır. Şekil 6 ve Tablo 2, 0/2/4/6/8/10 engel taramasıdır. Bu tarama yaklaşık yeniden gerçekleştirme için seçildi.
Makale sonuçları results/tables/paper_reference.csv içerisinde ayrı tutulur. Bizim hedefe ulaşma oranımız makaledeki accuracy veya optimal path efficiency ile aynı ölçüt kabul edilmez. Özette 9.64 s en kısa zaman olarak anılırken Şekil 5 açıklamasında hedef 3 için 8.68 s vardır. Tablo 2 sonrasındaki tabu araması zaman yorumu da Şekil 6'nın önceki anlatımıyla çelişir.

## Erişim ve lisans
Şekil 4 ayrıca görsel olarak kontrol edildi: başlık doğruluk derken grafik ekseni Time(s) ve çizilen değerler Şekil 5'teki sürelerle uyumludur. Bu nedenle doğruluk sayıları grafikten sayısallaştırılmadı; metinde bildirilen değerler olarak kaydedildi.

Data availability bölümüne göre veri yazarından istenmelidir. Makale içinde resmi kod deposu bağlantısı saptanmadı. Bu, dünyada hiçbir kod bulunmadığı iddiası değildir. Kaynak PDF'nin lisansı CC BY-NC-ND 4.0'dır. Proje paketi makalenin PDF'sini veya değiştirilmiş şekillerini içermez; DOI bağlantısı sağlar. Kod sıfırdan, yapay zekâ yardımıyla yazıldı. Öğrencinin inceleme sorumluluğu sürmektedir.
