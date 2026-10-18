"""Değiştirilebilir varsayılan argüman (mutable default argument) tuzağı testi."""
from typing import Optional


# Hatalı hali (Önce bunu çalıştırıp pytest'te hata aldığını gör, sonra yoruma al):
# def yakit_ekle(miktar: int, depo: list[int] = []) -> list[int]:
#     depo.append(miktar)
#     return depo


def yakit_ekle(miktar: int, depo: Optional[list[int]] = None) -> list[int]:
    """Depoya yakıt ekler. Depo verilmezse her çağrıda yeni bir liste oluşturur.

    Args:
        miktar (int): Eklenecek yakıt miktarı.
        depo (Optional[list[int]], optional): Mevcut yakıt deposu listesi. Varsayılan None.

    Returns:
        list[int]: Güncellenmiş yakıt deposu listesi.
    """
    if depo is None:
        depo = []
    depo.append(miktar)
    return depo


def test_yakit_ekle_bagimsiz_depolar():
    """Fonksiyon argümansız her çağrıldığında birbirinden bağımsız yeni liste döndürmelidir."""
    birinci_cagri = yakit_ekle(10)
    ikinci_cagri = yakit_ekle(20)

    # Eğer None kalıbı kullanılmazsa ikinci_cagri [10, 20] olur ve bu test patlar!
    assert birinci_cagri == [10]
    assert ikinci_cagri == [20]
    assert birinci_cagri is not ikinci_cagri
