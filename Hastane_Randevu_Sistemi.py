
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re
import json
import os

VERI_DIZINI = "hastane_verileri"
HASTALAR_DOSYASI = os.path.join(VERI_DIZINI, "hastalar.json")
DOKTORLAR_DOSYASI = os.path.join(VERI_DIZINI, "doktorlar.json")

ANA_ARKA_PLAN = "#F0F0F0"
IKINCIL_ARKA_PLAN = "#E0E0E0"
BUTON_ARKA_PLAN = "#ADD8E6"
BUTON_YAZI_RENGI = "black"
VURGU_BUTON_ARKA_PLAN = "#4682B4"
VURGU_BUTON_YAZI_RENGI = "white"
METIN_RENGI = "#333333"
GIRIS_ALANI_ARKA_PLAN = "#FFFFFF"
LISTE_KUTUSU_ARKA_PLAN = "#FEFEFE"

BUTON_USTUNE_GELINCE_ARKA_PLAN = "#B0E0E6"
VURGU_BUTON_USTUNE_GELINCE_ARKA_PLAN = "#5A9BD8"

FONT_NORMAL_STIL = ("Arial", 10)
FONT_KALIN_STIL = ("Arial", 10, "bold")
FONT_BASLIK_STIL = ("Arial", 14, "bold")

hasta_listesi = []
doktor_listesi = []
doktorlar_ve_bolumler = {}
bolum_listesi = []


class Hasta:
    def __init__(self, ad, soyad, eposta, sifre, randevular=None):
        self.ad, self.soyad, self.eposta, self.sifre = ad, soyad, eposta, sifre
        self.randevular = randevular if randevular is not None else []

    def sifreyi_dogrula(self, kontrol_edilecek_sifre): return self.sifre == kontrol_edilecek_sifre

    def sozluge_donustur(self): return self.__dict__

    @classmethod
    def sozlukten_olustur(cls, veri): return cls(**veri)


class Doktor:
    def __init__(self, ad, soyad, sifre, bolum, randevular=None):
        self.ad, self.soyad, self.sifre, self.bolum = ad, soyad, sifre, bolum
        self.randevular = randevular if randevular is not None else []

    def sifreyi_dogrula(self, kontrol_edilecek_sifre): return self.sifre == kontrol_edilecek_sifre

    def tam_adi_getir(self): return f"Dr. {self.ad} {self.soyad}"

    def sozluge_donustur(self): return self.__dict__

    @classmethod
    def sozlukten_olustur(cls, veri): return cls(**veri)


def veri_dizinini_kontrol_et():
    if not os.path.exists(VERI_DIZINI): os.makedirs(VERI_DIZINI)


def tum_verileri_kaydet():
    veri_dizinini_kontrol_et()
    try:
        with open(HASTALAR_DOSYASI, 'w', encoding='utf-8') as f:
            json.dump([p.sozluge_donustur() for p in hasta_listesi], f, indent=4, ensure_ascii=False)
        with open(DOKTORLAR_DOSYASI, 'w', encoding='utf-8') as f:
            json.dump([d.sozluge_donustur() for d in doktor_listesi], f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Kayıt Hatası", f"Veriler kaydedilemedi: {e}")


def tum_verileri_yukle():
    global hasta_listesi, doktor_listesi, bolum_listesi
    veri_dizinini_kontrol_et()
    varsayilan_doktorlar = [
        Doktor("Zeki Eren", "Köseoğlu", "123", "Kardiyoloji"),
        Doktor("İlhan Enes", "Kılıçarslan", "123", "Dahiliye"),
        Doktor("Enes", "Kaya", "123", "Dahiliye"),
        Doktor("Murat Can", "Yılmaz", "123", "KBB"),
        Doktor("Erdem", "Öztürk", "123", "Ortopedi"),
        Doktor("Bani", "Haznevi", "123", "Ortopedi"),
        Doktor("Ali Said", "Şaşmaz", "123", "Kardiyoloji"),
        Doktor("Zeki", "Erman", "123", "KBB")
    ]
    try:
        if os.path.exists(HASTALAR_DOSYASI):
            with open(HASTALAR_DOSYASI, 'r', encoding='utf-8') as f:
                hastalar_verisi = json.load(f)
                hasta_listesi = [Hasta.sozlukten_olustur(h_verisi) for h_verisi in hastalar_verisi]
        else:
            hasta_listesi = []

        if os.path.exists(DOKTORLAR_DOSYASI):
            with open(DOKTORLAR_DOSYASI, 'r', encoding='utf-8') as f:
                doktorlar_verisi = json.load(f)
                doktor_listesi = [Doktor.sozlukten_olustur(d_verisi) for d_verisi in doktorlar_verisi]
                if not doktor_listesi:
                    doktor_listesi = varsayilan_doktorlar
                    tum_verileri_kaydet()
        else:
            doktor_listesi = varsayilan_doktorlar
            tum_verileri_kaydet()
    except Exception as e:
        messagebox.showerror("Yükleme Hatası", f"Veriler yüklenemedi: {e}.\nVarsayılanlarla devam ediliyor.")
        hasta_listesi = []
        doktor_listesi = varsayilan_doktorlar
    doktor_bolum_yapilarini_yeniden_olustur()


def doktor_bolum_yapilarini_yeniden_olustur():
    global doktorlar_ve_bolumler, bolum_listesi
    benzersiz_bolumler = set()
    for dr in doktor_listesi:
        benzersiz_bolumler.add(dr.bolum)
    bolum_listesi[:] = sorted(list(benzersiz_bolumler))
    doktorlar_ve_bolumler.clear()
    for bolum_adi in bolum_listesi:
        doktorlar_ve_bolumler[bolum_adi] = []
    for dr in doktor_listesi:
        if dr.bolum in doktorlar_ve_bolumler:
            doktorlar_ve_bolumler[dr.bolum].append(dr.tam_adi_getir())


def eposta_ile_hasta_bul(eposta):
    return next((h for h in hasta_listesi if h.eposta.lower() == eposta.lower()), None)


def tam_ad_ile_doktor_bul(onek_ile_ad_str):
    if not onek_ile_ad_str.startswith("Dr. "): return None
    oneksiz_ad = onek_ile_ad_str[len("Dr. "):]
    for d in doktor_listesi:
        if f"{d.ad} {d.soyad}" == oneksiz_ad: return d
    return None


class Uygulama(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Basit Hastane Randevu Sistemi")
        self.geometry("500x550")
        self.configure(bg=ANA_ARKA_PLAN)
        self._gecerli_kullanici = None
        self._aktif_cerceve = None
        self.pencereyi_ortala()

        self.stil = ttk.Style(self)
        try:
            self.stil.theme_use('clam')
        except tk.TclError:
            pass

        self.stil.configure('TFrame', background=ANA_ARKA_PLAN)
        self.stil.configure('TLabel', background=ANA_ARKA_PLAN, foreground=METIN_RENGI, font=FONT_NORMAL_STIL)
        self.stil.configure('Title.TLabel', font=FONT_BASLIK_STIL, background=ANA_ARKA_PLAN, foreground=METIN_RENGI)

        self.stil.configure('TButton', font=FONT_NORMAL_STIL, background=BUTON_ARKA_PLAN, foreground=BUTON_YAZI_RENGI, padding=5,
                             borderwidth=1, relief="raised")
        self.stil.map('TButton',
                       background=[('active', BUTON_USTUNE_GELINCE_ARKA_PLAN), ('pressed', BUTON_ARKA_PLAN)],
                       relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        self.stil.configure('Accent.TButton', font=FONT_KALIN_STIL, background=VURGU_BUTON_ARKA_PLAN,
                             foreground=VURGU_BUTON_YAZI_RENGI, padding=5, borderwidth=1, relief="raised")
        self.stil.map('Accent.TButton',
                       background=[('active', VURGU_BUTON_USTUNE_GELINCE_ARKA_PLAN), ('pressed', VURGU_BUTON_ARKA_PLAN)],
                       relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        self.stil.configure('TEntry', fieldbackground=GIRIS_ALANI_ARKA_PLAN, foreground=METIN_RENGI, font=FONT_NORMAL_STIL,
                             padding=3)
        self.stil.configure('TCombobox', fieldbackground=GIRIS_ALANI_ARKA_PLAN, foreground=METIN_RENGI, font=FONT_NORMAL_STIL,
                             padding=3)
        self.stil.map('TCombobox',
                       fieldbackground=[('readonly', GIRIS_ALANI_ARKA_PLAN)])

        self.stil.configure('TLabelFrame', background=IKINCIL_ARKA_PLAN, borderwidth=1, relief="groove")
        self.stil.configure('TLabelFrame.Label', background=IKINCIL_ARKA_PLAN, foreground=METIN_RENGI, font=FONT_KALIN_STIL)

        self.protocol("WM_DELETE_WINDOW", self.kapatilirken)
        self.cerceveyi_degistir(GirisCercevesi)

    def pencereyi_ortala(self):
        self.update_idletasks()
        genislik, yukseklik = self.winfo_width(), self.winfo_height()
        ekran_genisligi, ekran_yuksekligi = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (ekran_genisligi // 2) - (genislik // 2)
        y = (ekran_yuksekligi // 2) - (yukseklik // 2)
        self.geometry(f'{genislik}x{yukseklik}+{x}+{y}')

    def cerceveyi_degistir(self, cerceve_sinifi, kullanici_nesnesi=None):
        if self._aktif_cerceve: self._aktif_cerceve.destroy()
        self._aktif_cerceve = cerceve_sinifi(self, kullanici_nesnesi=kullanici_nesnesi)
        self._aktif_cerceve.pack(expand=True, fill="both", padx=10, pady=10)

    def cikis_yap(self):
        self._gecerli_kullanici = None
        self.cerceveyi_degistir(GirisCercevesi)
        messagebox.showinfo("Çıkış", "Başarıyla çıkış yapıldı.", parent=self)

    def kapatilirken(self):
        if messagebox.askokcancel("Çıkış", "Uygulamadan çıkmak istiyor musunuz?", parent=self):
            tum_verileri_kaydet()
            self.destroy()


class GirisCercevesi(ttk.Frame):
    def __init__(self, ana_uygulama, kullanici_nesnesi=None):
        super().__init__(ana_uygulama)
        self.ana_uygulama = ana_uygulama

        ttk.Label(self, text="Hastane Randevu Sistemi", style='Title.TLabel').pack(pady=20)

        defter = ttk.Notebook(self)
        hasta_sekmesi = ttk.Frame(defter, padding=10)
        defter.add(hasta_sekmesi, text='Hasta İşlemleri')
        self.hasta_arayuzunu_olustur(hasta_sekmesi)

        doktor_sekmesi = ttk.Frame(defter, padding=10)
        defter.add(doktor_sekmesi, text='Doktor Girişi')
        self.doktor_arayuzunu_olustur(doktor_sekmesi)
        defter.pack(expand=True, fill="both", padx=20, pady=10)

    def hasta_arayuzunu_olustur(self, ana_cerceve):
        kayit_cercevesi = ttk.LabelFrame(ana_cerceve, text="Hasta Kayıt Ol", padding=10)
        kayit_cercevesi.pack(fill="x", pady=10)
        self.kayit_girisleri = {}
        alanlar = ["Ad", "Soyad", "E-posta", "Şifre"]
        alan_anahtarlari = ["ad", "soyad", "eposta", "sifre"]

        for i, (alan_etiketi, alan_anahtari) in enumerate(zip(alanlar, alan_anahtarlari)):
            ttk.Label(kayit_cercevesi, text=f"{alan_etiketi}:").grid(row=i, column=0, padx=5, pady=3, sticky="w")
            giris = ttk.Entry(kayit_cercevesi, width=30, show="*" if alan_etiketi == "Şifre" else "")
            giris.grid(row=i, column=1, padx=5, pady=3, sticky="ew")
            self.kayit_girisleri[alan_anahtari] = giris
        ttk.Button(kayit_cercevesi, text="Kayıt Ol", command=self.hasta_kaydi_yap, style="Accent.TButton").grid(row=len(alanlar),
                                                                                                   column=0,
                                                                                                   columnspan=2,
                                                                                                   pady=10, sticky="ew")

        giris_cercevesi = ttk.LabelFrame(ana_cerceve, text="Hasta Girişi", padding=10)
        giris_cercevesi.pack(fill="x", pady=10)
        ttk.Label(giris_cercevesi, text="E-posta:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.giris_eposta_alani = ttk.Entry(giris_cercevesi, width=30)
        self.giris_eposta_alani.grid(row=0, column=1, padx=5, pady=3, sticky="ew")
        ttk.Label(giris_cercevesi, text="Şifre:").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        self.giris_sifre_alani = ttk.Entry(giris_cercevesi, show="*", width=30)
        self.giris_sifre_alani.grid(row=1, column=1, padx=5, pady=3, sticky="ew")
        ttk.Button(giris_cercevesi, text="Giriş Yap", command=self.hasta_giris_yap, style="TButton").grid(row=2, column=0,
                                                                                                      columnspan=2,
                                                                                                      pady=10,
                                                                                                      sticky="ew")

    def doktor_arayuzunu_olustur(self, ana_cerceve):
        giris_cercevesi = ttk.LabelFrame(ana_cerceve, text="Doktor Girişi", padding=10)
        giris_cercevesi.pack(fill="x", pady=20)
        ttk.Label(giris_cercevesi, text="Ad Soyad:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.giris_doktor_ad_soyad = ttk.Entry(giris_cercevesi, width=30)
        self.giris_doktor_ad_soyad.grid(row=0, column=1, padx=5, pady=3, sticky="ew")
        ttk.Label(giris_cercevesi, text="Şifre:").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        self.giris_doktor_sifre = ttk.Entry(giris_cercevesi, show="*", width=30)
        self.giris_doktor_sifre.grid(row=1, column=1, padx=5, pady=3, sticky="ew")
        ttk.Button(giris_cercevesi, text="Doktor Giriş Yap", command=self.doktor_giris_yap, style="TButton").grid(row=2,
                                                                                                              column=0,
                                                                                                              columnspan=2,
                                                                                                              pady=10,
                                                                                                              sticky="ew")

    def hasta_kaydi_yap(self):
        ad = self.kayit_girisleri['ad'].get().strip()
        soyad = self.kayit_girisleri['soyad'].get().strip()
        eposta = self.kayit_girisleri['eposta'].get().strip()
        sifre = self.kayit_girisleri['sifre'].get()
        if not (ad and soyad and eposta and sifre):
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.", parent=self)
            return
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', eposta):
            messagebox.showerror("Hata", "Geçersiz e-posta.", parent=self)
            return
        if eposta_ile_hasta_bul(eposta):
            messagebox.showerror("Hata", "E-posta zaten kayıtlı.", parent=self)
            return
        hasta_listesi.append(Hasta(ad, soyad, eposta, sifre))
        tum_verileri_kaydet()
        messagebox.showinfo("Başarılı", "Kayıt tamamlandı!", parent=self)
        for giris in self.kayit_girisleri.values(): giris.delete(0, tk.END)

    def hasta_giris_yap(self):
        eposta = self.giris_eposta_alani.get().strip()
        sifre = self.giris_sifre_alani.get()
        hasta = eposta_ile_hasta_bul(eposta)
        if hasta and hasta.sifreyi_dogrula(sifre):
            self.ana_uygulama.cerceveyi_degistir(HastaPaneli, kullanici_nesnesi=hasta)
        else:
            messagebox.showerror("Hata", "E-posta veya şifre hatalı.", parent=self)

    def doktor_giris_yap(self):
        ad_soyad = self.giris_doktor_ad_soyad.get().strip()
        sifre = self.giris_doktor_sifre.get()
        doktor = next((d for d in doktor_listesi if (d.ad + " " + d.soyad).lower() == ad_soyad.lower()), None)
        if doktor and doktor.sifreyi_dogrula(sifre):
            self.ana_uygulama.cerceveyi_degistir(DoktorPaneli, kullanici_nesnesi=doktor)
        else:
            messagebox.showerror("Hata", "Doktor adı soyadı veya şifre hatalı.", parent=self)


class HastaPaneli(ttk.Frame):
    def __init__(self, ana_uygulama, kullanici_nesnesi):
        super().__init__(ana_uygulama)
        self.ana_uygulama = ana_uygulama
        self.hasta = kullanici_nesnesi
        ttk.Label(self, text=f"Hoş Geldiniz, {self.hasta.ad} {self.hasta.soyad}", style='Title.TLabel').pack(
            pady=20)
        ttk.Button(self, text="Yeni Randevu Al", command=self.yeni_randevu_penceresi_ac, style="Accent.TButton").pack(
            pady=10, ipadx=10, ipady=5)
        ttk.Button(self, text="Randevularımı Görüntüle", command=self.randevularim_penceresi_ac, style="TButton").pack(
            pady=10, ipadx=10, ipady=5)
        ttk.Button(self, text="Çıkış Yap", command=self.ana_uygulama.cikis_yap, style="TButton").pack(pady=20, ipadx=10,
                                                                                                 ipady=5)

    def yeni_randevu_penceresi_ac(self): YeniRandevuPenceresi(self.ana_uygulama, self.hasta)
    def randevularim_penceresi_ac(self): RandevularimPenceresi(self.ana_uygulama, self.hasta)


class DoktorPaneli(ttk.Frame):
    def __init__(self, ana_uygulama, kullanici_nesnesi):
        super().__init__(ana_uygulama)
        self.ana_uygulama = ana_uygulama
        self.doktor = kullanici_nesnesi
        ttk.Label(self, text=f"Dr. Paneli: {self.doktor.tam_adi_getir()} ({self.doktor.bolum})",
                  style='Title.TLabel').pack(pady=20)
        ttk.Button(self, text="Randevularımı Görüntüle", command=self.doktor_randevulari_penceresi_ac,
                   style="Accent.TButton").pack(pady=10, ipadx=10, ipady=5)
        ttk.Button(self, text="Çıkış Yap", command=self.ana_uygulama.cikis_yap, style="TButton").pack(pady=20, ipadx=10,
                                                                                                 ipady=5)

    def doktor_randevulari_penceresi_ac(self): DoktorRandevulariPenceresi(self.ana_uygulama, self.doktor)


class OzelUstPencere(tk.Toplevel):
    def __init__(self, ana_uygulama, baslik="", geometri="400x300"):
        super().__init__(ana_uygulama)
        self.ana_uygulama = ana_uygulama
        self.title(baslik)
        self.geometry(geometri)
        self.configure(bg=ANA_ARKA_PLAN)
        self.transient(ana_uygulama)
        self.grab_set()
        self.ana_pencereye_ortala()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def ana_pencereye_ortala(self):
        self.update_idletasks()
        ana_x, ana_y = self.ana_uygulama.winfo_x(), self.ana_uygulama.winfo_y()
        ana_genislik, ana_yukseklik = self.ana_uygulama.winfo_width(), self.ana_uygulama.winfo_height()
        genislik, yukseklik = self.winfo_width(), self.winfo_height()
        x = ana_x + (ana_genislik - genislik) // 2
        y = ana_y + (ana_yukseklik - yukseklik) // 2
        self.geometry(f'+{x}+{y}')


class YeniRandevuPenceresi(OzelUstPencere):
    def __init__(self, ana_uygulama, hasta):
        super().__init__(ana_uygulama, baslik="Yeni Randevu Al", geometri="450x250")
        self.hasta = hasta
        kapsayici = ttk.Frame(self, padding=15)
        kapsayici.pack(expand=True, fill="both")

        ttk.Label(kapsayici, text="Bölüm:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.bolum_degiskeni = tk.StringVar()
        self.bolum_acilir_liste = ttk.Combobox(kapsayici, textvariable=self.bolum_degiskeni, values=bolum_listesi, state="readonly",
                                        width=30)
        if bolum_listesi: self.bolum_degiskeni.set(bolum_listesi[0])
        self.bolum_acilir_liste.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.bolum_acilir_liste.bind("<<ComboboxSelected>>", self.doktor_listesini_guncelle)

        ttk.Label(kapsayici, text="Doktor:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.doktor_degiskeni = tk.StringVar()
        self.doktor_acilir_liste = ttk.Combobox(kapsayici, textvariable=self.doktor_degiskeni, state="readonly", width=30)
        self.doktor_acilir_liste.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(kapsayici, text="Tarih (gg/aa/yyyy SS:DD):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.tarih_saat_girisi = ttk.Entry(kapsayici, width=32)
        self.tarih_saat_girisi.insert(0, datetime.datetime.now().strftime("%d/%m/%Y %H:00"))
        self.tarih_saat_girisi.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(kapsayici, text="Randevu Oluştur", command=self.randevuyu_onayla, style="Accent.TButton").grid(row=3,
                                                                                                                column=0,
                                                                                                                columnspan=2,
                                                                                                                pady=15,
                                                                                                                sticky="ew",
                                                                                                                ipady=3)
        self.doktor_listesini_guncelle()

    def doktor_listesini_guncelle(self, olay=None):
        secili_bolum = self.bolum_degiskeni.get()
        doktorlar = doktorlar_ve_bolumler.get(secili_bolum, [])
        self.doktor_acilir_liste['values'] = doktorlar
        if doktorlar:
            self.doktor_degiskeni.set(doktorlar[0])
        else:
            self.doktor_degiskeni.set("")

    def randevuyu_onayla(self):
        bolum = self.bolum_degiskeni.get()
        doktor_str = self.doktor_degiskeni.get()
        tarih_str = self.tarih_saat_girisi.get()
        if not (bolum and doktor_str and tarih_str):
            messagebox.showerror("Eksik Bilgi", "Lütfen tüm alanları doldurun.", parent=self)
            return
        try:
            randevu_zamani = datetime.datetime.strptime(tarih_str, "%d/%m/%Y %H:%M")
            if randevu_zamani < datetime.datetime.now():
                messagebox.showwarning("Geçersiz Tarih", "Geçmişe randevu alamazsınız.", parent=self)
                return
        except ValueError:
            messagebox.showerror("Hatalı Format", "Tarih gg/aa/yyyy SS:DD formatında olmalıdır.", parent=self)
            return

        doktor_nesnesi = tam_ad_ile_doktor_bul(doktor_str)
        if not doktor_nesnesi:
            messagebox.showerror("Hata", "Doktor bulunamadı.", parent=self)
            return

        if any(rnd[1] == tarih_str for rnd in doktor_nesnesi.randevular):
            messagebox.showwarning("Çakışma", f"{doktor_str} için bu saat dolu.", parent=self)
            return
        if any(rnd[2] == tarih_str for rnd in self.hasta.randevular):
            messagebox.showwarning("Çakışma", "Sizin bu saatte başka randevunuz var.", parent=self)
            return

        self.hasta.randevular.append((bolum, doktor_str, tarih_str))
        doktor_nesnesi.randevular.append((f"{self.hasta.ad} {self.hasta.soyad}", tarih_str))
        tum_verileri_kaydet()
        messagebox.showinfo("Başarılı", "Randevunuz oluşturuldu.", parent=self)
        self.destroy()


class RandevularimPenceresi(OzelUstPencere):
    def __init__(self, ana_uygulama, hasta):
        super().__init__(ana_uygulama, baslik="Randevularım", geometri="700x350")
        self.hasta = hasta
        self._gelecek_randevu_eslesmesi = []

        ana_cerceve = ttk.Frame(self, padding=10)
        ana_cerceve.pack(expand=True, fill="both")

        gelecek_cercevesi = ttk.LabelFrame(ana_cerceve, text="Gelecek Randevular", padding=5)
        gelecek_cercevesi.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 5))
        self.liste_kutusu_gelecek = tk.Listbox(gelecek_cercevesi, width=45, height=10, exportselection=False, bg=LISTE_KUTUSU_ARKA_PLAN,
                                          font=FONT_NORMAL_STIL)
        kaydirma_cubugu_gelecek = ttk.Scrollbar(gelecek_cercevesi, orient="vertical", command=self.liste_kutusu_gelecek.yview)
        self.liste_kutusu_gelecek.config(yscrollcommand=kaydirma_cubugu_gelecek.set)
        self.liste_kutusu_gelecek.pack(side=tk.LEFT, fill="both", expand=True)
        kaydirma_cubugu_gelecek.pack(side=tk.RIGHT, fill="y")

        gecmis_cercevesi = ttk.LabelFrame(ana_cerceve, text="Geçmiş Randevular", padding=5)
        gecmis_cercevesi.pack(side=tk.RIGHT, fill="both", expand=True, padx=(5, 0))
        self.liste_kutusu_gecmis = tk.Listbox(gecmis_cercevesi, width=45, height=10, exportselection=False, bg=LISTE_KUTUSU_ARKA_PLAN,
                                         font=FONT_NORMAL_STIL)
        kaydirma_cubugu_gecmis = ttk.Scrollbar(gecmis_cercevesi, orient="vertical", command=self.liste_kutusu_gecmis.yview)
        self.liste_kutusu_gecmis.config(yscrollcommand=kaydirma_cubugu_gecmis.set)
        self.liste_kutusu_gecmis.pack(side=tk.LEFT, fill="both", expand=True)
        kaydirma_cubugu_gecmis.pack(side=tk.RIGHT, fill="y")

        self.randevulari_doldur()
        ttk.Button(ana_cerceve, text="Seçili Gelecek Randevuyu İptal Et", command=self.randevuyu_iptal_et,
                   style="Accent.TButton").pack(pady=10, side=tk.BOTTOM, ipady=3)

    def randevulari_doldur(self):
        self.liste_kutusu_gelecek.delete(0, tk.END)
        self.liste_kutusu_gecmis.delete(0, tk.END)
        self._gelecek_randevu_eslesmesi.clear()
        simdi = datetime.datetime.now()
        try:
            sirali_randevular = sorted(self.hasta.randevular,
                                       key=lambda r: datetime.datetime.strptime(r[2], "%d/%m/%Y %H:%M"))
        except ValueError:
            sirali_randevular = self.hasta.randevular
            messagebox.showwarning("Veri Uyarısı", "Bazı randevu tarihleri hatalı.", parent=self)

        for randevu_verisi in sirali_randevular:
            bilgi = f"{randevu_verisi[0]} | {randevu_verisi[1]} | {randevu_verisi[2]}"
            try:
                randevu_tarih_saat_nesnesi = datetime.datetime.strptime(randevu_verisi[2], "%d/%m/%Y %H:%M")
                if randevu_tarih_saat_nesnesi > simdi:
                    self.liste_kutusu_gelecek.insert(tk.END, bilgi)
                    self._gelecek_randevu_eslesmesi.append(randevu_verisi)
                else:
                    self.liste_kutusu_gecmis.insert(tk.END, bilgi)
            except ValueError:
                self.liste_kutusu_gecmis.insert(tk.END, f"HATALI: {bilgi}")

    def randevuyu_iptal_et(self):
        secili_indeksler = self.liste_kutusu_gelecek.curselection()
        if not secili_indeksler:
            messagebox.showwarning("Uyarı", "İptal için bir randevu seçin.", parent=self)
            return

        secili_orjinal_randevu = self._gelecek_randevu_eslesmesi[secili_indeksler[0]]

        if secili_orjinal_randevu in self.hasta.randevular:
            self.hasta.randevular.remove(secili_orjinal_randevu)
            doktor_nesnesi = tam_ad_ile_doktor_bul(secili_orjinal_randevu[1])
            if doktor_nesnesi:
                doktor_randevu_kaydi = (f"{self.hasta.ad} {self.hasta.soyad}", secili_orjinal_randevu[2])
                if doktor_randevu_kaydi in doktor_nesnesi.randevular:
                    doktor_nesnesi.randevular.remove(doktor_randevu_kaydi)
            tum_verileri_kaydet()
            self.randevulari_doldur()
            messagebox.showinfo("Başarılı", "Randevu iptal edildi.", parent=self)
        else:
            messagebox.showerror("Hata", "Randevu listede bulunamadı.", parent=self)


class DoktorRandevulariPenceresi(OzelUstPencere):
    def __init__(self, ana_uygulama, doktor):
        super().__init__(ana_uygulama, baslik=f"Dr. {doktor.ad} {doktor.soyad} - Randevular",
                         geometri="600x300")
        self.doktor = doktor
        kapsayici = ttk.LabelFrame(self, text="Randevu Listesi", padding=10)
        kapsayici.pack(expand=True, fill="both", padx=10, pady=10)

        self.liste_kutusu_randevular = tk.Listbox(kapsayici, width=70, height=10, bg=LISTE_KUTUSU_ARKA_PLAN,
                                             font=FONT_NORMAL_STIL)
        kaydirma_cubugu = ttk.Scrollbar(kapsayici, orient="vertical", command=self.liste_kutusu_randevular.yview)
        self.liste_kutusu_randevular.config(yscrollcommand=kaydirma_cubugu.set)
        self.liste_kutusu_randevular.pack(side=tk.LEFT, fill="both", expand=True)
        kaydirma_cubugu.pack(side=tk.RIGHT, fill="y")
        self.doktor_randevularini_doldur()

    def doktor_randevularini_doldur(self):
        self.liste_kutusu_randevular.delete(0, tk.END)
        simdi = datetime.datetime.now()
        if not self.doktor.randevular:
            self.liste_kutusu_randevular.insert(tk.END, "Görüntülenecek randevu yok.")
            return
        try:
            sirali_randevular = sorted(self.doktor.randevular,
                                       key=lambda r: datetime.datetime.strptime(r[1], "%d/%m/%Y %H:%M"))
        except ValueError:
            sirali_randevular = self.doktor.randevular
            messagebox.showwarning("Veri Uyarısı", "Bazı randevu tarihleri hatalı.", parent=self)

        for hasta_tam_ad, tarih_saat_str in sirali_randevular:
            try:
                randevu_tarih_saat_nesnesi = datetime.datetime.strptime(tarih_saat_str, "%d/%m/%Y %H:%M")
                durum_etiketi = " (Geçmiş)" if randevu_tarih_saat_nesnesi < simdi else " (Gelecek)"
                self.liste_kutusu_randevular.insert(tk.END, f"Hasta: {hasta_tam_ad} - Tarih: {tarih_saat_str}{durum_etiketi}")
            except ValueError:
                self.liste_kutusu_randevular.insert(tk.END, f"HATALI: Hasta: {hasta_tam_ad} - Tarih: {tarih_saat_str}")


if __name__ == "__main__":
    tum_verileri_yukle()
    uygulama = Uygulama()
    uygulama.mainloop()