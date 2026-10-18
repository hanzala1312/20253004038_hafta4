# İleri Python Programlama – Hafta 4 Lab Ödevi
## Üreteçler ve `functools`

- **Ders:** İleri Python Programlama
- **Kurum:** İstanbul Nişantaşı Üniversitesi
- **Öğretim Üyesi:** Dr. Öğr. Üyesi Murat Emeç
- **Dönem:** 2026–2027 Güz
- **Öğrenci:** Halil Efe Erdoğan
- **Numara:** 20253004038

## Proje Yapısı

- `uzay_oyunu/akis.py`: Görev 1 (`fibonacci`), Görev 2 (`yakit_gostergesi`), Görev 3 (`satirlari_oku`, `ayristir`, `uzun_yolculuklar`), Görev 4 (`rota_sayaci`, `onbelleksiz_rota_sayaci`, `rota_performans_karsilastir`) ve Bonus (`zamanlayici`, `tik_tak_calistir`) çözümleri.
- `uzay_oyunu/istatistik.py`: Görev 5 (`map`/`filter`/`reduce`, liste üreteci/`sum` ve `functools.partial` ile `hizli_yolculuk`) çözümleri.
- `uzay_oyunu/oyun.py`: Görev 2 kapsamında `yakit_gostergesi` ve `StopIteration` entegrasyonu eklenmiş `travel()` fonksiyonu ile `yolculuk()` fonksiyonu.
- `veri/seyir.txt`: Görev 3 seyir defteri veri dosyası.
- `tests/test_akis.py`: Tüm görevler ve bonus için birim testleri (`uv run pytest`).

## Görev 4 – Önbellekli Rota Sayacı Ölçümleri (`time.perf_counter()` ve `cache_info()`)

Mars’sız varsayılan galaksi üzerinde `"dünya"` gezegeninden başlayarak `adim=20` uzunluğundaki farklı rotaların sayısı (`4.315.343` farklı rota) önce önbelleksiz, ardından `@lru_cache` ile önbellekli sürümle ölçülmüştür:

| Sürüm | Başlangıç | Adım (`adim`) | Bulunan Rota Sayısı | Çalışma Süresi (`time.perf_counter()`) | Hızlanma |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Önbelleksiz (`onbelleksiz_rota_sayaci`)** | `"dünya"` | `20` | `4.315.343` | `2.718296 saniye` | `1x` (Baz) |
| **Önbellekli (`@lru_cache` - `rota_sayaci`)** | `"dünya"` | `20` | `4.315.343` | `0.000107 saniye` | `~25.401x daha hızlı` |

### `cache_info()` Çıktıları

- **`adim=20` çağrısı sonrasında `cache_info()` çıktısı:**
  ```text
  CacheInfo(hits=47, misses=51, maxsize=128, currsize=51)
  ```
- **Ödev föyündeki `say("dünya", 3), say("dünya", 10), say("dünya", 40)` çağrıları ve `cache_info()` çıktısı:**
  ```python
  >>> say = rota_sayaci(galaksi["baglantilar"])
  >>> say("dünya", 3), say("dünya", 10), say("dünya", 40)
  (9, 2185, 16832258606399)
  >>> say.cache_info()
  CacheInfo(hits=103, misses=109, maxsize=128, currsize=109)
  ```

### Neden Bu Kadar Hızlı?

Önbelleksiz sürümde aynı `(gezegen, adim)` alt problemleri üstel (exponential) sayıda tekrar tekrar hesaplanır. `@lru_cache` eklendiğinde ise her `(gezegen, adim)` çifti yalnızca **1 kez** (`misses=51`) hesaplanır ve sonraki tüm dallanmalarda doğrudan bellekten (`hits=47`) $O(1)$ sürede okunur. Böylece zaman karmaşıklığı $O(b^d)$ yerine $O(V \times d)$ düzeyine iner.

## Görev 5 – Okunabilirlik Karşılaştırması (`map/filter/reduce` vs. Liste Üreteci / `sum`)

- **Hangisi daha okunaklı?** Liste üreteçleri (`[g.upper() for g in ...]` ve `[g for g in ... if ...]`) ile `sum(...)` kullanımı, `map`/`filter`/`reduce` + `lambda` yazımına göre çok daha okunaklıdır.
- **Nedeni:** `filter(lambda g: ..., ...)` ve `reduce(lambda toplam, k: ..., ..., 0)` ifadelerinde `lambda` tanımları satırı uzatır ve bilişsel yükü artırır. Liste üreteçleri ise dönüştürme ve süzme mantığını tek bir doğal Python ifadesinde birleştirir; `sum()` ise toplama niyetini ilk bakışta açıkça gösterir. `map(str.upper, ...)` hazır bir fonksiyon referansı verildiğinde kısa olsa da, proje genelinde tutarlılık açısından liste üreteci daha anlaşılırdır.

## Bonus (+10) – `zamanlayici(aralik)` ve Meşgul Bekleme (`Busy-Waiting`) Açıklaması

- **Neden "Meşgul Bekleme" (`Busy-Waiting`)?**
  `zamanlayici(aralik)` üreteci, çağrıldığı her `next()` adımında o anki zamanı (`time.perf_counter()`) kontrol edip süre dolmadıysa `False`, dolduysa `True` üretir. Ana programdaki `while` döngüsü 10 saniye boyunca hiç durmadan saniyede milyonlarca kez `next(tik)` ve `next(tak)` çağrısı yapar. İşlemci (CPU) çekirdeği anlamlı bir iş yapmadığı halde sürekli saati sorguladığı için **%100 CPU kullanımıyla** çalışır; buna **meşgul bekleme (busy-waiting / polling)** denir.
- **`time.sleep()` ile Farkı Nedir?**
  `time.sleep(saniye)` çağrıldığında Python, işletim sistemi çekirdeğine (OS scheduler) ilgili iş parçacığını (thread) belirtilen süre boyunca **uyku (suspended/blocked)** durumuna almasını söyler. Bu süre boyunca program CPU döngüsü tüketmez ve işlemci diğer süreçlere ayrılır. Buna karşılık `zamanlayici(aralik)` üreteciyle kurulan ortak-yordam (coroutine) yapısı, işletim sistemi düzeyinde uyuma yapmadan aynı döngü içinde birden fazla bağımsız zamanlayıcıyı (2 sn'lik `"tik"` ve 5 sn'lik `"tak"`) tek iş parçacığında eşzamanlı (cooperative multitasking) yürütmeyi gösterir.

## Testleri Çalıştırma

```bash
uv run pytest
```
