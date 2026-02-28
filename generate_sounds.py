"""Generate all WAV sound effects for the Scratch stickman animation project."""

import io
import struct
import numpy as np


SAMPLE_RATE = 22050


def _to_wav_bytes(samples_float, sample_rate=SAMPLE_RATE):
    """Convert float32 numpy array (-1..1) to WAV bytes (16-bit PCM mono)."""
    samples_float = np.clip(samples_float, -1.0, 1.0)
    # Normalize to avoid clipping
    peak = np.max(np.abs(samples_float))
    if peak > 0:
        samples_float = samples_float * 0.95 / peak
    int_samples = (samples_float * 32767).astype(np.int16)

    buf = io.BytesIO()
    num_samples = len(int_samples)
    data_size = num_samples * 2  # 16-bit = 2 bytes per sample
    # WAV header
    buf.write(b'RIFF')
    buf.write(struct.pack('<I', 36 + data_size))
    buf.write(b'WAVE')
    buf.write(b'fmt ')
    buf.write(struct.pack('<I', 16))       # chunk size
    buf.write(struct.pack('<H', 1))        # PCM format
    buf.write(struct.pack('<H', 1))        # mono
    buf.write(struct.pack('<I', sample_rate))
    buf.write(struct.pack('<I', sample_rate * 2))  # byte rate
    buf.write(struct.pack('<H', 2))        # block align
    buf.write(struct.pack('<H', 16))       # bits per sample
    buf.write(b'data')
    buf.write(struct.pack('<I', data_size))
    buf.write(int_samples.tobytes())
    return buf.getvalue()


def _envelope(t, attack=0.01, decay=0.0, sustain_level=1.0, release=0.01):
    """Simple ADSR-ish envelope."""
    dur = t[-1] if len(t) > 0 else 0
    env = np.ones_like(t)
    # Attack
    attack_mask = t < attack
    if attack > 0:
        env[attack_mask] = t[attack_mask] / attack
    # Release
    release_start = dur - release
    release_mask = t > release_start
    if release > 0:
        env[release_mask] = (dur - t[release_mask]) / release
    return env


def _noise(n):
    """Generate white noise samples."""
    return np.random.randn(n).astype(np.float32)


def _bandpass(signal, low_freq, high_freq, sr=SAMPLE_RATE):
    """Simple FFT-based bandpass filter."""
    n = len(signal)
    fft = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    mask = (freqs >= low_freq) & (freqs <= high_freq)
    fft[~mask] = 0
    return np.fft.irfft(fft, n).astype(np.float32)


def _pink_noise(n):
    """Generate pink noise using FFT method."""
    white = _noise(n)
    fft = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n, 1.0 / SAMPLE_RATE)
    freqs[0] = 1  # avoid division by zero
    fft = fft / np.sqrt(freqs)
    return np.fft.irfft(fft, n).astype(np.float32)


# ============================================================
# SOUND GENERATORS
# ============================================================

def _gen_typing_loop():
    """3s of rapid irregular keyboard clicks."""
    dur = 3.0
    n = int(SAMPLE_RATE * dur)
    result = np.zeros(n, dtype=np.float32)

    # Generate random clicks
    rng = np.random.RandomState(42)
    t = 0.0
    while t < dur:
        # Random interval between clicks
        interval = rng.uniform(0.04, 0.12)
        t += interval
        if t >= dur:
            break
        idx = int(t * SAMPLE_RATE)
        # Each click is a short noise burst
        click_len = int(rng.uniform(0.005, 0.015) * SAMPLE_RATE)
        if idx + click_len < n:
            click = rng.randn(click_len).astype(np.float32) * rng.uniform(0.2, 0.5)
            # Quick decay
            decay = np.exp(-np.linspace(0, 8, click_len))
            click *= decay
            result[idx:idx + click_len] += click

    # Bandpass to sound like keys
    result = _bandpass(result, 800, 6000)
    return _to_wav_bytes(result)


def _gen_chatter_loop():
    """5s of indistinct office murmuring."""
    dur = 5.0
    n = int(SAMPLE_RATE * dur)
    result = np.zeros(n, dtype=np.float32)
    rng = np.random.RandomState(123)

    # Create several "voices" as filtered noise bursts
    for _ in range(8):
        # Each voice has a random pitch range
        low = rng.uniform(80, 200)
        high = rng.uniform(250, 500)
        voice = _noise(n)
        voice = _bandpass(voice, low, high)

        # Create bursts (simulate words/syllables)
        t = rng.uniform(0, 0.5)
        while t < dur:
            burst_dur = rng.uniform(0.1, 0.4)
            pause = rng.uniform(0.05, 0.3)
            start_idx = int(t * SAMPLE_RATE)
            end_idx = min(int((t + burst_dur) * SAMPLE_RATE), n)
            if start_idx < n:
                burst_env = np.zeros(n, dtype=np.float32)
                burst_env[start_idx:end_idx] = 1.0
                # Smooth envelope
                if end_idx - start_idx > 10:
                    ramp = min(int(0.02 * SAMPLE_RATE), (end_idx - start_idx) // 4)
                    if ramp > 0:
                        burst_env[start_idx:start_idx + ramp] = np.linspace(0, 1, ramp)
                        burst_env[end_idx - ramp:end_idx] = np.linspace(1, 0, ramp)
                result += voice * burst_env * rng.uniform(0.05, 0.15)
            t += burst_dur + pause

    # Add slight room tone
    room = _bandpass(_noise(n), 100, 300) * 0.02
    result += room

    return _to_wav_bytes(result)


def _gen_office_hum():
    """3s low 60Hz hum with harmonics."""
    dur = 3.0
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False).astype(np.float32)
    hum = (np.sin(2 * np.pi * 60 * t) * 0.3 +
           np.sin(2 * np.pi * 120 * t) * 0.15 +
           np.sin(2 * np.pi * 180 * t) * 0.05)
    env = _envelope(t, attack=0.1, release=0.1)
    return _to_wav_bytes(hum * env * 0.15)


def _gen_explosion():
    """1.5s explosion boom."""
    dur = 1.5
    n = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, n, endpoint=False).astype(np.float32)

    # Low frequency boom
    boom_freq = 60
    boom = np.sin(2 * np.pi * boom_freq * t) * np.exp(-t * 4)
    # Sub-bass thump
    sub = np.sin(2 * np.pi * 40 * t) * np.exp(-t * 3) * 0.8

    # White noise burst with decay
    noise_burst = _noise(n) * np.exp(-t * 6)

    # Filtered rumble
    rumble = _bandpass(_noise(n), 30, 200) * np.exp(-t * 3) * 0.5

    result = boom * 0.6 + sub * 0.4 + noise_burst * 0.5 + rumble
    # Sharp attack
    attack_env = np.ones(n, dtype=np.float32)
    attack_samples = int(0.005 * SAMPLE_RATE)
    attack_env[:attack_samples] = np.linspace(0, 1, attack_samples)
    result *= attack_env

    return _to_wav_bytes(result)


def _gen_glass_shatter():
    """0.8s glass shattering sound."""
    dur = 0.8
    n = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, n, endpoint=False).astype(np.float32)

    # High-frequency noise
    glass = _bandpass(_noise(n), 2000, 8000)
    # Add some mid crackling
    crackle = _bandpass(_noise(n), 1000, 4000) * 0.3
    # Sharp attack, rapid decay with some sustain
    env = np.exp(-t * 8) * 0.7 + np.exp(-t * 2) * 0.3
    # Add random impulses (individual shards)
    rng = np.random.RandomState(77)
    for _ in range(15):
        pos = int(rng.uniform(0, n * 0.6))
        imp_len = int(rng.uniform(0.002, 0.01) * SAMPLE_RATE)
        if pos + imp_len < n:
            glass[pos:pos + imp_len] += rng.randn(imp_len) * rng.uniform(0.3, 0.8)

    result = (glass + crackle) * env
    return _to_wav_bytes(result)


def _gen_gasp():
    """0.5s short gasp/exclamation."""
    dur = 0.5
    n = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, n, endpoint=False).astype(np.float32)

    # Breathy noise burst with pitch rise
    noise = _bandpass(_noise(n), 300, 2000)
    # Pitch-like component
    freq = 400 + 200 * t / dur  # rising pitch
    tone = np.sin(2 * np.pi * freq * t) * 0.3
    env = np.exp(-t * 5) * (1 - np.exp(-t * 40))  # fast attack, medium decay
    result = (noise * 0.5 + tone) * env
    return _to_wav_bytes(result)


def _gen_footsteps():
    """1.5s of rapid footsteps (5 steps)."""
    dur = 1.5
    n = int(SAMPLE_RATE * dur)
    result = np.zeros(n, dtype=np.float32)
    rng = np.random.RandomState(55)

    for i in range(5):
        t_step = 0.1 + i * 0.25 + rng.uniform(-0.02, 0.02)
        idx = int(t_step * SAMPLE_RATE)
        step_len = int(0.04 * SAMPLE_RATE)
        if idx + step_len < n:
            step = rng.randn(step_len).astype(np.float32)
            step = _bandpass(step, 100, 3000) if step_len > 20 else step
            step *= np.exp(-np.linspace(0, 10, step_len))
            step *= rng.uniform(0.4, 0.7)
            result[idx:idx + step_len] += step

    return _to_wav_bytes(result)


def _gen_wind_rush():
    """8s of wind with volume ramp up then down."""
    dur = 8.0
    n = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, n, endpoint=False).astype(np.float32)

    wind = _pink_noise(n)
    wind = _bandpass(wind, 100, 3000)

    # Volume envelope: ramp up for 4s, then ramp down
    env = np.zeros(n, dtype=np.float32)
    mid = n // 2
    env[:mid] = np.linspace(0.1, 0.8, mid)
    env[mid:] = np.linspace(0.8, 0.2, n - mid)

    # Add some gusts
    rng = np.random.RandomState(99)
    for _ in range(6):
        gust_pos = int(rng.uniform(0.5, 7.0) * SAMPLE_RATE)
        gust_len = int(rng.uniform(0.3, 0.8) * SAMPLE_RATE)
        if gust_pos + gust_len < n:
            gust_env = np.sin(np.linspace(0, np.pi, gust_len)) * 0.3
            env[gust_pos:gust_pos + gust_len] += gust_env

    result = wind * env
    return _to_wav_bytes(result)


def _gen_parachute_pop():
    """0.4s fabric snap."""
    dur = 0.4
    n = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, n, endpoint=False).astype(np.float32)

    # Sharp noise burst
    snap = _bandpass(_noise(n), 500, 5000)
    env = np.exp(-t * 15) * (1 - np.exp(-t * 100))
    # Add a slight tonal pop
    pop = np.sin(2 * np.pi * 300 * t) * np.exp(-t * 20) * 0.3
    result = snap * env * 0.7 + pop
    return _to_wav_bytes(result)


def _gen_fabric_flap():
    """3s of rhythmic fabric flapping."""
    dur = 3.0
    n = int(SAMPLE_RATE * dur)
    result = np.zeros(n, dtype=np.float32)
    rng = np.random.RandomState(66)

    # Rhythmic soft noise pulses
    flap_interval = 0.4
    t_flap = 0.0
    while t_flap < dur:
        idx = int(t_flap * SAMPLE_RATE)
        flap_len = int(0.08 * SAMPLE_RATE)
        if idx + flap_len < n:
            flap = _bandpass(rng.randn(flap_len).astype(np.float32), 200, 2000)
            flap *= np.sin(np.linspace(0, np.pi, flap_len))  # smooth envelope
            flap *= rng.uniform(0.2, 0.4)
            result[idx:idx + flap_len] += flap
        t_flap += flap_interval + rng.uniform(-0.05, 0.05)

    # Add soft continuous wind
    wind = _pink_noise(n)
    wind = _bandpass(wind, 100, 1500) * 0.08
    result += wind

    return _to_wav_bytes(result)


def _gen_landing_thud():
    """0.3s low-frequency impact."""
    dur = 0.3
    n = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, n, endpoint=False).astype(np.float32)

    # Low sine thump
    thud = np.sin(2 * np.pi * 80 * t) * np.exp(-t * 15)
    # Noise impact
    impact = _noise(n) * np.exp(-t * 25) * 0.3
    # Filtered
    result = thud * 0.7 + _bandpass(impact, 50, 500) * 0.3
    # Very fast attack
    attack = np.ones(n, dtype=np.float32)
    a_len = int(0.003 * SAMPLE_RATE)
    attack[:a_len] = np.linspace(0, 1, a_len)
    result *= attack
    return _to_wav_bytes(result)


def _gen_siren_distant():
    """3s oscillating siren tone, distant."""
    dur = 3.0
    n = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, n, endpoint=False).astype(np.float32)

    # Oscillating frequency between 600-900Hz
    freq = 750 + 150 * np.sin(2 * np.pi * 1.5 * t)  # 1.5 Hz wobble
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    siren = np.sin(phase) * 0.3

    # Add slight reverb (simple delay)
    delay_samples = int(0.05 * SAMPLE_RATE)
    reverb = np.zeros(n, dtype=np.float32)
    reverb[delay_samples:] = siren[:-delay_samples] * 0.3
    result = siren + reverb

    # Gentle envelope
    env = _envelope(t, attack=0.3, release=0.5)
    # Make it distant (low volume, slight filter)
    result = _bandpass(result * env, 400, 2000) * 0.25

    return _to_wav_bytes(result)


# ============================================================
# MAIN
# ============================================================

def generate_all_sounds():
    """Return a dict of {sound_name: wav_bytes}."""
    return {
        "typing-loop": _gen_typing_loop(),
        "chatter-loop": _gen_chatter_loop(),
        "office-hum": _gen_office_hum(),
        "explosion": _gen_explosion(),
        "glass-shatter": _gen_glass_shatter(),
        "gasp": _gen_gasp(),
        "footsteps": _gen_footsteps(),
        "wind-rush": _gen_wind_rush(),
        "parachute-pop": _gen_parachute_pop(),
        "fabric-flap": _gen_fabric_flap(),
        "landing-thud": _gen_landing_thud(),
        "siren-distant": _gen_siren_distant(),
    }


if __name__ == "__main__":
    sounds = generate_all_sounds()
    total = 0
    for name, data in sounds.items():
        print(f"  {name}: {len(data)} bytes")
        total += len(data)
    print(f"Total: {total} bytes ({total / 1024:.1f} KB)")
