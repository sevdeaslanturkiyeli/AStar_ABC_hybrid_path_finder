# 🚁 Hibrit ABC-A* Yol Planlama Sistemi 

## Proje Hakkında

Bu proje, ızgara tabanlı haritalar üzerinde çalışan ve **Artificial Bee Colony** (ABC) optimizasyon algoritması ile **A-Star** (A*) yol bulma algoritmasını birleştiren hibrit bir yol planlama sistemidir.

Sistem, harici bir metin dosyasından okunan haritalar üzerinde engellerden kaçınarak başlangıç ve hedef noktaları arasında optimum rotayı oluşturmaktadır. Klasik A* algoritmasına ek olarak, ABC algoritması kullanılarak riskli bölgeler belirlenmekte ve bu bölgelere ceza maliyetleri uygulanarak daha güvenli ve daha verimli rotalar elde edilmektedir.

Bu çalışma özellikle;

-İnsansız Hava Araçları (İHA)

-Otonom Kara Araçları

-Robotik Navigasyon Sistemleri

-Karar Destek Sistemleri

-Arama Kurtarma Operasyonları

gibi uygulamalar için geliştirilmiştir.

## Projenin Amacı

Klasik A* algoritmaları genellikle en kısa yolu bulmaya odaklanır. Ancak gerçek dünya uygulamalarında:

 Riskli bölgelerden uzak durulması,

 Gereksiz manevraların azaltılması,
 
 Daha güvenli rotaların oluşturulması

gibi kriterler de önemlidir.

Bu projede ABC algoritması ile belirlenen ceza bölgeleri kullanılarak A* algoritmasının yalnızca en kısa değil, aynı zamanda daha güvenli ve daha düşük maliyetli rotalar üretmesi hedeflenmiştir.

## Kullanılan Algoritmalar
### 1. Artificial Bee Colony (ABC)

Artificial Bee Colony algoritması, bal arılarının besin kaynağı arama davranışlarından esinlenen sezgisel bir optimizasyon algoritmasıdır.

Sistemde:

-İşçi Arılar (Employed Bees)

-Gözlemci Arılar (Onlooker Bees)

-Kaşif Arılar (Scout Bees)

kullanılarak harita üzerinde ceza uygulanacak bölgeler optimize edilir.


ABC algoritmasının amacı:

-Yol maliyetini azaltmak

-Gereksiz dönüşleri azaltmak

-Riskli bölgelerden kaçınmak

-Daha uygun rotalar oluşturmak

olarak belirlenmiştir.

### 2. A* (A-Star) Algoritması

A* algoritması başlangıç ve hedef noktaları arasında en uygun yolu bulmak için kullanılmaktadır.

Her düğüm aşağıdaki maliyet bilgilerini içerir:

 **g(n):** Başlangıçtan mevcut düğüme kadar olan gerçek maliyet

 **h(n):** Hedefe olan tahmini maliyet
 
 **f(n):** Toplam maliyet

Toplam maliyet:

**f(n) = g(n) + h(n)**

olarak hesaplanmaktadır.

Bu projede sezgisel fonksiyon olarak **Manhattan Mesafesi** kullanılmaktadır.

## Yol Maliyet Hesabı

Yol maliyeti aşağıdaki kriterler dikkate alınarak hesaplanmaktadır:

**Yol Uzunluğu**

Toplam gidilen düğüm sayısı.

**Ceza Bölgeleri**

ABC algoritması tarafından belirlenen bölgelerden geçildiğinde ek maliyet uygulanır.

Örneğin:

 Normal hücre maliyeti = 1
 
 Cezalı hücre maliyeti = 5

Bu sayede algoritma mümkün olduğunca riskli bölgelerden kaçınmaya çalışır.

**Dönüş Cezası**

Yol üzerindeki yön değişimleri ayrıca cezalandırılır.

Böylece:

Daha düzgün
Daha akıcı
İHA hareketlerine daha uygun

rotalar elde edilir.

## Harita Yapısı

Haritalar harici bir metin dosyasından okunmaktadır.

Örnek:

<img width="101" height="138" alt="image" src="https://github.com/user-attachments/assets/e5b98ce0-de9a-46a3-b7fb-8e91bc3833c3" />

Değerlerin anlamları:

**Değer	Açıklama**

 **0**	Geçilebilir Alan
 
 **1**	Engel

 **2**	Yasak veya Özel Bölge

## Algoritmanın Çalışma Mantığı
### 1. Haritanın Yüklenmesi

Harita dosyası okunur ve matris yapısına dönüştürülür.

### 2. Düğüm Oluşturulması

Her hücre için:

 -Konum bilgisi
 
 -Maliyet değerleri
 
 -Ebeveyn düğüm

oluşturulur.

### 3. ABC Optimizasyonu

ABC algoritması ceza uygulanacak bölgeleri belirler.

### 4. A* Yol Planlama

Belirlenen ceza bölgeleri dikkate alınarak en uygun rota oluşturulur.

### 5. Yol Görselleştirme

Bulunan yol matplotlib kullanılarak harita üzerinde çizdirilir.

```text
📂 Proje Yapısı
├── hybrid_pathfinder.py
├── hybrid.txt
├── aStar.py
├── aStar.txt
└── README.md
```

### Kurulum

Gerekli kütüphaneleri yükleyin:

```bash
pip install numpy matplotlib
```

### 💻 Kullanım

Başlangıç ve hedef koordinatlarını belirleyin:

 start = (2, 35)
 
 goal = (4, 45)

Algoritmayı çalıştırın:

**pathfinder =** HybridPathFinder(
    txt_file_path,
    start,
    goal
)

**optimal_path =** pathfinder.find_optimal_path()
### 📈 Çıktılar

Program çalıştırıldığında:

 * En uygun rota hesaplanır.
 
 * Yol koordinatları oluşturulur.
 
 * Yol harita üzerinde çizilir.
 
 Sonuç **map_visual.png** dosyasına kaydedilir.

<img width="639" height="541" alt="mapvisual" src="https://github.com/user-attachments/assets/5f83f6e4-e498-4e60-b20a-5c798a8a26bf" />


Görselleştirmede:

🟢 Yeşil Nokta → Başlangıç

🔴 Kırmızı Nokta → Hedef

🔵 Mavi Çizgi → Hesaplanan Yol
