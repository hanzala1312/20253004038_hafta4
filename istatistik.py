"""Görev 5 – map, filter, reduce, liste üreteci/sum ve functools.partial uygulamaları."""
from __future__ import annotations

from functools import partial, reduce
from typing import Any

from uzay_oyunu.oyun import yolculuk

# ============================================================================
# Okunabilirlik Değerlendirmesi (Görev 5 Yorumu):
# Python'da liste üreteçleri (`[g.upper() for g in ...]` ve `[g for g in ... if ...]`)
# ile `sum(...)` kullanımı, `map`/`filter`/`reduce` + `lambda` bileşimine kıyasla
# çok daha okunaklıdır. Çünkü liste üreteçleri hem dönüştürme hem de filtreleme
# mantığını tek bir düz ifadede, `lambda` sözdizimi gürültüsü olmadan doğal dil
# akışına yakın biçimde ifade eder; `sum()` ise `reduce(lambda a, b: ..., 0)`
# kalıbına göre amacı ilk bakışta belli eder.
# ============================================================================


# 1. Gezegen adlarının büyük harfli listesi
# Not: Türkçe 'i' harfinin standart örnek çıktıdaki ('SIRIUS', 'ORION', 'CENTAURI',
# 'KARA_DELIK', 'DÜNYA') ile birebir örtüşmesi için str.upper() kullanılmıştır.

def buyuk_harfli_gezegenler_map(galaksi: dict[str, Any]) -> list[str]:
    """map kullanarak gezegen adlarının büyük harfli listesini döndürür.

    Args:
        galaksi (dict[str, Any]): Galaksi veri sözlüğü.

    Returns:
        list[str]: Büyük harfli gezegen adları listesi.
    """
    return list(map(str.upper, galaksi["gezegenler"]))


def buyuk_harfli_gezegenler_liste_ureteci(galaksi: dict[str, Any]) -> list[str]:
    """Liste üreteci (list comprehension) ile gezegen adlarının büyük harfli listesini döndürür.

    Args:
        galaksi (dict[str, Any]): Galaksi veri sözlüğü.

    Returns:
        list[str]: Büyük harfli gezegen adları listesi.
    """
    return [gezegen.upper() for gezegen in galaksi["gezegenler"]]


# 2. En az iki bağlantısı olan gezegenler

def en_az_iki_baglantili_filter(galaksi: dict[str, Any]) -> list[str]:
    """filter kullanarak en az iki bağlantısı olan gezegenlerin listesini döndürür.

    Args:
        galaksi (dict[str, Any]): Galaksi veri sözlüğü.

    Returns:
        list[str]: En az 2 komşusu bulunan gezegenler.
    """
    baglantilar: dict[str, list[str]] = galaksi["baglantilar"]
    return list(
        filter(
            lambda gezegen: len(baglantilar.get(gezegen, [])) >= 2,
            galaksi["gezegenler"],
        )
    )


def en_az_iki_baglantili_liste_ureteci(galaksi: dict[str, Any]) -> list[str]:
    """Liste üreteci kullanarak en az iki bağlantısı olan gezegenlerin listesini döndürür.

    Args:
        galaksi (dict[str, Any]): Galaksi veri sözlüğü.

    Returns:
        list[str]: En az 2 komşusu bulunan gezegenler.
    """
    baglantilar: dict[str, list[str]] = galaksi["baglantilar"]
    return [
        gezegen
        for gezegen in galaksi["gezegenler"]
        if len(baglantilar.get(gezegen, [])) >= 2
    ]


# 3. Toplam bağlantı sayısı

def toplam_baglanti_reduce(galaksi: dict[str, Any]) -> int:
    """functools.reduce kullanarak galaksideki toplam bağlantı sayısını hesaplar.

    Args:
        galaksi (dict[str, Any]): Galaksi veri sözlüğü.

    Returns:
        int: Tüm gezegenlerin bağlantı sayılarının toplamı.
    """
    baglantilar: dict[str, list[str]] = galaksi["baglantilar"]
    return reduce(
        lambda toplam, komsular: toplam + len(komsular),
        baglantilar.values(),
        0,
    )


def toplam_baglanti_sum(galaksi: dict[str, Any]) -> int:
    """sum ve üreteç ifadesi kullanarak galaksideki toplam bağlantı sayısını hesaplar.

    Args:
        galaksi (dict[str, Any]): Galaksi veri sözlüğü.

    Returns:
        int: Tüm gezegenlerin bağlantı sayılarının toplamı.
    """
    baglantilar: dict[str, list[str]] = galaksi["baglantilar"]
    return sum(len(komsular) for komsular in baglantilar.values())


# 4. functools.partial ile hiz=3 sabitlenmiş hizli_yolculuk fonksiyonu
hizli_yolculuk = partial(yolculuk, hiz=3)