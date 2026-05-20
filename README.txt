# 🏥 Hastane Randevu Sistemi

Python'un standart GUI kütüphanesi olan **Tkinter** kullanılarak geliştirilmiş, basit ve kullanıcı dostu bir masaüstü hastane randevu yönetimi uygulamasıdır. Veri saklama işlemleri için yerel **JSON** dosyaları kullanılarak hafif, hızlı ve bağımsız bir veri yapısı sunulmuştur.

---

## 🚀 Projenin Amacı

Bu uygulamanın temel amacı; hastaların kolayca sisteme kaydolup istedikleri bölüm ve doktordan randevu alabilmelerini, mevcut randevularını görüntüleyip iptal edebilmelerini sağlamaktır. Aynı zamanda doktorların da kendi panellerinden üzerlerine atanmış randevuları detaylı bir şekilde takip etmelerine olanak tanır.

---

## ✨ Temel Özellikler

Uygulama, kullanıcı rollerine göre ayrılmış zengin bir özellik seti sunar:

### 🧑‍🤝‍🧑 Hasta Modülü
* **Kullanıcı Kaydı:** Yeni hastalar ad, soyad, e-posta ve şifre bilgileriyle sisteme hızlıca kayıt olabilirler.
* **Güvenli Giriş:** Kayıtlı hastalar e-posta ve şifreleriyle profillerine erişebilirler.
* **Dinamik Randevu Alma:**
    * Bölüm (Kardiyoloji, KBB, vb.) seçimi yapabilme.
    * Seçilen bölüme göre sistemde kayıtlı doktorların otomatik olarak listelenmesi.
    * İstenilen tarih ve saat formatına göre randevu oluşturabilme.
* **Randevu Yönetimi:**
    * **Gelecek ve Geçmiş Randevular:** Tüm randevuları iki ayrı listede düzenli olarak görüntüleme.
    * **Randevu İptali:** Henüz tarihi gelmemiş aktif randevuları kolayca iptal edebilme.

### 🩺 Doktor Modülü
* **Doktor Girişi:** Doktorlar, sisteme kayıtlı ad-soyad ve şifre bilgileriyle kendi yönetim panellerine erişebilirler.
* **Randevu Listeleme:** Kendilerine atanmış tüm randevuları (geçmiş ve gelecek) hasta bilgileriyle birlikte tek ekranda görüntüleme.
* **Durum Takibi:** Randevuların sistem tarafından tarihine göre "Gelecek" veya "Geçmiş" olarak otomatik etiketlenmesi.

---

## 🛠️ Kullanılan Teknolojiler

| Kategori | Teknoloji / Kütüphane |
| :--- | :--- |
| **Programlama Dili** | Python 3 |
| **Arayüz (GUI)** | Tkinter (Daha modern bir görünüm için `ttk` modülü ile) |
| **Veri Saklama** | JSON |
| **Standart Kütüphaneler** | `os`, `datetime`, `re`, `json` |

---

## ⚙️ Kurulum ve Çalıştırma

Uygulama ilk kez çalıştırıldığında veritabanı altyapısını otomatik olarak hazırlar. Verilerin saklanacağı `hastane_verileri` adında bir klasör ve içinde varsayılan doktor bilgilerini barındıran `doktorlar.json` dosyası sistem tarafından oluşturulur.

Projeyi yerel makinenizde çalıştırmak için terminalinizde şu komutu girmeniz yeterlidir:

```bash
python Hastane_Randevu_Sistemi.py