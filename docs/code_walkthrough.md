# Kod okuma rehberi

## Okuma sırası
1. `src/core.py` başındaki sabitler fizik ve zaman ölçeklerini tanımlar. RULES Kartezyen çarpımı 80 kural oluşturur. CENTER/WIDTHS sabit öncüllerdir.
2. `memberships`: beş normalize girdiden Gaussian üyelikler hesaplanır. `activation`: her kuralın beş üyeliği minimumla birleştirilir, sonra etkinlikler toplamına bölünür. `control`: normalize etkinlik ve öğrenilmiş sonuç ağırlıkları çarpılır; çıktı fiziksel hız sınırlarına getirilir.
3. `prior`: uzman başlangıç kurallarını kurar. `models/full` ise gerçekten evrimle seçilmiş ağırlıkları içerir. Bu iki kavramı karıştırma.
4. `sense`: dairesel engellerin gövdeye göre üç açısal sektördeki en kısa yüzey açıklığını hesaplar. Sektör genişliği ve engelin açısal boyutu hesaba katılır. Bu gerçek lidar ışın izleme modeli değildir.
5. `segment_clearance`: hareket parçasının engel merkezine minimum uzaklığı, iki yarıçap ve duvarlar üzerinden güvenlik açıklığını hesaplar. `rollout`: bu denetleyiciyi adım adım yürütür; sonuç, yol, süre, ceza ve durum dizileri üretir.
6. `reachable`: BFS yalnız harita geçişini doğrular. `make_map`: deterministik harita üretir. Kontrolcü BFS yolunu görmez.
7. `src/experiment.py/train`: aynı haritalarda popülasyonun uygunluğunu ölçer, turnuva/çaprazlama/mutasyon uygular. Çıkış ağırlıkları kromozomdur. İki sonuçlu bir kural blok sayılır.
8. `run`: eğitim ve doğrulama adaylarını kaydeder, yalnız doğrulamayla lambda seçer, sonra bütün test haritalarını iki yöntemde çalıştırır. `summarize`: tohum ve harita tekrarlarını ayırır, ortak başarıları eşleştirir.
9. `src/paper_experiment.py`: kaynağın engel sayısı taramasının yaklaşık sürümü. Ana test genellemesiyle karıştırma.
10. `src/demo.py`: Tkinter döngüsü aynı sense/control/segment_clearance işlevlerini çağırır. Ekranda gösterilen üyelikler kontrol hesabının gerçek ara değerleridir.
11. `src/figures.py`: CSV/JSON'dan grafikler üretir. `tools/build_deliverables.py`: rapor ve sunum üretir; temel yazılımın çalışması için gerekli değildir.

## Somut kural örneği
RULES satırı `[0,1,0,2,1]`: ön yakın, sol uzak, sağ yakın, hedef açısı sıfır civarı, hedef uzak. Ön engel yakın olduğundan uzman başlangıçta sola dönüş verir. GA bu kuralın hız/dönüş sonuçlarını değiştirebilir. Diğer kurallar da kısmen etkin olduğundan son çıktı bu tek kuralın emri değildir.

## Kavramsal sınırlar
Bu kod öğrenilmiş öncüllere sahip tam ANFIS değildir. Geri yayılım yoktur; eğitim GA ile gerçekleşir. Çevrim içi öğrenme yoktur. Kontrolcü yereldir; küresel en kısa yolu garantilemez. Sensör gürültüsü, dinamik engeller ve diferansiyel tekerlek dinamiği uygulanmamıştır.
