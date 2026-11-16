# Bulanık sinir ağıyla robot navigasyonu

**Emirhan Efe Demir · 1306230024 · Atanan makale 16**

Referans: Jiawei Zhang (2025), DOI [10.1038/s41598-025-93926-1](https://www.nature.com/articles/s41598-025-93926-1).

Amaç, engeller arasında hedefe giden robotun beş katmanlı bulanık denetleyicisini yeniden kurmak ve GA uygunluğuna sürekli güvenli mesafe cezası eklenmesinin etkisini ölçmektir. Bu çalışma makalenin birebir tekrarı değildir. Ayrıntılı sapmalar `docs/assumptions.md`, kapsam `docs/reproduction_scope.md` içindedir.

## Kurulum ve çalıştırma
Python 3.12 önerilir. Proje klasöründe PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m src.demo
```

Linux/macOS:
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m src.demo
```
Linux'ta Tkinter ayrıca `python3-tk` sistem paketini gerektirebilir. Hazır modeller pakettedir; demo için tekrar eğitim gerekmez.

Aktif Python ile deney komutları:
```bash
python -m src.experiment --quick
python -m src.experiment
python -m src.paper_experiment
python -m src.figures
```
`src.experiment` baseline ve tüm güvenlik katsayılarını aynı protokolde birlikte eğitir; böylece seçim ve test ayrımı korunur. Sonuçlar quick/full klasörlerinde ayrı tutulur. Komut tekrar çalıştırılırsa aynı modun sonuçları yenilenir. Gerçek hesaplama süreleri doğal olarak değişir.

## Sistem
5 girdi: ön/sol/sağ engel açıklığı, hedef açı hatası, hedef uzaklığı. 80 kural, 160 öğrenilen çıkış ağırlığı. Gaussian üyelik, min t-norm, normalizasyon, ağırlıklı toplam. GA yalnızca çıkış ağırlıklarını değiştirir; merkezler/genişlikler sabittir. Çıkış v ve omega'dır. Öğrenme çevrim dışıdır. Sabit uzman öncülü, öğrenilmiş modelden açıkça ayrılır.

## Veri ve deney
Sentetik haritalar tohumlu oluşturulur, robotun sığabileceği yol ızgara aramasıyla kontrol edilir. Eğitim 8, doğrulama 8, test 30 haritadır. Beş bağımsız GA tohumu kullanılır. Her lambda için 20 birey × 20 nesil × 8 harita = 3200 değerlendirme/model. Güvenli mesafe katsayısı doğrulamada seçilir. Ham CSV, model JSON ve bütün haritalar pakettedir.

## Gerçek sonuçlar
Seçilen lambda=100. Baseline: 142/150 başarı, 7 çarpışma, 1 zaman aşımı. Proposed: 140/150 başarı, 9 çarpışma, 1 zaman aşımı. Ortalama minimum açıklık sırasıyla 0.2725 ve 0.2786 m. Başarı oranının eğitim tohumları arası örnek SS'si 2.98 ve 4.71 yüzde puandır. Bu farklar için istatistiksel anlamlılık iddiası yoktur. 135 ortak başarılı koşuda proposed yol farkı -0.0347 m'dir.

## Sınırlılıklar
Statik dairesel engeller, ideal sensörler, düşük eğitim bütçesi ve yeni hareket modeli kullanılır. Makale verileri/kodu/ölçüt tanımları eksiktir. Çalışmanın katkısı güvenlik cezasının kontrollü etkisidir; küresel optimum veya yeni algoritma iddiası değildir. Rapor ve savunma hazırlığı öğrencinin gerçek incelemesinin yerini almaz.

## Dosyalar
`src/core.py`: FNN ve fizik. `src/experiment.py`: GA ve ayrılmış deneyler. `src/demo.py`: Tkinter arayüzü. `src/figures.py`: sonuç görselleri. `data/`: haritalar. `models/`: eğitilmiş ağırlıklar. `results/full/`: ham sonuçlar. `docs/`: yöntem ve savunma. `report/` ve `presentation/`: teslim belgeleri.

## GitHub
Yerel Git geçmişi vardır; uzak depoya yüklenmemiştir. GitHub üzerinde boş depo oluşturduktan sonra:
```bash
git remote add origin https://github.com/KULLANICI/fuzzy-logic-project.git
git branch -M main
git push -u origin main
```
`KULLANICI` yerine kendi kullanıcı adını yaz. Classroom teslimi yapılmadı. Kaynaklar `references/README.md` içinde IEEE biçimindedir.
