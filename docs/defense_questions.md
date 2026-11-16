# Teknik savunma: 20 soru ve cevap

## 1. Problemin nedir?
Statik engeller arasında hedefe ulaşan açıklanabilir bir bulanık denetleyiciyi kurmak ve yakın geçiş cezasının başarısı/çarpışması üzerindeki etkisini ölçmek. Gerçek robot kontrolünü doğruladığım iddiasında değilim.

## 2. Neden bulanık mantık?
“Ön engel yakınsa yavaşla” gibi dilsel bilgiyi sürekli girdilerle birleştirir. Keskin eşikler yerine yumuşak geçiş sağlar. Bunun bütün alternatiflerden üstün olduğunu deneyle göstermedik.

## 3. Üyelik derecesi olasılık mı?
Hayır. Bir sayının seçilen dilsel kümeyle uyumudur. Bir girdi aynı anda yakın ve uzak kümelerinde kısmen bulunabilir; üyeliklerin kendi aralarında toplamının bir olması gerekmez.

## 4. Gaussian neden seçildi?
Makale Gaussian adını kullanır. Uygulama exp(-((x-c)/sigma)^2) seçer. Kaynaktaki denklem eksiktir; bu tamamlamayı varsayım olarak kaydettik. Sigma kümelerin örtüşmesini değiştirir.

## 5. Girdiler neden normalize edildi?
Metre ve radyanı aynı ölçeklerde yorumlamak için. Engel uzaklıkları 3 m, hedef uzaklığı 10 m, açı pi ile ölçeklenir. Kırpma, uzak değerlerin aşırı etkisini engeller ama menzil ötesindeki bilgiyi de kaybeder.

## 6. Kaç kural ve parametre var?
2×2×2×5×2=80 kural. Her kuralın hız ve dönüş için iki sonuç ağırlığı var: toplam 160 öğrenilen ağırlık. Merkez ve genişlikler sabit.

## 7. Neden min t-norm?
Makalenin denklem (2)'si minimum kullanır. Kuralı en zayıf eşleşen öncül sınırlar. Çarpım alternatif olabilirdi ancak bu projede katkı değişkenini artırmamak için karşılaştırılmadı.

## 8. Durulaştırma nasıl yapılıyor?
Kural etkinlikleri toplamlarına bölünür ve sayısal sonuç ağırlıklarıyla toplanır. Mamdani çıktı üyelik alanının ağırlık merkezi alınmaz. Sıfır toplamda eşit etkinlik koruması vardır.

## 9. Bu ANFIS mi?
Bu, GA ile sonuç ağırlıkları öğrenilen beş katmanlı bulanık ağdır. Jang'ın hibrit öğrenme algoritmasını ve öncül uyarlamasını kullanmadığımız için ANFIS diye adlandırmıyoruz.

## 10. GA neyi öğreniyor?
Kural sonuçlarının 160 gerçek ağırlığını. Kromozom bir yol noktaları dizisi değildir. Kaynakta her iki anlatım vardır; ayrıntılı ağırlık tanımını seçtik.

## 11. Popülasyon nasıl başlıyor?
Bir uzman kural öncülü ve bunun etrafındaki Gaussian rastgele sapmalardan. Makalenin saf rastgele ağırlık başlatmasından sapma olarak açıklanmıştır. Aynı öncül iki yöntemde de kullanılır.

## 12. Çaprazlama ve mutasyon nasıl?
Turnuvada dört adaydan en iyisi seçilir. İki kesim kural blok sınırındadır. Gen başına .12 olasılıkla nesille küçülen sınırlı rastgele değişim uygulanır. İki elit korunur, ağırlıklar [-1,1]'e kırpılır.

## 13. Makaledeki fitness birebir mi?
Formülün toplam yapısı korunur, ama t/d ölçeği, qv/qs sayımı ve başarısızlık işlemi bizim açık varsayımlarımızdır. Başarısız koşuya t=7000 verilmesi erken çarpışmanın ödüllendirilmesini önler.

## 14. Katkın tam olarak ne?
0.6 m eşik altındaki yüzey açıklığının normalize kareli açığını koşu boyunca ortalayıp lambda ile cezalandırmak. Çarpışma ödülünden farklı olarak çarpışmadan önceki yakın geçişleri de ayırt eder. Literatürde güvenlik cezası yeni değildir; bu bir kontrollü proje genişletmesidir.

## 15. Test sızıntısını nasıl önledin?
Eğitim, doğrulama ve test tohumları ayrıdır. Lambda yalnız doğrulamada seçildi. Test sonuçlarından sonra katsayı değişmedi. Ana test haritaları aynı kaldı; yaklaşık kaynak deneyi ayrı haritalarda yürütüldü.

## 16. 150 deney bağımsız mı?
150 model-harita koşusu var: 5 eğitim tohumu × 30 ortak harita. Beş bağımsız eğitim tekrarı var; aynı haritanın tekrarı bağımsız harita örneği değildir. Standart sapmayı eğitim tohumları üzerinden veriyoruz.

## 17. Sonuç neden kötüleşti?
Proposed iki fazla çarpışma verdi. Az eğitim haritası, amaç fonksiyonu ödünleşimi ve evrim bütçesi olası nedenler; hangisinin nedensel olduğu ayrıca test edilmedi. Sonuç güvenlik üstünlüğünü desteklemiyor.

## 18. Yol uzunluğu karşılaştırmasında yanlılık var mı?
Yalnız başarılı koşuların alt kümeleri farklı olabilir. Bu yüzden başarı pay/paydasını ve iki yöntemin ortak başarılı olduğu 135 eşleşmedeki -0.0347 m farkı ayrıca raporladık. Başarısız yollar ham CSV'de tutulur.

## 19. Robot engelin içinden atlayabilir mi?
Sayısal adımın sadece uçları değil, tüm doğru parçası robot yarıçapıyla kontrol edilir. Bu, parçalı doğrusal modelde atlamayı önler. Sürekli yay hareketi, tekerlek kayması ve gerçek sensör gürültüsü modellenmedi.

## 20. Neler eksik ve yapay zekâ nasıl kullanıldı?
Orijinal veriler ve kesin parametreler yok; birebir deney tekrarı kısmi. Dinamik depo ve diğer karşılaştırma algoritmaları kapsam dışı. Codex kod, deney, belgeler ve kaynak incelemesine kapsamlı yardım etti. Öğrencinin bağımsız incelemesi, GitHub yüklemesi ve Classroom teslimi henüz tamamlanmış sayılmaz.
