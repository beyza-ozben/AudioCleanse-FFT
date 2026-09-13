import librosa
import librosa.display
import noisereduce as nr
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

# --- Yolu Tanımla ---
file_path = "SinyalRöportaj6.wav"

# --- Ses Yükle ---
y, sr = librosa.load(file_path, sr=None)
print(f"Örnekleme frekansı: {sr} Hz")

# --- Gürültü örneği: İlk ... saniye (sadece ortam sesi) ---
noise_sample = y[:int(sr * 5)]

# --- Gürültü Azaltımı (NoiseReduce ile) ---
y_denoised = nr.reduce_noise(y=y, sr=sr, y_noise=noise_sample, prop_decrease=1.0)

# --- Temizlenmiş Dosyayı Kaydet ---
sf.write("çıktı6.wav", y_denoised, sr)

# --- FFT Karşılaştırmalı Görselleştirme ---
def plot_fft_comparison_zoomed(y1, y2, sr, label1="Orijinal", label2="Denoised", max_freq=2000):
    N = len(y1)
    Y1 = np.fft.fft(y1)
    Y2 = np.fft.fft(y2)
    freqs = np.fft.fftfreq(N, d=1/sr)

    # Sadece pozitif ve 0 - max_freq Hz arasındaki frekansları al
    mask = (freqs >= 0) & (freqs <= max_freq)

    plt.figure(figsize=(10, 4))
    plt.plot(freqs[mask], np.abs(Y1[mask]), label=label1, alpha=0.7, color='pink')
    plt.plot(freqs[mask], np.abs(Y2[mask]), label=label2, alpha=0.7, color='purple')
    plt.title(f"FFT Karşılaştırması ({label1} vs {label2})")
    plt.xlabel("Frekans (Hz)")
    plt.ylabel("Genlik")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


plot_fft_comparison_zoomed(y, y_denoised, sr, "Orijinal Sinyal", "Gürültü Giderilmiş Sinyal", max_freq=2000)


