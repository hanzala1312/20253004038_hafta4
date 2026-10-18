"""Görev kayıtlarını esnek parametrelerle oluşturan modül."""
from typing import Any


def gorev_kaydi(
    baslik: str,
    *adimlar: str,
    oncelik: str = "normal",
    **ekler: Any
) -> str:
    """Verilen başlık, adımlar, öncelik ve ek bilgilerle görev kaydı metni üretir.

    Args:
        baslik (str): Görevin başlığı.
        *adimlar (str): Görev adımları (değişken sayıda konumsal argüman).
        oncelik (str, optional): Görev önceliği (yalnızca adıyla verilebilir). Varsayılan "normal".
        **ekler (Any): Ek anahtar-değer bilgileri.

    Returns:
        str: Biçimlendirilmiş görev kaydı metni.
    """
    satirlar: list[str] = [f"[{oncelik.upper()}] {baslik}"]

    for sira, adim in enumerate(adimlar, start=1):
        satirlar.append(f"{sira}. {adim}")

    for anahtar, deger in ekler.items():
        satirlar.append(f"{anahtar}: {deger}")

    return "\n".join(satirlar)


if __name__ == "__main__":
    # 1. Doğrudan argümanlarla çağrı biçimi
    print("--- 1. Çağrı Biçimi (Doğrudan) ---")
    kayit1 = gorev_kaydi(
        "Kara deliğe atla",
        "Kredi kazan",
        "Pilot bul",
        "Hiperdrive al",
        oncelik="yüksek",
        sorumlu="Ayşe"
    )
    print(kayit1)

    print("\n--- 2. Çağrı Biçimi (* ve ** ile açarak) ---")
    # 2. Listeyi (*) ve sözlüğü (**) açarak çağrı biçimi
    adim_listesi = ["Kredi kazan", "Pilot bul", "Hiperdrive al"]
    ek_bilgiler = {"oncelik": "yüksek", "sorumlu": "Ayşe"}
    kayit2 = gorev_kaydi("Kara deliğe atla", *adim_listesi, **ek_bilgiler)
    print(kayit2)
