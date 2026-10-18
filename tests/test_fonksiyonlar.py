"""Görev 1, 2, 3 ve 5 için birim testleri."""
import pytest
from uzay_oyunu.oyun import envanter_metni, hedef_menusu, galaksi_kur
from uzay_oyunu.araclar import hamle_sayaci, en_bagli_gezegenler


def test_envanter_metni_dolu():
    """Eşyalar varken doğru metni döndürmeli."""
    assert envanter_metni(True, False, True) == "Sende: bol kredi, yetenekli bir pilot"
    assert envanter_metni(True, True, True) == "Sende: bol kredi, hiperdrive, yetenekli bir pilot"


def test_envanter_metni_bos():
    """Hiç eşya yokken boş metin döndürmeli."""
    assert envanter_metni(False, False, False) == ""


def test_hedef_menusu():
    """Hedef listesini numaralı menü metnine çevirmeli."""
    beklenen = "Nereye gitmek istersin?\n[1] centauri\n[2] sirius"
    assert hedef_menusu(["centauri", "sirius"]) == beklenen


def test_galaksi_kur_varsayilan_ve_ozel():
    """Galaksi kurulumu varsayılan yakıtı ve özel yakıtı doğru ayarlamalı."""
    g = galaksi_kur(["mars"], {"mars": []}, "mars")
    assert g["konum"] == "mars"
    assert g["yakit"] == 50

    g2 = galaksi_kur(["dünya"], {"dünya": []}, "dünya", yakit=100)
    assert (g2["konum"], g2["yakit"]) == ("dünya", 100)


def test_galaksi_kur_hatali_baslangic():
    """Başlangıç gezegeni listede yoksa ValueError fırlatmalı."""
    with pytest.raises(ValueError):
        galaksi_kur(["mars"], {"mars": []}, "plüton")


def test_hamle_sayaci():
    """Closure tabanlı sayaç her çağrıda 1 artmalı."""
    sayac = hamle_sayaci()
    assert sayac() == 1
    assert sayac() == 2
    assert sayac() == 3


def test_en_bagli_gezegenler():
    """Gezegenler bağlantı sayısına göre azalan, eşitlikte alfabetik sıralanmalı."""
    ornek_galaksi = {
        "gezegenler": ["dünya", "centauri", "sirius", "orion", "kara_delik"],
        "baglantilar": {
            "sirius": ["centauri", "dünya", "orion", "kara_delik"],
            "centauri": ["dünya", "sirius", "orion"],
            "dünya": ["centauri", "sirius"],
            "orion": ["centauri", "sirius"],
            "kara_delik": ["sirius"]
        }
    }
    assert en_bagli_gezegenler(ornek_galaksi) == [
        "sirius", "centauri", "dünya", "orion", "kara_delik"
    ]
