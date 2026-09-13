# 🎙️ FFT Tabanlı Ses Analizi ve Gürültü Temizleme Sistemi

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![DSP](https://img.shields.io/badge/Signal%20Processing-FFT%20%2F%20STFT-orange.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

BİL314 - Sinyaller ve Sistemler dersi kapsamında geliştirilen bu proje; sayısal ses sinyallerindeki gürültü bileşenlerini **Hızlı Fourier Dönüşümü (FFT)** ve spektral çıkarma (spectral gating) yöntemleriyle tespit edip temizleyen, hem çevrimdışı (dosya tabanlı) hem de mikrofon üzerinden gerçek zamanlı (real-time) çalışan bir gürültü engelleme sistemidir.

---

## 📌 İçindekiler
- [Proje Özeti ve Temel Özellikler](#-proje-özeti-ve-temel-özellikler)
- [Algoritma ve Çalışma Mantığı](#-algoritma-ve-çalışma-mantığı)
- [Proje Mimarisi](#-proje-mimarisi)
- [Kurulum](#-kurulum)
- [Kullanım Senaryoları](#-kullanım-senaryoları)
  - [1. Sinyal Analizi ve SNR Tespiti](#1-sinyal-analizi-ve-snr-tespiti-sesanalizipy)
  - [2. Dosya Üzerinden Ses Temizleme](#2-dosya-üzerinden-ses-temizleme-sestemizlemepy)
  - [3. Gerçek Zamanlı (Canlı) Gürültü Giderme](#3-gerçek-zamanlı-canlı-gürültü-giderme-gercekzamanpy)
- [Kullanılan Kütüphaneler](#-kullanılan-kütüphaneler)
- [Lisans](#-lisans)

---

## 🚀 Proje Özeti ve Temel Özellikler

- **Zaman ve Frekans Domeni Analizi:** Ses sinyalinin dalga formu (`waveshow`) ve FFT ile spektral güç yoğunluğu grafikleri .
- **SNR (Sinyal-Gürültü Oranı) Hesaplama:** Hem zaman tabanlı eşikleme (amplitude thresholding) hem de bant enerjisi oranıyla teorik ve frekans domeni SNR hesabı .
- **Spektral Gürültü Giderme:** Gürültü profili (noise profile) çıkarımı üzerinden spektral filtreleme ile arka plan uğultusu, dip ses ve ortam parazitlerinin giderilmesi .
- **Canlı Akış (Real-Time Callback):** `sounddevice` ve blok bazlı işleme mimarisiyle mikrofondan alınan sesin filtrelenerek anlık olarak hoparlöre aktarılması .
- **Bandpass Filtreleme:** Butterworth bandpass filtresi (500 Hz – 4400 Hz) ile insan ses bandı dışındaki harmoniklerin ve frekansların bastırılması .

---

## 🔬 Algoritma ve Çalışma Mantığı

1. **Örnekleme & Sinyal Dönüşümü:** $x[n]$ ayrık ses sinyali `librosa` ile yüklenir ve genlik değerleri normalize edilir .
2. **Hızlı Fourier Dönüşümü (FFT):** Zaman domenindeki sinyal frekans bileşenlerine ayrıştırılarak konuşma bandı (300 Hz – 4000 Hz) ve gürültü baskın bölgeler ayrıştırılır .
3. **Spektral Azaltma & Karşılaştırma:** Kayıttan alınan ortam gürültü kesiti temel alınarak spektral baskılama uygulanır . Temizlenmiş sinyal ile ham sinyalin frekans spektrumları görsel olarak karşılaştırılır .

---

## 📂 Proje Mimarisi

```text
FFT_ses_temizleme/
├── README.md              # Proje dokümantasyonu
├── sesanalizi.py          # Zaman/frekans domeni görselleştirme ve SNR hesabı
├── sestemizleme.py        # Çevrimdışı ses dosyası filtreleme ve FFT karşılaştırması
└── gercekzaman.py         # Mikrofondan anlık gürültü profilleme ve canlı filtreleme
```

---

## 🛠️ Kurulum

Python 3.10 sürümüyle izole bir Conda ortamı oluşturulması önerilir :

```bash
# 1. Depoyu klonlayın
git clone [https://github.com/beyza-ozben/FFT_ses_temizleme.git](https://github.com/beyza-ozben/FFT_ses_temizleme.git)
cd FFT_ses_temizleme

# 2. Conda ortamı oluşturun ve aktif edin
conda create --name sinyal python=3.10 -y
conda activate sinyal

# 3. Gerekli paketleri yükleyin
pip install numpy scipy matplotlib librosa noisereduce soundfile sounddevice pyaudio
```

> **Not:** Linux ortamında ses aygıtı kütüphaneleri için `libasound2-dev` veya `portaudio19-dev` paketlerine ihtiyaç duyulabilir:
> ```bash
> sudo apt-get update && sudo apt-get install -y portaudio19-dev libasound2-dev
> ```

---

## 💻 Kullanım Senaryoları

Test ses dosyalarınızın kayıpsız `.wav` formatında olması önerilir .

### 1. Sinyal Analizi ve SNR Tespiti (`sesanalizi.py`)
Mevcut ses dosyasının zaman serisi dalga formunu, örnekleme frekansını, sinyal gücünü ve FFT tabanlı frekans spektrumunu inceler :
```bash
python sesanalizi.py
```
- **Çıktılar:** Dalga boyu grafiği, 0–Fs/2 frekans spektrumu, zaman & frekans domeni SNR değerleri .

### 2. Dosya Üzerinden Ses Temizleme (`sestemizleme.py`)
Belirlenen gürültü aralığını referans alarak ses dosyasını filtreler, temiz halini yeni bir `.wav` dosyası olarak kaydeder ve FFT karşılaştırma spektrumunu çizer :
```bash
python sestemizleme.py
```
- **Parametre Ayarı:** Kod içerisindeki `noise_sample = y[:int(sr * 5)]` kısmını kendi kaydınızdaki yalnızca arka plan gürültüsünün bulunduğu saniye aralığına göre güncelleyebilirsiniz .

### 3. Gerçek Zamanlı (Canlı) Gürültü Giderme (`gercekzaman.py`)
Çalıştırıldığında önce 2 saniye ortamı dinleyerek referans gürültü matrisini çıkarır, ardından gerçek zamanlı callback akışında Butterworth Bandpass ve gürültü azaltımını uygulayarak temiz sesi çıkışa verir :
```bash
python gercekzaman.py
```
- Programı sonlandırmak için terminalde `Enter` tuşuna basmanız yeterlidir .

---

## 📦 Kullanılan Kütüphaneler

| Kütüphane | Kullanım Amacı |
|---|---|
| **NumPy** | Matris işlemleri, FFT spektral vektör hesapları ve dizi manipülasyonu  |
| **SciPy** | Hızlı Fourier Dönüşümü (`scipy.fft`) ve Butterworth filtre tasarımı  |
| **Librosa** | Ses yükleme, zaman domeni gösterimi ve örnekleme frekansı yönetimi  |
| **NoiseReduce** | Spektral çıkarma (spectral gating) tabanlı dinamik gürültü filtreleme  |
| **SoundDevice** | Düşük gecikmeli gerçek zamanlı ses girişi ve çıkış akışı yönetimi  |
| **SoundFile** | `.wav` formatında kayıpsız ses dışa aktarma  |
| **Matplotlib** | Zaman serisi ve FFT frekans spektrumu görselleştirme  |

---

## 📄 Lisans
Bu proje eğitim ve araştırma amaçlı hazırlanmış olup MIT lisansı altında serbestçe geliştirilebilir.
