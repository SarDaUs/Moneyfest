# Moneyfest
#  Deadlock Simulator & Banker's Algorithm 

İşletim Sistemleri dersi kapsamında geliştirilmiş; **Banker Algoritması (Banker's Algorithm)**, **Deadlock Tespiti ve Çözümü (Deadlock Detection & Resolution)** ve **Kaynak Tahsis Çizgesi (Resource Allocation Graph - RAG)** konularını teorik ders notlarından çıkarıp; canlı, görsel ve interaktif bir masaüstü simülasyonuna dönüştürmek amacıyla geliştirilmiştir.

## Proje İçeriği

Canlı Kaynak Tahsis Grafiği (RAG Visualizer): Süreçler ($P$) ile kaynaklar ($R$) arasındaki bağımlılıkları, kilitlenmeleri ve istekleri NetworkX & Matplotlib kullanarak dinamik bir ağ grafiği üzerinde anlık çizer.

Banker's Algoritması ile Güvenlik Analizi: Sisteme yeni kaynak istekleri geldiğinde sistemin Güvenli Durumda (Safe State) kalıp kalmadığını analiz eder ve güvenli çalışma dizisini (Safe Sequence) hesaplar.

Adım Adım Algoritma Simülasyonu (Step Engine): Banker's Algoritması'nın arka planda nasıl karar verdiğini, hangi sürecin kontrol edildiğini ve ne zaman kaynak serbest bıraktığını düğümleri renklendirerek (Sarı: Kontrol ediliyor, Yeşil: Başarılı, Kırmızı: Bekliyor) canlı gösterir.

Anlık Sistem Sağlık Göstergesi (Health Meter): Sistemdeki kilitlenme riskini anlık analiz ederek üst panelde HEALTHY (Yeşil), WARNING (Sarı) veya CRITICAL / DEADLOCK (Kırmızı) rozetleriyle bildirir.

Akıllı Kilitlenme Çözümü (Multi-Strategy Recovery): Deadlock oluştuğunda sistemi en az zararla kurtarmak için 4 farklı strateji sunar. Max Allocation (En çok kaynak tutan süreci sonlandırma)Lowest Priority (En düşük öncelikli süreci kapatma)Lowest Termination Cost (Sisteme en az maliyet çıkaracak süreci kurban etme)Resource Preemption (Süreci öldürmeden elindeki kaynakları zorla geri alma).

Dinamik Boyutlandırma ve Esnek Veri Girişi: Sabit bir senaryoya bağlı kalmadan kullanıcı tarafından istenilen sayıda Süreç ($P$) ve Kaynak ($R$) tanımlanmasına, matris verilerinin doğrudan arayüzden güncellenmesine olanak tanır.

Hazır Senaryo Kütüphanesi (Presets): Tek tıkla Deadlock, Safe State veya High Starvation senaryolarını yükleyerek hızlı demo/test yapma imkanı sağlar.

Raporlama ve Log Kaydetme Motoru: Tüm matris analizlerini, süreç önceliklerini ve güvenli diziyi .txt raporu olarak; arayüzdeki tüm işlem geçmişini ise .log dosyası olarak bilgisayara aktarır.

##  Kurulum ve Çalıştırma

Projenin bilgisayarınızda çalışabilmesi için **Python 3.8** veya üzeri bir sürümün yüklü olması gerekmektedir.
Terminal kısmından python main.py komutunu çalıştırınca dosyamız açılmaktadır.

git clone [https://github.com/SarDaus/Moneyfest.git](https://github.com/SarDaUs/Moneyfest.git)
cd Moneyfest ya da dosyayı zip olarak indirin.

Terminalde ;

pip install networkx matplotlib

çalıştırın.



İndirmeler tamamlandıktan sonra programı çalıştırmak için terminalde ;

py main.py

kodunu çalıştırın.

## Dosya indirme

Yeşil code butonuna basıp dosyayı bilgisayarınıza zip olarak indirin.
