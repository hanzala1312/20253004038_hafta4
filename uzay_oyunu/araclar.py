"""Closure tabanlı sayaç, lambda sıralama ve süre ölçüm araçları."""
import time
from typing import Any, Callable


def sure_olc(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Verilen fonksiyonun çalışma süresini ölçen ve ekrana yazan sarmalayıcı (decorator).

    Args:
        fonksiyon (Callable[..., Any]): Süresi ölçülecek fonksiyon.

    Returns:
        Callable[..., Any]: Sarmalanmış fonksiyon.
    """
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        baslangic = time.perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        bitis = time.perf_counter()
        gecen_sure = bitis - baslangic
        print(f"[{fonksiyon.__name__}] çalışma süresi: {gecen_sure:.6f} saniye")
        return sonuc

    return sarmalayici


def hamle_sayaci() -> Callable[[], int]:
    """Her çağrıldığında bir artan closure tabanlı bir sayaç fonksiyonu döndürür.

    Returns:
        Callable[[], int]: Çağrıldığında güncel hamle sayısını döndüren fonksiyon.
    """
    sayi = 0

    def sayac() -> int:
        nonlocal sayi
        sayi += 1
        return sayi

    return sayac


def en_bagli_gezegenler(galaksi: dict[str, Any]) -> list[str]:
    """Gezegenleri bağlantı sayısına göre azalan, eşitlikte alfabetik sırayla döndürür.

    Args:
        galaksi (dict[str, Any]): 'gezegenler' ve 'baglantilar' içeren galaksi sözlüğü.

    Returns:
        list[str]: Sıralanmış gezegen isimleri listesi.
    """
    gezegenler: list[str] = galaksi["gezegenler"]
    baglantilar: dict[str, list[str]] = galaksi["baglantilar"]

    return sorted(
        gezegenler,
        key=lambda g: (-len(baglantilar.get(g, [])), g)
    )


# Bonus görevi gereği fonksiyonu sure_olc ile sarmalıyoruz:
en_bagli_gezegenler = sure_olc(en_bagli_gezegenler)
