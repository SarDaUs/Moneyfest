# Moneyfest
#  Deadlock Simulator & Banker's Algorithm 

İşletim Sistemleri dersi kapsamında geliştirilmiş; **Banker Algoritması (Banker's Algorithm)**, **Deadlock Tespiti ve Çözümü (Deadlock Detection & Resolution)** ve **Kaynak Tahsis Çizgesi (Resource Allocation Graph - RAG)** konularını teorik ders notlarından çıkarıp; canlı, görsel ve interaktif bir masaüstü simülasyonuna dönüştürmek amacıyla geliştirilmiştir.

##  İçerik

Görselleştirme: Süreç (P) ve Kaynak (R) bağımlılıklarını Resource Allocation Graph (RAG) üzerinden dinamik ve renkli bir ağ grafiği olarak çizdirip kilitlenmenin nerede oluştuğunu anında tespit etmek. 

Güvenlik Analizi: Sisteme gelen kaynak isteklerinin güvenli bir çalışma sırasında (Safe Sequence) kalıp kalmadığını Banker's Algoritması ile adım adım simüle etmek.

Akıllı Kurtarma Stratejileri: Kilitlenme durumunda gerçek işletim sistemlerinin kullandığı kurban seçimi (Victim Selection: En çok kaynak tüketen, en düşük öncelikli veya en az maliyetli süreci kapatma) ve kaynak geri alma (Resource Preemption) karar mekanizmalarını deneysel olarak test etmek.

##  Kurulum ve Çalıştırma

Projenin bilgisayarınızda çalışabilmesi için **Python 3.8** veya üzeri bir sürümün yüklü olması gerekmektedir.
Terminal kısmından python main.py komutunu çalıştırınca dosyamız açılmaktadır.

git clone [https://github.com/SarDaus/Moneyfest.git](https://github.com/SarDaUs/Moneyfest.git)
cd Moneyfest ya da dosyayı zip olarak indirin.

Ternminalde 
pip install networkx matplotlib
çalıştırın.

İndirmeler tamamlandıktan sonra programı çalıştırmak için terminalde 
py main.py
kodunu çalıştırın.

## Dosya indirme

Yeşil code butonuna basıp dosyayı bilgisayarınıza zip olarak indirin.
