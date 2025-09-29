import numpy as np
import soundfile as sf

def overdamped_impulse(fs=48_000, dur=3.0, wn=2*np.pi*4, zeta=1.6, peak=0.95):
    """
    fs:   sample rate
    dur:  duración (s)
    wn:   frecuencia natural (rad/s) -> elige 2π*3 a 2π*8 para que sea “lento” y audible
    zeta: coeficiente de amortiguamiento (>1 sobreamortiguado)
    peak: pico máximo tras normalizar (evitar clipping)
    """
    assert zeta > 1.0, "Para sobreamortiguado usa zeta > 1"
    t = np.arange(int(fs*dur)) / fs
    d = np.sqrt(zeta**2 - 1.0)
    s1 = -wn*(zeta - d)
    s2 = -wn*(zeta + d)

    # Respuesta al impulso h(t) = (wn/(2*sqrt(zeta^2-1))) * (e^{s1 t} - e^{s2 t})
    h = (wn/(2*d)) * (np.exp(s1*t) - np.exp(s2*t))

    # Quitar DC y normalizar para audio
    y = h - h.mean()
    y /= (np.max(np.abs(y)) + 1e-12)
    y = (peak * y).astype(np.float32)
    return y, fs

y, fs = overdamped_impulse()
sf.write("overdamped_impulse.wav", y, fs, subtype="PCM_16")
