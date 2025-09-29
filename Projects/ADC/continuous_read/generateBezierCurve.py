import numpy as np
import soundfile as sf

def vel_bezier_env(
    dur=5.0, fs=48_000, KF=24.0,
    r=(252, 1050, 1800, 1575, 700, 126),
    shift=0.0, tajuste=0.5
):
    """
    Build the Bézier-shaped envelope V_Bezier(t) and time-scale it so the
    overall duration equals `dur` seconds.

    Parameters
    ----------
    dur : float
        Desired total duration in seconds.
    fs : int
        Sample rate (Hz).
    KF : float
        Scale factor (matches your original code's KF).
    r : tuple
        Coefficients (r1..r6) of the polynomial used inside the Bézier term.
    shift : float
        Time shift used in the original piecewise definition (pre-scaling).
    tajuste : float
        Adjustment offset used in the original timing (pre-scaling).

    Returns
    -------
    env : np.ndarray (float32)
        Envelope samples shaped by your piecewise Bézier logic.
    fs : int
        Sample rate (returned for convenience).
    """
    r1, r2, r3, r4, r5, r6 = r

    # Original (base) time marks before scaling
    T1b = 0.1 + shift
    T2b = 0.2 + shift
    T3b = 1.0 + shift + tajuste
    T4b = 1.7 + shift + tajuste
    T5b = 2.7 + shift + tajuste
    T6b = 2.8 + shift + tajuste
    base_end = T6b

    # Scale all time marks so the final time equals `dur`
    s = dur / base_end
    T1, T2, T3, T4, T5, T6 = [t * s for t in (T1b, T2b, T3b, T4b, T5b, T6b)]

    # Time vector
    t = np.arange(int(fs * dur)) / fs

    def Bezier(K1):
        # Clamp to [0,1] to avoid extrapolation artifacts
        K1 = np.clip(K1, 0.0, 1.0)
        return (K1**5) * (
            r1 - (r2 * K1) + (r3 * K1**2) - (r4 * K1**3) + (r5 * K1**4) - (r6 * K1**5)
        )

    # Default value for t > T6 (matches your final 'else' branch: KF*(1-0.25))
    y = np.full_like(t, KF * (1 - 0.25), dtype=np.float32)

    # Region t <= T1
    m = (t <= T1)
    y[m] = 0.0

    # Region T1 < t <= T2 (ramp up to 100% of KF using Bézier)
    m = (t > T1) & (t <= T2)
    K1 = (t[m] - T1) / (T2 - T1)
    y[m] = KF * Bezier(K1)

    # Region T2 < t <= T3 (hold at 100% KF)
    m = (t > T2) & (t <= T3)
    y[m] = KF

    # Region T3 < t <= T4 (ramp down to 50% KF using Bézier)
    m = (t > T3) & (t <= T4)
    K1 = (t[m] - T3) / (T4 - T3)
    y[m] = KF - KF * 0.5 * Bezier(K1)

    # Region T4 < t <= T5 (hold at 50% KF)
    m = (t > T4) & (t <= T5)
    y[m] = KF * 0.5

    # Region T5 < t <= T6 (ramp up from 50% to 75% KF using Bézier)
    m = (t > T5) & (t <= T6)
    K1 = (t[m] - T5) / (T6 - T5)
    y[m] = (KF * 0.5) + KF * 0.25 * Bezier(K1)

    return y.astype(np.float32), fs


def render_bezier_tone(filename, dur=5.0, fs=48_000, f0=440.0, amp=0.9, **env_kwargs):
    """
    Modulate a sine carrier with the Bézier envelope and write a WAV.

    Parameters
    ----------
    filename : str
        Output WAV path.
    dur : float
        Duration in seconds.
    fs : int
        Sample rate (Hz).
    f0 : float
        Carrier sine frequency (Hz).
    amp : float
        Peak gain for the final audio (<=1.0 recommended).
    **env_kwargs :
        Extra keyword args passed to vel_bezier_env (KF, r, shift, tajuste).

    Returns
    -------
    y : np.ndarray (float32)
        The rendered audio (mono), range roughly within [-amp, amp].
    fs : int
        Sample rate.
    """
    # Generate the envelope
    env, fs = vel_bezier_env(dur=dur, fs=fs, **env_kwargs)

    # Normalize envelope to [0, 1] for amplitude modulation
    env = env - env.min()
    peak = env.max()
    if peak > 0:
        env = env / peak

    # Generate carrier
    t = np.arange(int(fs * dur)) / fs
    car = np.sin(2 * np.pi * f0 * t).astype(np.float32)

    # Apply envelope and final amplitude limit
    y = (amp * env * car).astype(np.float32)

    # Save as 16-bit PCM WAV
    sf.write(filename, y, fs, subtype="PCM_16")
    return y, fs


# ----------------------
# Example usages
# ----------------------

# 5 seconds
y5, fs5 = render_bezier_tone("bezier_5s.wav", dur=5.0, f0=440.0)

# 1 second
y1, fs1 = render_bezier_tone("bezier_1s.wav", dur=1.0, f0=660.0)

# Fraction of a second (0.2 s)
# y02, fs02 = render_bezier_tone("bezier_0p2s.wav", dur=0.2, f0=880.0)
