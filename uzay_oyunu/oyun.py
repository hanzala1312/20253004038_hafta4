"""Uzay oyunu ana modülü - Hafta 3 fonksiyonları ve güncellenmiş travel yapısı."""
import json
from pathlib import Path
from typing import Any
from uzay_oyunu.araclar import hamle_sayaci


def envanter_metni(credits: bool, engines: bool, copilot: bool) -> str:
    """Oyuncunun sahip olduğu eşyaları metin olarak döndürür.

    Args:
        credits (bool): Kredi durumu.
        engines (bool): Motor/Hiperdrive durumu.
        copilot (bool): Yardımcı pilot durumu.

    Returns:
        str: Eşya varsa 'Sende: ...' metni, yoksa boş metin ('').
    """
    esyalar: list[str] = []
    if credits:
        esyalar.append("bol kredi")
    if engines:
        esyalar.append("hiperdrive")
    if copilot:
        esyalar.append("yetenekli bir pilot")

    if not esyalar:
        return ""
    return f"Sende: {', '.join(esyalar)}"


def hedef_menusu(hedefler: list[str]) -> str:
    """Verilen hedef gezegen listesini numaralı menü metnine dönüştürür.

    Args:
        hedefler (list[str]): Gidilebilecek gezegenlerin listesi.

    Returns:
        str: Numaralandırılmış hedef menüsü metni.
    """
    satirlar = ["Nereye gitmek istersin?"]
    for i, hedef in enumerate(hedefler, start=1):
        satirlar.append(f"[{i}] {hedef}")
    return "\n".join(satirlar)


def galaksi_kur(
    gezegenler: list[str],
    baglantilar: dict[str, list[str]],
    baslangic: str,
    **kwargs: Any
) -> dict[str, Any]:
    """Galaksi veri yapısını doğrular ve kurar.

    Args:
        gezegenler (list[str]): Galaksideki gezegenlerin listesi.
        baglantilar (dict[str, list[str]]): Gezegenler arası geçiş bağlantıları.
        baslangic (str): Oyunun başlayacağı gezegen.
        **kwargs (Any): 'yakit' gibi ek ayarlar (verilmezse yakit=50 olur).

    Raises:
        ValueError: Başlangıç gezegeni gezegenler listesinde yoksa fırlatılır.

    Returns:
        dict[str, Any]: Kurulan galaksi sözlüğü.
    """
    if baslangic not in gezegenler:
        raise ValueError(f"Başlangıç gezegeni '{baslangic}' gezegenler listesinde yok!")

    yakit: int = kwargs.get("yakit", 50)

    return {
        "gezegenler": gezegenler,
        "baglantilar": baglantilar,
        "baslangic": baslangic,
        "konum": baslangic,
        "yakit": yakit,
    }


def varsayilan_galaksiyi_yukle() -> dict[str, Any]:
    """galaksi.json dosyasını okur ve galaksi_kur(**veri) ile galaksiyi döndürür.

    Returns:
        dict[str, Any]: Kurulan varsayılan galaksi sözlüğü.
    """
    dosya_yolu = Path(__file__).parent / "galaksi.json"
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        veri = json.load(f)
    return galaksi_kur(**veri)
