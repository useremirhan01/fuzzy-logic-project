# Yeniden gerçekleştirme kapsamı

Bu belge öğretim elemanı onayı değildir. Makalenin sayfa 4, denklemler (1)-(4) bulanık ağının yapısal yeniden kurulumu ve sayfa 6-7 ağırlık evrimi temel alınmıştır. Merkez/genişlik, kural sayısı ve fizik tamamlayıcı varsayımlardır. Yapı sabit sonuçlu Sugeno benzeri ağırlıklı ortalama yorumuna uygundur; Jang'ın hibrit öğrenmeli ANFIS algoritması uygulanmamıştır.

Seçilen temel deney: “Path planning experiment”, Şekil 6 / Tablo 2, 0,2,4,6,8,10 engel taraması. `python -m src.paper_experiment` her yoğunluk için ayrı haritada 5 GA tohumu çalıştırır. Sonuç `results/full/paper_approximation.csv` dosyasındadır. Burada harita üzerinde GA eğitimi ve bulunan yol değerlendirmesi yapılır; bu sonuç genelleme testi değildir. Kontrolcü, GA, harita ve donanım aynı olmadığından yayın süreleriyle oran ya da hızlanma iddiası kurulmaz.

Ana katkı deneyi ayrı tutulur: eğitim 100..107, doğrulama 1000..1007, test 2000..2029 tohumları. Testte 2/4/6/8/10 engel bulunur. Katsayı seçiminden sonra test sonuçları elde edilmiştir. Yaklaşık makale deneyinin 4000+engel_sayısı haritaları ana testten ayrıdır.

MRR durumu: Fuzzy bileşen ve bir temel deneyin yaklaşık kurulumu tamamlanmıştır. Birebir deney tekrarı kısmen karşılanır. Orijinal haritalar, örnek veri, tam parametreler ve ölçüt tanımları olmadan birebir tekrar veya orijinal %98.64 sonucunun doğrulanması mümkün değildir. BPNN/SOM/ART ve diğer planlayıcılar yeniden uygulanmamıştır. 40 dinamik engelli 500 örneklik deney kapsam dışıdır.
