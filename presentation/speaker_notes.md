# Konuşmacı notları

Hedef ana sunum 17-19 dakika, demo/soru-cevap ayrıca 5 dakika.

## Slayt 1: Bulanık robot navigasyonu
1 dakika: Problemi ve tek değişkenli katkıyı anlat. Sonuçların tamamen iyileşme göstermediğini baştan belirt.

## Slayt 2: Problem ve araştırma sorusu
1 dakika: Mavi ve yeşil yollar aynı haritada farklı modellerdir. Bu görsel önceden çizilmiş demo değildir; kayıtlı modelin core.py ile yeniden koşusudur.

## Slayt 3: Literatürde yöntemlerin rolü
1.5 dakika: [2] ve [3] özet/künye düzeyinde incelendi. Güvenlik cezasının dünyada yeni olduğunu iddia etme. Kaynaklar references/README.md.

## Slayt 4: Beş katmanlı bulanık ağ
1.5 dakika: Her kural beş üyelik derecesinin minimumudur. Normalize etkinlikler toplamı birdir. Çıktı ağırlıkları GA ile öğrenilir; merkez ve genişlikler sabittir.

## Slayt 5: Üyelik ve çıktı hesabı
1.5 dakika: sigma büyüdükçe kümeler daha fazla örtüşür. Bu bir olasılık dağılımı değildir. Mamdani alan merkezi ve Jang hibrit ANFIS öğrenmesi uygulanmadı.

## Slayt 6: Makaleye sadakat ve belirsizlikler
1.5 dakika: Denklem 1 exp/eksi içermiyor. Hedef koordinatı bozuk. Şekil 4 başlığı ile ekseni çelişiyor. Bunları kaynak PDF ile göster; yazara ait kesin düzeltme gibi sunma.

## Slayt 7: Simülasyon ve çarpışma kontrolü
1 dakika: Izgara araması robotu yönlendirmez. Sayısal adım doğru parçasıdır. Dinamik engel, kayma ve sensör gürültüsü yoktur.

## Slayt 8: Genetik algoritma
1.5 dakika: Aynı tohumlarda başlangıç popülasyonu ve bütçe eşittir. Çıkış ağırlıkları öğrenilir. Lambda farklı amaç fonksiyonu olduğundan eğri yüksekliği tek başına karşılaştırma değildir.

## Slayt 9: Özgün katkı: açıklık cezası
1 dakika: c robot-engel yüzey açıklığıdır; dünya sınırları da dahildir. Ortalama ceza tehlikeli kısa bölgeyi seyreltebilir. Güvenlik garantisi yoktur.

## Slayt 10: Deney ve katsayı seçimi
1 dakika: Test haritaları aynı modeller arasında eşleşmiştir. 150 koşu 150 eğitim tohumu değildir. Pozitif lambda seçim kuralı önceden belirlenmiştir.

## Slayt 11: Test sonuçları
1.5 dakika: Başarı oranı tohum SS baseline 2.98, proposed 4.71 yüzde puan. Farkın istatistiksel anlamlı olduğunu söyleme.

## Slayt 12: Açıklık ve yol ödünleşimi
1 dakika: Başarısız koşuları oranlardan çıkarma. Yaklaşık 6 mm açıklık farkı fiziksel robotta güvenlik kanıtı değildir.

## Slayt 13: Sınırlılıklar ve sonuç
1 dakika: Negatif sonuç saklanmadı. Öğrenci yöntemi incelemeli ve savunabilmeli. Yapay zekâ kapsamlı kullanıldı, öğrencinin doğrulaması henüz yapılmış sayılmıyor.

## Slayt 14: Canlı demo ve teknik savunma
Sunum sonrası 5 dakika: docs/demo_guide.md akışını izle. Yeniden eğitim gerekmez. Bir başarısız örneği göster ve nedenini kesinlik iddiası olmadan yorumla.

## Kaynaklar
[1] J. Zhang, “Application and development of artificial intelligence and computer technology in the field of intelligent robots,” Scientific Reports, vol. 15, art. 14656, 2025. doi: 10.1038/s41598-025-93926-1. https://www.nature.com/articles/s41598-025-93926-1

[2] Y. Teng, T. Feng, C. Song, J. Li, S. X. Yang, and H. Zhu, “Path Planning of Mobile Robot Based on Dual-Layer Fuzzy Control and Improved Genetic Algorithm,” Symmetry, vol. 17, no. 4, art. 609, 2025. doi: 10.3390/sym17040609. https://www.mdpi.com/2073-8994/17/4/609

[3] S. Stavrinidis, P. Zacharia, and E. Xidias, “A Fuzzy Control Strategy for Multi-Goal Autonomous Robot Navigation,” Sensors, vol. 25, no. 2, art. 446, 2025. doi: 10.3390/s25020446. https://www.mdpi.com/1424-8220/25/2/446

[4] J.-S. R. Jang, “ANFIS: Adaptive-Network-Based Fuzzy Inference System,” IEEE Transactions on Systems, Man, and Cybernetics, vol. 23, no. 3, pp. 665-685, 1993. doi: 10.1109/21.256541. https://www.cic.ipn.mx/~pescamilla/SistInt/Jang1993.pdf