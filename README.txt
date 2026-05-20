Hastane Randevu Sistemi
Python/Tkinter tabanlı basit hastane randevu otomasyonu. Hasta kaydı, randevu alma/iptal etme ve doktor paneli özelliklerini içerir. Veri saklama için JSON kullanılmıştır.

Bu proje, Python'un standart GUI kütüphanesi olan Tkinter kullanılarak geliştirilmiş, basit ve kullanıcı dostu bir masaüstü hastane randevu yönetimi uygulamasıdır. Uygulama, hasta ve doktor olmak üzere iki farklı kullanıcı rolünü destekler ve tüm verileri yerel JSON dosyalarında saklayarak kalıcı bir veri yapısı sunar.

Projenin Amacı
Bu uygulamanın temel amacı, hastaların kolayca sisteme kaydolup istedikleri bölüm ve doktordan randevu alabilmelerini, mevcut randevularını görüntüleyip iptal edebilmelerini sağlamaktır. Aynı zamanda doktorların da kendi panellerinden üzerlerine atanmış randevuları takip etmelerine olanak tanır.

Özellikler
Uygulama, kullanıcı rollerine göre ayrılmış zengin bir özellik seti sunar:

Hasta Arayüzü
Kullanıcı Kaydı: Yeni hastalar ad, soyad, e-posta ve şifre bilgileriyle kolayca sisteme kayıt olabilirler.
Güvenli Giriş: Kayıtlı hastalar e-posta ve şifreleriyle sisteme giriş yapabilirler.
Dinamik Randevu Alma:
Bölüm (Kardiyoloji, KBB, vb.) seçimi yapabilirler.
Seçilen bölüme göre sistemde kayıtlı doktorlar otomatik olarak listelenir.
İstenilen tarih ve saat formatına göre randevu oluşturabilirler.
Randevu Yönetimi:
Gelecek ve Geçmiş Randevular: Tüm randevularını "Gelecek" ve "Geçmiş" olarak iki ayrı listede görüntüleyebilirler.
Randevu İptali: Henüz tarihi gelmemiş bir randevuyu kolayca iptal edebilirler.
Doktor Arayüzü
Doktor Girişi: Doktorlar, sisteme kayıtlı ad-soyad ve şifre bilgileriyle kendi panellerine erişebilirler.
Randevu Listeleme: Kendilerine atanmış tüm randevuları (hem geçmiş hem de gelecek) hasta bilgileriyle birlikte görüntüleyebilirler.
Durum Takibi: Randevular, tarihine göre "Gelecek" veya "Geçmiş" olarak otomatik etiketlenir.
Kullanılan Teknolojiler
Programlama Dili: Python 3
Arayüz (GUI): Tkinter (Daha modern bir görünüm için ttk modülü ile)
Veri Saklama: JSON (Hasta ve doktor verileri için)
Standart Kütüphaneler: os, datetime, re, json
Uygulama ilk kez çalıştırıldığında, verilerin saklanacağı hastane_verileri adında bir klasör ve içinde varsayılan doktor bilgilerini içeren doktorlar.json dosyası otomatik olarak oluşturulur.