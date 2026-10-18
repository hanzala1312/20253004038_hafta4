"""Hafta 4 Lab: Üreteçler, veri işleme boru hattı, önbellekli rota sayacı ve zamanlayıcı."""
from __future__ import annotations

import time
from collections.abc import Callable, Iterable, Iterator
from functools import lru_cache
from itertools import islice, takewhile
from pathlib import Path
from typing import Any


# ============================================================================
# Görev 1 – Fibonacci üreteci (15 puan)
# ============================================================================

def fibonacci() -> Iterator[int]:
    """Sonsuz Fibonacci sayı dizisi üreteci.

    Her çağrıda sıradaki Fibonacci sayısını (0, 1, 1, 2, 3, 5, 8, ...) üretir.

    Yields:
        int: Sıradaki Fibonacci sayısı.
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def fibonacci_ilk_uc() -> tuple[int, int, int]:
    """next() kullanarak Fibonacci üretecinden ilk üç değeri alır.

    Returns:
        tuple[int, int, int]: İlk üç Fibonacci sayısı (0, 1, 1).
    """
    g = fibonacci()
    return next(g), next(g), next(g)


def fibonacci_ilk_n(n: int = 12) -> list[int]:
    """itertools.islice kullanarak ilk n Fibonacci sayısını liste olarak döndürür.

    Args:
        n (int): Alınacak eleman sayısı. Varsayılan 12.

    Returns:
        list[int]: İlk n Fibonacci sayısı.
    """
    return list(islice(fibonacci(), n))


def fibonacci_esikten_kucuk(esik: int = 100) -> list[int]:
    """itertools.takewhile ile verilen eşikten küçük Fibonacci sayılarını döndürür.

    Args:
        esik (int): Üst sınır (hariç). Varsayılan 100.

    Returns:
        list[int]: Eşik değerinden küçük Fibonacci sayıları.
    """
    return list(takewhile(lambda x: x < esik, fibonacci()))


# ============================================================================
# Görev 2 – Yakıt göstergesi (20 puan)
# ============================================================================

def yakit_gostergesi(yakit: int, tuketim: int) -> Iterator[int]:
    """Her adımda yakıtı tüketim kadar azaltıp kalan yakıtı üreten üreteç.

    Yakıt 0'a inince 0 değerini üretir ve bir sonraki çağrıda StopIteration
    ile durur.

    Args:
        yakit (int): Başlangıç yakıt miktarı.
        tuketim (int): Her yolculukta harcanacak yakıt miktarı.

    Yields:
        int: Yolculuk sonrası kalan yakıt miktarı (en az 0).
    """
    if tuketim <= 0:
        raise ValueError("Tüketim miktarı pozitif bir tam sayı olmalıdır.")

    while yakit > 0:
        yakit = max(0, yakit - tuketim)
        yield yakit


# ============================================================================
# Görev 3 – Seyir defteri boru hattı (25 puan)
# ============================================================================

def satirlari_oku(yol: str | Path) -> Iterator[str]:
    """Dosyayı satır satır tembel (lazy) olarak okur; boş ve '#' ile başlayanları atlar.

    Hiçbir aşamada tüm dosyayı bellekte bir listeye okumaz.

    Args:
        yol (str | Path): Okunacak seyir defteri dosyasının yolu.

    Yields:
        str: Başındaki/sonundaki boşlukları temizlenmiş geçerli satır.
    """
    with open(yol, "r", encoding="utf-8") as dosya:
        for satir in dosya:
            temiz = satir.strip()
            if not temiz or temiz.startswith("#"):
                continue
            yield temiz


def ayristir(satirlar: Iterable[str]) -> Iterator[tuple[str, str, int]]:
    """'kaynak -> hedef yakit' biçimindeki satırlardan (kaynak, hedef, yakit) demeti üretir.

    Args:
        satirlar (Iterable[str]): İşlenecek satır akışı.

    Yields:
        tuple[str, str, int]: (kaynak gezegen, hedef gezegen, harcanan yakıt) demeti.
    """
    for satir in satirlar:
        sol, sag = satir.split("->")
        kaynak = sol.strip()
        hedef_parcalari = sag.strip().split()
        hedef = hedef_parcalari[0]
        yakit = int(hedef_parcalari[1])
        yield (kaynak, hedef, yakit)


def uzun_yolculuklar(
    kayitlar: Iterable[tuple[str, str, int]], esik: int
) -> Iterator[tuple[str, str, int]]:
    """Yakıt tüketimi verilen eşik değerinden büyük olan yolculuk kayıtlarını süzer.

    Args:
        kayitlar (Iterable[tuple[str, str, int]]): (kaynak, hedef, yakit) demetleri akışı.
        esik (int): Yakıt alt sınırı (kesin büyük olanlar süzülür: yakit > esik).

    Yields:
        tuple[str, str, int]: Eşik değerini aşan (kaynak, hedef, yakit) demeti.
    """
    for kaynak, hedef, yakit in kayitlar:
        if yakit > esik:
            yield (kaynak, hedef, yakit)


# ============================================================================
# Görev 4 – Önbellekli rota sayacı (25 puan)
# ============================================================================

def onbelleksiz_rota_sayaci(
    baglantilar: dict[str, list[str]]
) -> Callable[[str, int], int]:
    """Önbellek (@lru_cache) kullanmadan rota sayısını hesaplayan fonksiyon döndürür.

    Performans karşılaştırması (time.perf_counter) için kullanılır.

    Args:
        baglantilar (dict[str, list[str]]): Gezegenlerin komşuluk sözlüğü.

    Returns:
        Callable[[str, int], int]: rota_sayisi(gezegen, adim) fonksiyonu.
    """
    def rota_sayisi(gezegen: str, adim: int) -> int:
        """Verilen gezegenden başlayıp tam 'adim' yolculuk yapan farklı rota sayısı."""
        if adim < 0:
            raise ValueError("Adım sayısı negatif olamaz.")
        if adim == 0:
            return 1
        return sum(
            rota_sayisi(komsu, adim - 1)
            for komsu in baglantilar.get(gezegen, [])
        )

    return rota_sayisi


def rota_sayaci(
    baglantilar: dict[str, list[str]]
) -> Callable[[str, int], int]:
    """İçinde @lru_cache ile süslenmiş rota_sayisi(gezegen, adim) fonksiyonunu döndürür.

    Args:
        baglantilar (dict[str, list[str]]): Gezegenlerin komşuluk sözlüğü.

    Returns:
        Callable[[str, int], int]: Önbellekli rota_sayisi(gezegen, adim) fonksiyonu.
    """
    @lru_cache
    def rota_sayisi(gezegen: str, adim: int) -> int:
        """Verilen gezegenden başlayıp tam 'adim' yolculuk yapan farklı rota sayısı."""
        if adim < 0:
            raise ValueError("Adım sayısı negatif olamaz.")
        if adim == 0:
            return 1
        return sum(
            rota_sayisi(komsu, adim - 1)
            for komsu in baglantilar.get(gezegen, [])
        )

    return rota_sayisi


def rota_performans_karsilastir(
    baglantilar: dict[str, list[str]],
    gezegen: str = "dünya",
    adim: int = 20,
) -> dict[str, Any]:
    """Önbelleksiz ve @lru_cache'li rota_sayisi sürümlerini time.perf_counter() ile ölçer.

    Args:
        baglantilar (dict[str, list[str]]): Gezegenlerin komşuluk sözlüğü.
        gezegen (str): Başlangıç gezegeni. Varsayılan "dünya".
        adim (int): Adım sayısı. Varsayılan 20.

    Returns:
        dict[str, Any]: Sonuç, önbelleksiz süre, önbellekli süre ve cache_info bilgisi.
    """
    say_onbelleksiz = onbelleksiz_rota_sayaci(baglantilar)
    baslangic_1 = time.perf_counter()
    sonuc_1 = say_onbelleksiz(gezegen, adim)
    sure_onbelleksiz = time.perf_counter() - baslangic_1

    say_onbellekli = rota_sayaci(baglantilar)
    baslangic_2 = time.perf_counter()
    sonuc_2 = say_onbellekli(gezegen, adim)
    sure_onbellekli = time.perf_counter() - baslangic_2

    assert sonuc_1 == sonuc_2
    return {
        "sonuc": sonuc_2,
        "onbelleksiz_sure": sure_onbelleksiz,
        "onbellekli_sure": sure_onbellekli,
        "cache_info": say_onbellekli.cache_info(),
    }


# ============================================================================
# Bonus (+10 puan) – Zamanlayıcı üreteci ve Meşgul Bekleme (Busy-Waiting)
# ============================================================================
# Açıklama (Meşgul Bekleme vs. time.sleep):
# Aşağıdaki `zamanlayici(aralik)` üreteci ve `tik_tak_calistir` döngüsü bir
# "meşgul bekleme" (busy-waiting / polling) örneğidir. Çünkü `while` döngüsü
# 10 saniye boyunca hiç duraksamadan (saniyede milyonlarca kez) `next()` ile
# üreteçleri sorgular ve `time.perf_counter()` üzerinden sürenin dolup dolmadığını
# kontrol eder. Bu sırada işlemci (CPU) çekirdeği %100 yük altında boş yere
# döngü çevirir.
# `time.sleep(saniye)` kullanıldığında ise işletim sistemi ilgili iş parçacığını
# (thread) uyku durumuna (suspended/blocked) alır; süre dolana kadar CPU hiç
# meşgul edilmez ve enerji/kaynak tüketimi sıfıra yakın olur.

def zamanlayici(aralik: float) -> Iterator[bool]:
    """Belirtilen zaman aralığı her dolduğunda True, aksi halde False üreten üreteç.

    Args:
        aralik (float): Tetiklenme aralığı (saniye).

    Yields:
        bool: Aralık dolduysa True, henüz dolmadıysa False.
    """
    if aralik <= 0:
        raise ValueError("Zamanlayıcı aralığı pozitif olmalıdır.")

    son_zaman = time.perf_counter()
    while True:
        simdi = time.perf_counter()
        if simdi - son_zaman >= aralik:
            son_zaman += aralik
            yield True
        else:
            yield False


def tik_tak_calistir(
    toplam_sure: float = 10.0,
    tik_aralik: float = 2.0,
    tak_aralik: float = 5.0,
) -> list[str]:
    """zamanlayici(aralik) üretecini kullanarak belirli süre boyunca tik/tak yazar.

    Varsayılan olarak 10 saniye boyunca her 2 saniyede "tik", her 5 saniyede "tak"
    yazdırır ve üretilen mesajların listesini döndürür.

    Args:
        toplam_sure (float): Programın toplam çalışma süresi (saniye). Varsayılan 10.0.
        tik_aralik (float): "tik" yazdırma aralığı (saniye). Varsayılan 2.0.
        tak_aralik (float): "tak" yazdırma aralığı (saniye). Varsayılan 5.0.

    Returns:
        list[str]: Sırasıyla ekrana yazdırılan "tik" ve "tak" mesajları.
    """
    tik = zamanlayici(tik_aralik)
    tak = zamanlayici(tak_aralik)
    baslangic = time.perf_counter()
    cikti: list[str] = []

    # Bitiş anındaki sınır tetiklemelerini kaçırmamak için küçük bir tolerans (0.05 sn)
    while time.perf_counter() - baslangic <= toplam_sure + 0.05:
        if next(tik):
            print("tik")
            cikti.append("tik")
        if next(tak):
            print("tak")
            cikti.append("tak")

    return cikti