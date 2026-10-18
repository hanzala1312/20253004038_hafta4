Kapsam (Scope) ve LEGB Kuralı İncelemesi
Ad: Halil Efe
Soyad: Erdoğan
Numara: 20253004038
Bölüm: Bilişim Sistemleri ve Teknolojileri
GitHub Deposu: 
Python'da değişken isimleri LEGB (Local -> Enclosing -> Global -> Built-in) sırasıyla aranır. Dersteki üç kapsam örneğinin incelenmesi aşağıdadır:


Örnek 1: Global Değişkeni Okuma (Shadowing Yok)
yakit = 100

def durumu_goster():

    print(yakit)

durumu_goster()

Tahminim: 100
Gerçek Sonuç: 100
Nedeni: durumu_goster() fonksiyonunun kendi yerel (Local) kapsamında yakit adlı bir değişken tanımlanmamıştır. Python LEGB kuralına göre bir üst kapsama (Global) bakar, yakit = 100 değerini bulur ve ekrana yazdırır.


Örnek 2: Yerel Değişken Ataması (Gölgeleme / Shadowing)
yakit = 100

def yakit_azalt():

    yakit = 80

    print("Fonksiyon içi:", yakit)

yakit_azalt()

print("Fonksiyon dışı:", yakit)

Tahminim: Fonksiyon içi 80, Fonksiyon dışı 100
Gerçek Sonuç: Fonksiyon içi: 80 Fonksiyon dışı: 100
Nedeni: Fonksiyon içinde yakit = 80 ataması yapıldığında Python, yerel (Local) kapsamda yeni bir yakit değişkeni oluşturur. Bu yerel değişken, fonksiyon çalışırken globaldeki yakit değişkenini gölgeler (shadowing). Globaldeki yakit değişkeni bu atamadan etkilenmez ve 100 olarak kalır.


Örnek 3: UnboundLocalError Hatası ve Açıklaması
yakit = 100

def yakit_harcama():

    print(yakit)

    yakit = yakit - 10

yakit_harcama()

Tahminim: Önce 100 yazar, sonra 90 yapar (veya hata verir).
Gerçek Sonuç: UnboundLocalError: cannot access local variable 'yakit' where it is not associated with a value
Nedeni ve Açıklaması: Python derleme aşamasında fonksiyon gövdesinin tamamını tarar. İçeride yakit = ... şeklinde bir atama ifadesi gördüğü anda, yakit değişkenini o fonksiyonun yerel (Local) değişkeni olarak işaretler ve global kapsamla bağlantısını keser. Ancak fonksiyon çalıştığında, henüz yakit değişkenine yerel bir değer atanmadan önce (print(yakit) veya sağ taraftaki yakit - 10 okumasında) değişkene erişilmeye çalışılır. Yerel değişken henüz bir değere bağlanmadığı için Python UnboundLocalError fırlatır.
Çözümü: Global değişken kullanmak yerine değer fonksiyona parametre olarak verilmeli ve yeni değer return edilmelidir (veya iç içe fonksiyonlarda nonlocal kullanılmalıdır).
