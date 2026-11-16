"""Rapor/sunum PDF ve düzenlenebilir HTML/Markdown kaynaklarını üretir.
Ek bağımlılıklar: reportlab==4.2.5, pillow. Grafikler önce src.figures ile üretilir.
"""
import csv,json,html,statistics
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,PageBreak,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parents[1]
for folder in ['report','presentation','docs','configs','experiments/baseline','experiments/proposed','results/raw','results/tables']:(ROOT/folder).mkdir(parents=True,exist_ok=True)
font=Path('C:/Windows/Fonts/arial.ttf')
bold=Path('C:/Windows/Fonts/arialbd.ttf')
if not font.exists():
    font=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');bold=font.with_name('DejaVuSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('Body',str(font)));pdfmetrics.registerFont(TTFont('Bold',str(bold)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
summary=json.loads((ROOT/'results/full/summary.json').read_text());sel=json.loads((ROOT/'results/full/selection.json').read_text())['selected_lambda']
raw=list(csv.DictReader((ROOT/'results/full/raw.csv').open()))
training=list(csv.DictReader((ROOT/'results/full/training.csv').open()))
config=json.loads((ROOT/'results/full/config.json').read_text())
refs=(ROOT/'references/README.md').read_text(encoding='utf-8').split('İnceleme derinliği:')[0].replace('# Doğrulanmış kaynaklar','').strip()
stats={}
for method,lam in [('baseline',0),('proposed',sel)]:
    r=[x for x in raw if x['method']==method];times=[float(x['seconds']) for x in training if int(x['lam'])==lam]
    stats[method]=dict(training_mean=statistics.mean(times),training_sd=statistics.stdev(times),inference=statistics.median(float(x['inference_us']) for x in r))

# Bir blok bir rapor sayfasıdır; uzunluk ve taşma ayrıca doğrulanır.
pages=[
('1. Introduction / Giriş',[
('p','Bulanık sinir ağı ve genetik algoritma ile robot navigasyonu: güvenli mesafe cezasının kontrollü değerlendirmesi'),
('p','Emirhan Efe Demir · 1306230024 · Atanan makale: 16 · 16 Kasım 2026'),
('p','Bu proje, Jiawei Zhang’ın 2025 tarihli çalışmasının [1] bulanık kontrol bileşenini yeniden kurar ve robotun engellere fazla yaklaşmasını cezalandıran bir uygunluk terimini değerlendirir. Amaç, yalnızca hareket eden bir robot göstermek değil, yöntemin hangi kısmının kaynakla desteklendiğini ve hangi kısmının uygulama varsayımı olduğunu açıkça ayırmaktır. Sistem Python ile CPU üzerinde çalışır ve harita, model, deney ayarları ile ham sonuçları kaydeder.'),
('p','Temel araştırma sorusu, sürekli açıklık cezasının çarpışma ve hedefe ulaşma oranlarını değiştirirken yol uzunluğu ve süreyi nasıl etkilediğidir. Deney 5 bağımsız eğitim tohumu ve 30 ortak test haritası içerir. Doğrulama sonucunda seçilen katsayı 100’dür. Temel sistem 142/150, geliştirilen sistem 140/150 başarı elde etmiştir. Geliştirme, ortalama minimum açıklıkta küçük artışa rağmen çarpışmayı azaltmamıştır. Bu olumsuz bulgu, daha güvenli görünen bir eğitim hedefinin testte kendiliğinden daha güvenli davranış üretmediğini göstermektedir.'),
('h','2. Related Work / İlgili çalışmalar'),
('p','Teng ve arkadaşları [2], iki katmanlı bulanık kontrol ile yol ve görev güvenlik seviyelerinden GA uygunluk ağırlıkları üretir. Stavrinidis ve arkadaşları [3], GA’yı çoklu hedef sıralamasında kullanırken bulanık kontrolcüleri takip ve dinamik engelden kaçınmaya ayırır. Bu projenin tek hedefli, sabit katsayılı kontrolcü evrimi her iki çalışmadan farklı bir deney düzenidir. Bu iki kaynak için yayıncı özetleri ve künyeleri incelenmiştir; yöntemlerin bütün deney ayrıntıları doğrulanmış kabul edilmez.'),
('p','Jang’ın adaptif bulanık sistem çalışması [4], kurallarla sayısal öğrenmenin birlikte ele alınmasına teorik temel sağlar. Ancak burada Jang’ın hibrit öğrenmesi uygulanmaz. Gaussian öncüllerin merkezleri ve genişlikleri sabittir; GA yalnızca çıkış ağırlıklarını arar. Güvenlik cezası literatürde yeni değildir. Proje katkısı, atanan makalenin yorumlanmış temel sistemi üzerinde tek değişkenli, tekrar üretilebilir bir genişletme ve duyarlılık analizidir.'),
('p','Yönergedeki minimum yeniden gerçekleştirme kapsamı bu raporda önerilen teknik kapsamdır; öğretim elemanının onayı alınmış gibi sunulmamaktadır. Kaynakta eksik olan veri ve ölçüt tanımları nedeniyle birebir sonuç tekrarına ilişkin gereksinim kısmen karşılanır.')]),
('3. Theoretical Background / Teorik altyapı',[
('p','Bulanık küme, bir girdinin dilsel kavrama aitliğini 0 ile 1 arasında ifade eder. Örneğin 1.5 m engel açıklığı, seçilen ölçeğe göre hem “yakın” hem “uzak” kümelerini etkinleştirebilir. Üyelik derecesi olasılık değildir. Gaussian biçim, merkezden uzaklaştıkça yumuşak azalan ve her sonlu girdide negatif olmayan bir eşleşme sağlar.'),
('eq','μ<sub>ij</sub>(x<sub>i</sub>) = exp[-((x<sub>i</sub> - c<sub>ij</sub>)/σ<sub>i</sub>)²]'),
('p','Burada i girdiyi, j o girdinin dilsel kümesini, c merkezi, σ pozitif genişliği gösterir. İlk üç girdi ön/sol/sağ açıklıktır: 3 m’de kırpılır ve 3’e bölünür. Hedef açısı [-π,π) aralığına sarılıp π’ye bölünür. Hedef uzaklığı 10 m’de kırpılır ve 10’a bölünür. Böylece ölçek farkları üyelik karşılaştırmasını bozmaz.'),
('table',[['Girdi','Normalize merkezler','Genişlik'],['Ön / sol / sağ','0, 1','0.42'],['Hedef açı hatası','-1, -0.5, 0, 0.5, 1','0.30'],['Hedef uzaklığı','0, 1','0.55']]),
('p','Bütün dilsel kombinasyonlar 2×2×2×5×2=80 kural oluşturur. Her kural beş öncülün minimumunu kullanır. Bu işlem “ve” bağlacının min t-norm yorumudur. Sonra kurallar toplam etkinliğe bölünür. Toplam sayısal olarak sıfıra yaklaşırsa eşit ağırlık kullanılır; böylece tanımsız bölme engellenir.'),
('eq','α<sub>r</sub> = min<sub>i</sub> μ<sub>i,j(r,i)</sub>(x<sub>i</sub>),     ᾱ<sub>r</sub> = α<sub>r</sub> / Σ<sub>k</sub> α<sub>k</sub>'),
('eq','y<sub>l</sub> = Σ<sub>r=1..80</sub> ᾱ<sub>r</sub> w<sub>rl</sub>,     l : {hız, dönüş}'),
('p','Ağırlıklar [-1,1] aralığındadır. Doğrusal çıktı [0,1] aralığına kırpılıp 0.8 m/s ile; açısal çıktı [-1,1] aralığına kırpılıp 1 rad/s ile ölçeklenir. Sabit kural sonuçlarının ağırlıklı ortalaması Sugeno benzeri bir yorumdur. Mamdani çıktı kümelerinin alan merkezi hesaplanmaz. Öğrenme 80×2=160 ağırlığı değiştirir; üyelikler sabit kaldığından tam adaptif öncül öğrenmesi yoktur.'),
('p','Uzman öncülü, ön engel yakınsa daha açık yana dönmeyi ve hızı azaltmayı, yol açıksa hedef açı hatasına göre yönelmeyi kodlar. Başlangıç popülasyonu bu öncülün etrafında rastgele örneklenir. Öncül tek başına eğitilmiş model değildir; GA seçiliminden geçen parametreler models/full dosyalarında saklanır.')]),
('4. Original Method / Referans yöntem',[
('p','Kaynak [1], beş katmanlı FNN’nin Gaussian bulanıklaştırma, minimum, normalizasyon ve ağırlıklı çıktı adımlarını denklemler (1)-(4) ile sunar. GA bölümünde gerçek değerli bağlantı ağırlıkları kromozom olarak tanımlanır; turnuva boyutu 4, nöron sınırlarında iki noktalı çaprazlama ve sınırlı değişim açıklanır. Bu ayrıntılar yeniden kurulan sistemin ana dayanağıdır.'),
('eq','f = (7000 - t) + (1200 - d) + qv/30 + qs/20'),
('p','Kaynağın denklem (9)’unda t hedefe ulaşma süresi, d duruş anındaki hedef uzaklığı olarak anlatılır; qv ve qs’nin ayrı operasyonel tanımları eksiktir. Başarısız koşuların nasıl ele alındığı ve mesafe-zaman birimleri de açıklanmaz. Bu nedenle formülü çalıştırmak için ek seçimler gereklidir. Bu seçimler kaynak sonuçlarının aynısını ürettiği varsayımıyla kullanılamaz.'),
('p','Tam metin ve PDF görüntüsü kontrolü önemli sorunlar göstermiştir. Gaussian adı verilen denklem (1), exp ve eksi işareti içermeyen kareli uzaklıktır. Hedef koordinatı (570570570) olarak basılmıştır. Tekerlek “kuvvetleri” ile açı artışı/hız arasında boyutları açıklanmayan doğrudan ilişki kurulmuştur. Daha sonraki anlatım kromozomu yol düğümleri olarak tanımlayarak ağırlık kromozomu açıklamasından ayrılır. FNN-GA çift yönlü geri besleme iddiasının uygulanabilir güncelleme denklemleri yoktur.'),
('p','Navigasyon deneyi 40 statik/dinamik engel ve 500 örnekten söz eder. BPNN, SOM, ART ile karşılaştırma verilir. Şekil 4 başlığı doğruluk olmasına rağmen çizilen eksen süre ve değerler Şekil 5 zamanlarıyla uyumludur. Bu raporda doğruluk sayıları grafik ölçümü olarak değil, metinde bildirilen kaynak sonuçları olarak ele alınır. Özetteki en kısa 9.64 s ifadesi de hedef 3 için metinde verilen 8.68 s ile uyuşmaz.'),
('table',[['Kaynak konumu','Bildirilen değer','Bizim ölçütümüzle ilişki'],['Hedef 1, metin','%98.64 accuracy','Başarı oranıyla eşitlenmez'],['Hedef 1, Şekil 5','9.64 s','Farklı fizik ve koşullar'],['Hedef 2, Tablo 1','%1.52 sapma','Açı hata tanımı eksik'],['0 engel, Tablo 2','%99.12 verim','Operasyonel tanım eksik']]),
('p','Data availability bölümü veri için yazara başvurulmasını ister. Makale içinde resmi kod deposu bağlantısı tespit edilmemiştir. Haritalar, bütün ağ parametreleri ve özgün deney örnekleri elde olmadan sayısal eşleşme doğrulanamaz. Lisans CC BY-NC-ND 4.0’dır; kaynak PDF ve makale görselleri bu pakette yeniden dağıtılmaz.')]),
('5. Reproduction Methodology / Yeniden gerçekleştirme',[
('p','Uygulama, kaynakta daha ayrıntılı verilen ağırlık kromozomu yorumunu seçer. FNN çıkışlarını yol kromozomuna dönüştüren ikinci mekanizma kullanılmaz. Ağ katmanlarının sırası korunur; üyelik denklemi geçerli Gaussian biçimiyle tamamlanır. Girdi sayıları, üyelik merkezleri, genişlikler ve bütün kural kombinasyonları proje kararlarıdır. Aynı kararlar baseline ve proposed için aynıdır.'),
('p','Fizik ortamı 10×10 m’dir. Robot 0.18 m yarıçaplı bir disk, engeller 0.25–0.55 m yarıçaplı statik dairelerdir. Adım 0.2 s, en fazla 250 adım, hedef toleransı 0.30 m’dir. Başlangıç x=0.6 m, hedef x=9.4 m, y konumları tohumla üretilir. Engel merkezleri x=1.7–8.3 m ve y=0.8–9.2 m arasında seçilir. Dolayısıyla bu, genel depoları temsil eden tarafsız bir harita dağılımı değildir.'),
('eq','θ<sub>k+1</sub> = wrap(θ<sub>k</sub> + ω<sub>k</sub>Δt)'),
('eq','p<sub>k+1</sub> = p<sub>k</sub> + v<sub>k</sub>Δt [cos θ<sub>k+1</sub>, sin θ<sub>k+1</sub>]'),
('p','Her sayısal adım düz doğru parçası olarak kabul edilir. Bu parçaya engel merkezinin minimum uzaklığından engel ve robot yarıçapları çıkarılarak çarpışma kontrol edilir. Böylece uç noktaları güvenli olsa bile engelin içinden atlama yakalanır. Bu hesap parçalı doğrusal modele göre kesindir; sürekli diferansiyel sürüş yayı için tam fizik doğruluğu iddiası değildir. Dünya sınırı da robot yarıçapıyla kontrol edilir.'),
('p','Harita geçilebilirliği 0.2 m ızgarada dört komşulu BFS ile, her kenarın süpürülen disk açıklığı doğrulanarak kontrol edilir. Bu arama kontrolcüye yol vermez. Yalnızca geçilebilir haritaları seçer. Izgara çözünürlüğü nedeniyle gerçekten geçilebilir dar bir haritayı reddedebilir; bu da deney dağılımını kolaylaştırabilir.'),
('p','Seçilen temel deney, kaynağın “Path planning experiment” bölümündeki Şekil 6/Tablo 2 engel sayısı taramasıdır. 0,2,4,6,8,10 engel için ayrı haritalarda beşer GA çalıştırılmıştır. Sonuçlar paper_approximation.csv içindedir. Orijinal harita, Visual C++ 6.0 donanımı ve süre tanımı bilinmediğinden bu yaklaşık tekrar, yayın sürelerini doğrulamaz. Buradaki harita üzerinde eğitim değerlendirmesi ana genelleme testinden ayrıdır.'),
('p','Kontrolcüde tekerlek kuvveti yerine v ve ω kullanılır. İdeal diferansiyel sürüş dönüşümü vL=v-bω/2 ve vR=v+bω/2’dir; b dingil açıklığıdır. Simülasyonun bu dönüşüme ihtiyacı yoktur ve motor, kayma, ivmelenme veya tekerlek dinamiği içermez.')]),
('6. Proposed Extension / Önerilen geliştirme',[
('p','Temel uygunluk denkleminde çarpışmasız adımlar zaten ödüllendirilmektedir. Yeni terim, çarpışmadan önce riskli yakın geçişleri de ayırt eden sürekli bir açıklık cezasıdır. Robot ve engel yüzeyleri arası minimum açıklık c, güvenli eşik c*=0.6 m olmak üzere her adımın kareli açığı hesaplanır. Dünya sınırları da c içinde bulunduğundan bu terim yalnızca engel mesafesini değil, sınır açıklığını da kapsar.'),
('eq','P = (1/K) Σ<sub>k=1..K</sub> max(0, (0.6 - c<sub>k</sub>)/0.6)²'),
('eq','F<sub>λ</sub> = F<sub>0</sub> - λP'),
('p','K koşunun gerçekleşen adım sayısıdır. Ortalama alınması yalnızca uzun sürdüğü için bir yolun daha büyük ceza biriktirmesini azaltır. Bununla birlikte aynı ortalama, kısa fakat çok riskli bir bölgeyi diğer adımlarla seyreltebilir. Bu seçim güvenlik garantisi sağlamaz. Sabit lambda ve güvenli eşik, açıklık-süre-başarı dengesini değiştiren hiperparametrelerdir.'),
('h','7. Experimental Setup / Deney düzeni'),
('p','Temel formülün uygulama yorumu: t başarılı koşuda adım sayısı, başarısız koşuda 7000; d son hedef uzaklığının 60 katı; qv çarpışmasız ve |Δθ|<0.1 olan adım sayısı; qs bütün çarpışmasız adımlar. Başarısızlık için 7000 değeri, erken çarpışmanın kısa süre nedeniyle ödüllendirilmesini önleyen proje seçimidir. Bu ölçekler makaleden doğrulanmış birim dönüşümü değildir.'),
('table',[['Ayar','Değer'],['Eğitim / doğrulama / test haritaları','8 / 8 / 30, ayrık tohumlar'],['Bağımsız GA tohumları','11, 22, 33, 44, 55'],['Popülasyon / nesil / elit','20 / 20 / 2'],['Turnuva / gen mutasyon olasılığı','4 / 0.12'],['Lambda adayları','0, 100, 400, 1000'],['Model başına bütçe','3200 harita değerlendirmesi']]),
('p','İki noktalı çaprazlama kural bloklarının sınırlarında yapılır. Mutasyon en büyük adımı nesillerle azaltır ve ağırlıkları [-1,1] aralığında tutar. Başlangıç popülasyonları ve rastgele dizi aynı tohumda lambda’lar arasında eşleştirilmiştir. Katsayı pozitif adaylardan doğrulama başarısı, daha az çarpışma, daha yüksek açıklık ve daha küçük lambda sırasıyla seçilir. Test haritaları bu karara katılmaz. Çalışma Python '+config['python']+' ve NumPy '+config['numpy']+' ile Windows üzerinde yürütülmüştür. quick modu ayrı dosyalara yazar.')]),
('8. Results / Sonuçlar',[
('table',[['Ölçüt','Baseline','Proposed (λ=100)'],['Başarı','142 / 150','140 / 150'],['Çarpışma','7 / 150','9 / 150'],['Zaman aşımı','1 / 150','1 / 150'],['Tohum başarı oranı ort. ± SS','%94.67 ± 2.98 puan','%93.33 ± 4.71 puan'],['Min. açıklık, tüm koşular ort.','0.2725 m','0.2786 m'],['Yol, yalnız başarılı koşular','10.4504 m (n=142)','10.3804 m (n=140)'],['Süre, yalnız başarılı koşular','20.2493 s','19.5257 s']]),
('img','outcomes.png'),
('p','Paydalar beş eğitimin aynı 30 test haritasındaki toplamıdır. 150 koşu, 150 bağımsız eğitim deneyi değildir. Başarı oranı standart sapması beş tohum üzerinden hesaplanır. İki yöntemin de başarılı olduğu 135 eşleşmiş koşuda proposed eksi baseline yol farkı -0.0347 m’dir. Başarıya koşullu ortalama yoldaki -0.0700 m farkı, farklı başarılı alt kümelerden de etkilenir.'),
('p',f"Model başına GA eğitim süresi baseline {stats['baseline']['training_mean']:.3f} ± {stats['baseline']['training_sd']:.3f} s, proposed {stats['proposed']['training_mean']:.3f} ± {stats['proposed']['training_sd']:.3f} s ölçülmüştür. Tek satırlı kontrolcü çağrılarının medyanı sırasıyla yaklaşık {stats['baseline']['inference']:.1f} ve {stats['proposed']['inference']:.1f} µs’dir. Bu mikro ölçüm sensör/arayüz maliyetini içermez. Donanım yüküne bağlı gerçek süreler, simülasyon saniyesinden ve makalenin planlama süresinden farklıdır.")]),
('9. Discussion / Tartışma',[
('p','Güvenli mesafe terimi testte ortalama minimum açıklığı yaklaşık 6.1 mm artırmıştır. Ancak başarı iki koşu düşmüş ve çarpışma iki koşu artmıştır. Bu sonuç, katkının testte daha güvenli olduğunu desteklemez. Beş eğitim tekrarı küçük bir örneklem olduğundan farkların istatistiksel anlamlı olduğu söylenemez. Aynı haritaların bütün tohumlarda kullanılması harita ve model belirsizliğini iç içe geçirir.'),
('img','ablation.png'),
('p','Pozitif katsayıların doğrulamadaki başarı sayıları birbirine yakındır. Seçim kuralı lambda=100’ü belirlemiştir. Test sonucunu gördükten sonra daha iyi görünen bir katsayı seçilmemiştir. Eğitim haritalarının azlığı, uzman öncülünün oluşturduğu başlangıç yanlılığı ve düşük nesil sayısı genelleme farkının olası nedenleridir. Bunlar deneyle ayrı ayrı doğrulanmış nedensel açıklamalar değildir.'),
('p','Güvenli açıklık ödülü ile hedefe ulaşma arasında bir ödünleşim vardır. Engel çevresinde daha geniş dönüş güvenlik payını artırabilir, fakat hedefin çevresinde dönmeye veya zaman aşımına yol açabilir. Sensör vektöründe dünya duvarlarının bulunmaması da sınıra yaklaşırken yeterli uyarı üretmeyebilir. Güvenlik teriminin bütün adımlar üzerinde ortalama olması yerel riskleri saklayabilir.'),
('p','Yakınsama eğrisi her neslin en iyi uygunluk değerini ve tohumlar arası standart sapmayı gösterir. Farklı lambda’lar farklı amaç fonksiyonları kullandığı için eğrilerin mutlak yükseklikleri doğrudan performans sıralaması değildir. Test başarı/çarpışma ve ortak başarılı koşu karşılaştırması asıl değerlendirmedir. Sonraki çalışma, eğitim haritası sayısı ve popülasyon bütçesini yalnızca yeni bir deney protokolünde artırmalıdır.')]),
('10. Limitations / Sınırlılıklar',[
('p','Çalışma orijinal yöntemin sayısal birebir tekrarı değildir. Kaynak veri, tam kural tablosu, ağ parametreleri, haritalar ve ölçüt tanımları eksiktir. Gaussian ifade gerekçeli biçimde tamamlanmış, farklı koordinat ve hareket modeli seçilmiştir. FNN-GA çevrim içi geri beslemesi, BPNN/SOM/ART karşılaştırmaları, 40 dinamik engelli depo ve 500 örneklik deney uygulanmamıştır. Minimum yeniden gerçekleştirme gereksiniminin birebir deney kısmı bu nedenle kısmi kalır.'),
('p','Sentetik dairesel engeller, ideal gözlem ve sabit robot boyutu fiziksel gerçekliği sınırlar. Başlangıç-hedef x düzeni ve geçilebilirlik filtresi harita çeşitliliğini azaltır. Ağın öncülleri sabittir. Öğrenme bütçesi küçüktür ve istatistiksel çıkarım yalnızca betimseldir. Çarpışma kontrolü sayısal doğru parçaları için geçerlidir. Demo fiziksel bir robota doğrudan sürüş komutu vermek için doğrulanmamıştır.'),
('h','11. Conclusion / Sonuç'),
('p','Beş katmanlı bulanık denetleyici, GA ile çıkış ağırlığı öğrenimi, açıklanabilir canlı demo ve tekrar üretilebilir deney hattı gerçekleştirilmiştir. Yaklaşık engel sayısı taraması ve ayrı genelleme deneyi çalıştırılmıştır. Güvenli mesafe cezası ortalama açıklığı az miktarda artırsa da testte çarpışmayı azaltmamıştır. Katkının değeri, başarı iddiasından çok bu etkinin adil ve görünür biçimde ölçülmesidir.'),
('p','Gelecek çalışma için önceden tanımlanmış yeni protokolde daha geniş eğitim haritaları, duvar algısı, gürültü, dinamik engeller ve minimum açıklığa odaklı farklı risk özetleri değerlendirilebilir. Makale verileri elde edilirse ayrıca gerçek bir tekrar planlanmalıdır. Aynı test setine sürekli ayar yapmak bağımsız test özelliğini kaybettirir.'),
('h','Generative AI Usage Disclosure'),
('p','ChatGPT/Codex; makale incelemesi, kaynak araması, kod yazımı, hata ayıklama, deney yürütme, grafik, rapor ve sunum taslağı üretiminde kapsamlı olarak kullanılmıştır. Dosyalardaki deneyler araç ortamında gerçekten çalıştırılmıştır. Öğrencinin bütün kodu ve bulguları henüz bağımsız olarak doğruladığı ileri sürülmemektedir. Öğrenci, teslim öncesinde yöntemi incelemeli, komutları kendi ortamında çalıştırmalı ve çıktıları açıklayabilmelidir.'),
('p','Teslim durumu: Yerel Git deposu ve gerçek aşama commit’leri hazırlanmıştır. GitHub’a yükleme ve Classroom teslimi yapılmamıştır. Öğretim elemanı kapsam onayı alınmamıştır. Sunum PDF ve düzenlenebilir HTML kaynağı sağlanır; PPTX üretimi mevcut çalışma ortamındaki bağımlılık erişim hatası nedeniyle tamamlanamamıştır. Masaüstü demo işlevleri programatik kontrol edilmiştir; ekran yakalama engeli nedeniyle görsel masaüstü denetimi tamamlanamamıştır.')]),
('References / Kaynaklar',[('p',p) for p in refs.split('\n\n')])
]

style=ParagraphStyle('body',fontName='Body',fontSize=10.5,leading=15.3,textColor=HexColor('#243448'),spaceAfter=9)
hstyle=ParagraphStyle('h',parent=style,fontName='Bold',fontSize=14,leading=19,spaceBefore=10,spaceAfter=10)
title=ParagraphStyle('title',parent=hstyle,fontSize=21,leading=26,spaceAfter=19)
eqstyle=ParagraphStyle('equation',parent=style,fontSize=12,leading=18,leftIndent=12,spaceBefore=5,spaceAfter=12)
def par(t,sty=style):return Paragraph(t,sty)
def footer(c,doc):
    c.setStrokeColor(HexColor('#b8cbd9'));c.line(42,35,553,35);c.setFont('Body',8);c.setFillColor(HexColor('#536a7a'));c.drawString(42,23,'Emirhan Efe Demir · Bulanık Mantık Dönem Projesi');c.drawRightString(553,23,str(doc.page))
story=[];markdown=[]
for pi,(name,blocks) in enumerate(pages):
    if pi:story.append(PageBreak())
    story.append(par(name,title));markdown+=['# '+name,'']
    for kind,value in blocks:
        if kind in ['p','h','eq']:
            story.append(par(value,hstyle if kind=='h' else eqstyle if kind=='eq' else style));markdown+=[('## ' if kind=='h' else '')+value,'']
        elif kind=='img':
            story.append(Image(str(ROOT/'results/figures'/value),width=480,height=240));story.append(Spacer(1,8));markdown+=[f'![Deney grafiği](../results/figures/{value})','']
        elif kind=='table':
            widths=[150,150,210] if len(value[0])==3 else [240,270]
            t=Table([[par(str(c),ParagraphStyle('cell',parent=style,fontSize=9,leading=12,spaceAfter=0)) for c in row] for row in value],colWidths=widths,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#e2edf3')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#d2dde5'))]));story.extend([t,Spacer(1,12)])
            markdown+=['| '+' | '.join(row)+' |' for row in [value[0],['---']*len(value[0])]+value[1:]]+['']
SimpleDocTemplate(str(ROOT/'report/report.pdf'),pagesize=(595.28,841.89),leftMargin=42,rightMargin=42,topMargin=40,bottomMargin=48,title='Bulanık Robot Navigasyonu',author='Emirhan Efe Demir').build(story,onFirstPage=footer,onLaterPages=footer)
(ROOT/'report/report.md').write_text('\n'.join(markdown),encoding='utf-8')

slides=[
('Bulanık robot navigasyonu','Güvenli mesafe cezasının kontrollü değerlendirmesi\nEmirhan Efe Demir · 1306230024\nMakale 16 · 2026',None,'1 dakika: Problemi ve tek değişkenli katkıyı anlat. Sonuçların tamamen iyileşme göstermediğini baştan belirt.'),
('Problem ve araştırma sorusu','Robot engeller arasında hedefe ulaşmalı.\nYakın geçişleri cezalandırmak çarpışmayı azaltıyor mu?\nBaşarı, açıklık, yol ve süre birlikte değerlendirildi.', 'trajectories.png','1 dakika: Mavi ve yeşil yollar aynı haritada farklı modellerdir. Bu görsel önceden çizilmiş demo değildir; kayıtlı modelin core.py ile yeniden koşusudur.'),
('Literatürde yöntemlerin rolü','Zhang [1]: FNN navigasyonu ve GA ağırlık/yol anlatımı.\nTeng vd. [2]: Güvenlik seviyelerinden GA ağırlıkları.\nStavrinidis vd. [3]: GA ile hedef sıralaması, bulanık takip.\nBu proje: Tek hedef, öğrenilen çıkış ağırlıkları.',None,'1.5 dakika: [2] ve [3] özet/künye düzeyinde incelendi. Güvenlik cezasının dünyada yeni olduğunu iddia etme. Kaynaklar references/README.md.'),
('Beş katmanlı bulanık ağ','5 normalize girdi\nGaussian üyelikler\n80 kuralda minimum etkinlik\nToplama bölerek normalizasyon\n160 ağırlıkla iki kontrol çıktısı',None,'1.5 dakika: Her kural beş üyelik derecesinin minimumudur. Normalize etkinlikler toplamı birdir. Çıktı ağırlıkları GA ile öğrenilir; merkez ve genişlikler sabittir.'),
('Üyelik ve çıktı hesabı','μ = exp[-((x-c)/σ)²]\nαr = min μi  ve  ᾱr = αr / Σαk\ny = Σ ᾱr wr\nÇıkışlar: v : [0, 0.8] m/s, ω : [-1, 1] rad/s',None,'1.5 dakika: sigma büyüdükçe kümeler daha fazla örtüşür. Bu bir olasılık dağılımı değildir. Mamdani alan merkezi ve Jang hibrit ANFIS öğrenmesi uygulanmadı.'),
('Makaleye sadakat ve belirsizlikler','Korunan: Katman sırası, min, normalizasyon, ağırlık kromozomu.\nTamamlanan: Gaussian ifade, kural sayısı, fizik ve ölçütler.\nEksik kaynaklar: Haritalar, ham veri, kesin parametreler.\nBirebir tekrar gereksinimi kısmen karşılanıyor.',None,'1.5 dakika: Denklem 1 exp/eksi içermiyor. Hedef koordinatı bozuk. Şekil 4 başlığı ile ekseni çelişiyor. Bunları kaynak PDF ile göster; yazara ait kesin düzeltme gibi sunma.'),
('Simülasyon ve çarpışma kontrolü','10×10 m dünya, 0.18 m yarıçaplı robot\n0.2 s adım, 50 s zaman aşımı\nSüpürülen disk: hareket boyunca çarpışma kontrolü\nIzgara araması yalnızca haritanın geçilebilirliğini doğrular.', 'trajectories.png','1 dakika: Izgara araması robotu yönlendirmez. Sayısal adım doğru parçasıdır. Dinamik engel, kayma ve sensör gürültüsü yoktur.'),
('Genetik algoritma','20 birey, 20 nesil, 2 elit\n4 adaylı turnuva seçilimi\nKural sınırlarında iki noktalı çaprazlama\nAzalan gen mutasyonu, ağırlık sınırı [-1,1]', 'convergence.png','1.5 dakika: Aynı tohumlarda başlangıç popülasyonu ve bütçe eşittir. Çıkış ağırlıkları öğrenilir. Lambda farklı amaç fonksiyonu olduğundan eğri yüksekliği tek başına karşılaştırma değildir.'),
('Özgün katkı: açıklık cezası','P = ortalama max(0, (0.6-c)/0.6)²\nFλ = F0 - λP\nYakın geçişleri, çarpışma olmadan da cezalandırır.\nDeğişen tek bileşen bu terimdir.',None,'1 dakika: c robot-engel yüzey açıklığıdır; dünya sınırları da dahildir. Ortalama ceza tehlikeli kısa bölgeyi seyreltebilir. Güvenlik garantisi yoktur.'),
('Deney ve katsayı seçimi','8 eğitim, 8 doğrulama, 30 test haritası\n5 bağımsız eğitim tohumu\nλ adayları: 0, 100, 400, 1000\nDoğrulama seçimi λ=100; test seçimde kullanılmadı.', 'ablation.png','1 dakika: Test haritaları aynı modeller arasında eşleşmiştir. 150 koşu 150 eğitim tohumu değildir. Pozitif lambda seçim kuralı önceden belirlenmiştir.'),
('Test sonuçları','Baseline: 142/150 başarı, 7 çarpışma\nProposed: 140/150 başarı, 9 çarpışma\nHer iki yöntemde 1 zaman aşımı\nBaşarı artışı veya güvenlik üstünlüğü gözlenmedi.', 'outcomes.png','1.5 dakika: Başarı oranı tohum SS baseline 2.98, proposed 4.71 yüzde puan. Farkın istatistiksel anlamlı olduğunu söyleme.'),
('Açıklık ve yol ödünleşimi','Ortalama minimum açıklık: 0.2725 → 0.2786 m\n135 ortak başarıda yol farkı: -0.0347 m\nBaşarılı alt kümeler farklıysa yol ortalaması yanıltabilir.', 'density.png','1 dakika: Başarısız koşuları oranlardan çıkarma. Yaklaşık 6 mm açıklık farkı fiziksel robotta güvenlik kanıtı değildir.'),
('Sınırlılıklar ve sonuç','Kaynak deneyler birebir doğrulanamadı.\nStatik engeller, ideal sensörler ve küçük eğitim bütçesi kullanıldı.\nGüvenlik terimi test çarpışmalarını azaltmadı.\nYeni deneyler yeni bir değerlendirme protokolü gerektirir.',None,'1 dakika: Negatif sonuç saklanmadı. Öğrenci yöntemi incelemeli ve savunabilmeli. Yapay zekâ kapsamlı kullanıldı, öğrencinin doğrulaması henüz yapılmış sayılmıyor.'),
('Canlı demo ve teknik savunma','python -m src.demo\nAynı haritada iki modeli karşılaştır.\nHedefi değiştir, engel ekle veya sil.\nÜyelikleri ve en etkin kuralları incele.',None,'Sunum sonrası 5 dakika: docs/demo_guide.md akışını izle. Yeniden eğitim gerekmez. Bir başarısız örneği göster ve nedenini kesinlik iddiası olmadan yorumla.')]

c=canvas.Canvas(str(ROOT/'presentation/presentation.pdf'),pagesize=(960,540));c.setTitle('Bulanık Robot Navigasyonu');c.setAuthor('Emirhan Efe Demir')
htmlslides=[];notes=[]
for i,(name,body,img,note) in enumerate(slides):
    c.setFillColor(HexColor('#f7f9fc'));c.rect(0,0,960,540,fill=1,stroke=0)
    heading=Paragraph(name,ParagraphStyle('st',fontName='Bold',fontSize=30,leading=36,textColor=HexColor('#153653')));_,hh=heading.wrap(860,90);heading.drawOn(c,50,490-hh)
    font_size=19 if img else 23;content=Paragraph('<br/><br/>'.join(html.escape(x) for x in body.split('\n')),ParagraphStyle('sb',fontName='Body',fontSize=font_size,leading=font_size*1.35,textColor=HexColor('#30475e')))
    cw=380 if img else 830;_,ch=content.wrap(cw,370);content.drawOn(c,50,400-ch)
    if img:c.drawImage(str(ROOT/'results/figures'/img),450,115,width=470,height=280,preserveAspectRatio=True,anchor='c',mask='auto')
    c.setFont('Body',10);c.setFillColor(HexColor('#5a7084'));c.drawString(50,28,'Emirhan Efe Demir · 1306230024');c.drawRightString(910,28,f'{i+1:02d} / {len(slides):02d}');c.showPage()
    im=f'<img src="../results/figures/{img}" alt="Gerçek deney sonuçları">' if img else ''
    htmlslides.append(f'<section><h1>{html.escape(name)}</h1><div class="content"><p>{"<br><br>".join(html.escape(x) for x in body.split(chr(10)))}</p>{im}</div><footer>{i+1} / {len(slides)} · Emirhan Efe Demir</footer></section>')
    notes += [f'## Slayt {i+1}: {name}',note,'']
c.save()
(ROOT/'presentation/presentation.html').write_text('<!doctype html><html lang="tr"><meta charset="utf-8"><title>Bulanık Robot Navigasyonu</title><style>body{margin:0;background:#dbe3eb;font-family:Arial,sans-serif;color:#153653}section{box-sizing:border-box;width:1280px;min-height:720px;padding:60px;margin:20px auto;background:#f7f9fc;position:relative;page-break-after:always}h1{font-size:40px;margin:0 0 60px}p{font-size:27px;line-height:1.35;margin:0;flex:1}.content{display:flex;align-items:center;gap:36px}img{width:600px;object-fit:contain}footer{position:absolute;bottom:30px;font-size:15px;color:#60788d}@media print{@page{size:13.333in 7.5in;margin:0}body{background:white}section{width:1280px;height:720px;margin:0}}</style>'+''.join(htmlslides)+'</html>',encoding='utf-8')
(ROOT/'presentation/speaker_notes.md').write_text('# Konuşmacı notları\n\nHedef ana sunum 17-19 dakika, demo/soru-cevap ayrıca 5 dakika.\n\n'+'\n'.join(notes)+'\n## Kaynaklar\n'+refs,encoding='utf-8')
(ROOT/'configs/full.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
for method,lam in [('baseline',0),('proposed',sel)]:
    (ROOT/f'experiments/{method}/README.md').write_text(f'# {method}\n\nLambda={lam}. `python -m src.experiment` iki yöntemi ortak protokolde yürütür. Model dosyaları models/full, ham sonuçlar results/full/raw.csv içindedir.\n',encoding='utf-8')
(ROOT/'results/raw/README.md').write_text('# Ham kayıtlar\n\nKanonik ham kayıtlar ../full/raw.csv, validation.csv, training.csv ve paper_approximation.csv dosyalarıdır. Quick kayıtları ayrı klasördedir. Kopya dosya oluşturulmaz.\n',encoding='utf-8')
paper=[['obstacles','GA_seconds_reported','GA_efficiency_percent_reported'],[0,.128,99.12],[2,.366,99.00],[4,.651,98.84],[6,.942,98.61],[8,1.358,98.26],[10,1.652,98.05]]
with (ROOT/'results/tables/paper_reference.csv').open('w',newline='',encoding='utf-8') as f:csv.writer(f).writerows(paper)
(ROOT/'docs/runtime_statistics.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
print('Report PDF + Markdown, 14-slide PDF + editable HTML, speaker notes generated.')
