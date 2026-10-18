"""Hafta 4 Lab Ödevi (Görev 1, 2, 3, 4, 5 ve Bonus) birim testleri."""
from __future__ import annotations

from collections.abc import Iterator
from itertools import islice, takewhile
from pathlib import Path

import pytest

from uzay_oyunu.akis import (
    ayristir,
    fibonacci,
    fibonacci_esikten_kucuk,
    fibonacci_ilk_n,
    fibonacci_ilk_uc,
    onbelleksiz_rota_sayaci,
    rota_sayaci,
    satirlari_oku,
    tik_tak_calistir,
    uzun_yolculuklar,
    yakit_gostergesi,
    zamanlayici,
)
from uzay_oyunu.istatistik import (
    buyuk_harfli_gezegenler_liste_ureteci,
    buyuk_harfli_gezegenler_map,
    en_az_iki_baglantili_filter,
    en_az_iki_baglantili_liste_ureteci,
    hizli_yolculuk,
    toplam_baglanti_reduce,
    toplam_baglanti_sum,
)
from uzay_oyunu.oyun import galaksi_kur, travel, varsayilan_galaksiyi_yukle, yolculuk


# ============================================================================
# Görev 1 Testleri – Fibonacci üreteci
# ============================================================================

def test_fibonacci_uc_farkli_yolla() -> None:
    """Fibonacci değerleri next(), islice ve takewhile ile doğru alınabilmeli."""
    # 1. yol: next() ile ilk üç değer
    g = fibonacci()
    assert (next(g), next(g), next(g)) == (0, 1, 1)
    assert fibonacci_ilk_uc() == (0, 1, 1)

    # 2. yol: itertools.islice ile ilk 12 değer
    beklenen_12 = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    assert list(islice(fibonacci(), 12)) == beklenen_12
    assert fibonacci_ilk_n(12) == beklenen_12

    # 3. yol: itertools.takewhile ile 100'den küçük değerler
    assert list(takewhile(lambda x: x < 100, fibonacci())) == beklenen_12
    assert fibonacci_esikten_kucuk(100) == beklenen_12


def test_fibonacci_tek_kullanimlik_uretec() -> None:
    """Aynı üreteçten ikinci list(islice(...)) çağrısı farklı sonuç vermelidir."""
    uret = fibonacci()
    ilk_dilim = list(islice(uret, 5))
    ikinci_dilim = list(islice(uret, 5))

    assert ilk_dilim == [0, 1, 1, 2, 3]
    assert ikinci_dilim == [5, 8, 13, 21, 34]
    assert ilk_dilim != ikinci_dilim


# ============================================================================
# Görev 2 Testleri – Yakıt göstergesi ve StopIteration / travel()
# ============================================================================

def test_yakit_gostergesi_ornek_cikti_ve_stopiteration() -> None:
    """yakit_gostergesi(100, 30) [70, 40, 10, 0] üretmeli ve ardından StopIteration fırlatmalı."""
    gosterge = yakit_gostergesi(100, 30)
    assert isinstance(gosterge, Iterator)
    assert list(gosterge) == [70, 40, 10, 0]

    # Üreteç tükendikten sonra next() çağrısı StopIteration fırlatmalı
    with pytest.raises(StopIteration):
        next(gosterge)


def test_travel_yakit_bitince_kaybeder() -> None:
    """travel() içinde yakıt bittiğinde StopIteration yakalanıp kayıp mesajı dönmeli."""
    galaksi = galaksi_kur(
        gezegenler=["dünya", "sirius"],
        baglantilar={"dünya": ["sirius"], "sirius": ["dünya"]},
        baslangic="dünya",
        yakit=10,
    )
    # Tüketim 5 iken: 1. yolculukta 5 kalır, 2. yolculukta 0 kalır,
    # 3. yolculukta StopIteration yakalanır ve oyuncu kaybeder.
    sonuc = travel(galaksi, adimlar=["sirius", "dünya", "sirius"], tuketim=5)
    assert sonuc == "Yakıtın bitti, uzayda sürükleniyorsun…"


def test_travel_yeterli_yakit_ile_basarili() -> None:
    """Küçük tüketimle (ör. yakıt 100, tüketim 5) normal yolculuklar sorunsuz tamamlanmalı."""
    galaksi = varsayilan_galaksiyi_yukle()
    sonuc = travel(galaksi, adimlar=["sirius", "orion"], tuketim=5)
    assert galaksi["konum"] == "orion"
    assert galaksi["yakit"] == 90
    assert "Kalan yakıt: 90" in sonuc


# ============================================================================
# Görev 3 Testleri – Seyir defteri boru hattı (tembellik ve doğruluk)
# ============================================================================

def test_seyir_defteri_boru_hatti(tmp_path: Path) -> None:
    """Üç üreteçli boru hattı dosyayı listeye okumadan doğru sonuçları üretmeli."""
    seyir_dosyasi = Path(__file__).parent.parent / "veri" / "seyir.txt"
    assert seyir_dosyasi.exists()

    # Her aşamanın liste değil tembel üreteç (Iterator) döndürdüğünü doğrula
    satir_akisi = satirlari_oku(seyir_dosyasi)
    assert isinstance(satir_akisi, Iterator)

    kayit_akisi = ayristir(satir_akisi)
    assert isinstance(kayit_akisi, Iterator)

    uzun_akis = uzun_yolculuklar(kayit_akisi, 10)
    assert isinstance(uzun_akis, Iterator)
    assert [h for _, h, _ in uzun_akis] == ["sirius", "centauri", "orion", "kara_delik"]

    # Toplam yakıt kontrolü (88)
    toplam_yakit = sum(y for _, _, y in ayristir(satirlari_oku(seyir_dosyasi)))
    assert toplam_yakit == 88


# ============================================================================
# Görev 4 Testleri – Önbellekli rota sayacı (@lru_cache)
# ============================================================================

def test_rota_sayaci_ve_onbellek() -> None:
    """rota_sayaci örnek çıktıları (9, 2185, 16832258606399) vermeli ve lru_cache kullanmalı."""
    galaksi = varsayilan_galaksiyi_yukle()
    say = rota_sayaci(galaksi["baglantilar"])

    sonuclar = (say("dünya", 3), say("dünya", 10), say("dünya", 40))
    assert sonuclar == (9, 2185, 16832258606399)

    # Önbelleğin gerçekten aktif olduğunu ve hit ürettiğini doğrula
    bilgi = say.cache_info()
    assert bilgi.hits > 0
    assert bilgi.currsize > 0

    # Önbelleksiz sürümle küçük adımda birebir aynı sonucu verdiğini doğrula
    say_onbelleksiz = onbelleksiz_rota_sayaci(galaksi["baglantilar"])
    assert say_onbelleksiz("dünya", 6) == say("dünya", 6)


# ============================================================================
# Görev 5 Testleri – map, filter, reduce, liste üreteci, sum ve partial
# ============================================================================

def test_istatistik_iki_yolla_ayni_sonuclar() -> None:
    """map/filter/reduce ve liste üreteci/sum fonksiyonları örnek çıktıları üretmeli."""
    galaksi = varsayilan_galaksiyi_yukle()

    beklenen_buyuk = ["DÜNYA", "CENTAURI", "SIRIUS", "ORION", "KARA_DELIK"]
    assert buyuk_harfli_gezegenler_map(galaksi) == beklenen_buyuk
    assert buyuk_harfli_gezegenler_liste_ureteci(galaksi) == beklenen_buyuk

    beklenen_iki_baglantili = ["dünya", "centauri", "sirius", "orion"]
    assert en_az_iki_baglantili_filter(galaksi) == beklenen_iki_baglantili
    assert en_az_iki_baglantili_liste_ureteci(galaksi) == beklenen_iki_baglantili

    assert toplam_baglanti_reduce(galaksi) == 10
    assert toplam_baglanti_sum(galaksi) == 10


def test_hizli_yolculuk_partial() -> None:
    """functools.partial ile türetilen hizli_yolculuk hiz=3 sabit değerini kullanmalı."""
    assert hizli_yolculuk. keywords == {"hiz": 3}
    assert hizli_yolculuk("dünya", "sirius") == yolculuk("dünya", "sirius", hiz=3)
    assert hizli_yolculuk("dünya", "sirius") == "dünya -> sirius (hız=3)"


# ============================================================================
# Bonus Testi – zamanlayici(aralik) üreteci
# ============================================================================

def test_zamanlayici_ve_tik_tak() -> None:
    """zamanlayici üreteci belirlenen aralıklarda True üretmeli."""
    z = zamanlayici(0.02)
    assert isinstance(z, Iterator)
    # İlk çağrı hemen yapıldığı için False olmalı
    assert next(z) is False

    # Hızlı test için ölçeklenmiş süre (0.10 sn boyunca her 0.02 sn'de tik, 0.05 sn'de tak)
    olaylar = tik_tak_calistir(toplam_sure=0.10, tik_aralik=0.02, tak_aralik=0.05)
    assert "tik" in olaylar
    assert "tak" in olaylar