import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Ses dosyasını yükleyin (örnek dosya: "audio.wav")
file_path = "SinyalRöportaj6.wav"
y, sr = librosa.load(file_path, sr=None)  # Orijinal örnekleme frekansını koru

# Ses sinyalini zaman domaininde görselleştirme
plt.figure(figsize=(14, 4))
librosa.display.waveshow(y, sr=sr)
plt.title('Zaman Domaininde Ses Sinyali')
plt.xlabel('Zaman (saniye)')
plt.ylabel('Genlik')
plt.show()

# Örnekleme frekansı
print(f"Örnekleme frekansı: {sr} Hz")

# Ortalama güç (Power)
signal_power = np.mean(y ** 2)
print(f"Sinyal Gücü: {signal_power:.4f}")

# Gürültü seviyesini tahmin etmek için düşük genlikli sinyal bölgesi seçimi
threshold = 0.01
noise = y[np.abs(y) < threshold]
noise_power = np.mean(noise ** 2) if len(noise) > 0 else 1e-10

# SNR hesaplama (dB cinsinden)
snr = 10 * np.log10(signal_power / noise_power)
print(f"Tahmini SNR: {snr:.2f} dB")

from scipy.fft import fft, fftfreq

# FFT uygulama
N = len(y)
yf = fft(y)
xf = fftfreq(N, 1 / sr)

# Yalnızca pozitif frekansları al
magnitude = np.abs(yf[:N//2])
frequencies = xf[:N//2]

# Güç Spektrumu görselleştirme
plt.figure(figsize=(12, 4))
plt.plot(frequencies, magnitude)
plt.title("Frekans Domaini - Güç Spektrumu")
plt.xlabel("Frekans (Hz)")
plt.ylabel("Genlik")
plt.xlim(0, sr/2)
plt.grid()
plt.show()

# Gürültü olarak 0-300 Hz ve 4000 Hz üzerini kabul et
speech_band = (frequencies >= 300) & (frequencies <= 4000)
noise_band = ~speech_band

speech_energy = np.sum(magnitude[speech_band] ** 2)
noise_energy = np.sum(magnitude[noise_band] ** 2)

print(f"Konuşma Enerjisi: {speech_energy:.2f}")
print(f"Gürültü Enerjisi: {noise_energy:.2f}")

snr_freq = 10 * np.log10(speech_energy / (noise_energy + 1e-10))
print(f"Frekans Domaininde Tahmini SNR: {snr_freq:.2f} dB")
