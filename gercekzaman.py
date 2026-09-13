import sounddevice as sd
import numpy as np
import noisereduce as nr
from scipy.signal import butter, lfilter

# --- Ayarlar ---
samplerate = 64000
frame_duration = 2  # saniye
frame_samples = int(samplerate * frame_duration)

print("⚠️  Gürültü örneği alınıyor. Lütfen 2 saniye sessiz kalın...")
noise_buffer = sd.rec(frame_samples, samplerate=samplerate, channels=1, dtype='float32')
sd.wait()
print("✅ Gürültü örneği alındı.")

# Gürültü örneğini 1D hale getir
noise_sample = noise_buffer[:, 0]

# --- Bandpass Filtre (isteğe bağlı) ---
def bandpass_filter(y, sr, lowcut=500.0, highcut=4400.0, order=5):
    nyq = 0.5 * sr
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, y)

# --- Giriş/Çıkış Akışı ---
def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(status)

    # Mono giriş (tek kanal)
    input_frame = indata[:, 0]

    # Gürültü azaltımı uygula
    denoised_frame = nr.reduce_noise(y=input_frame, y_noise=noise_sample, sr=samplerate, prop_decrease=1.0)

    # Bandpass filtre uygula (isteğe bağlı)
    denoised_frame = bandpass_filter(denoised_frame, samplerate)

    # Çıkışa aktar
    outdata[:, 0] = denoised_frame.astype(np.float32)

# --- Akışı Başlat ---
print("🎧 Mikrofon dinleniyor... Gürültü temizlenmiş ses hoparlöre aktarılıyor.")
with sd.Stream(channels=1, samplerate=samplerate, blocksize=frame_samples,
               callback=audio_callback):
    input("Çıkmak için Enter'a basın...\n")
