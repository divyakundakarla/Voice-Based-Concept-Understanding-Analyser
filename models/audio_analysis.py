"""
models/audio_analysis.py
Audio signal processing and fluency analysis using Librosa.
"""

import numpy as np


def analyze_audio(audio_path: str) -> dict:
    """
    Perform comprehensive audio analysis on a file.

    Args:
        audio_path: Path to audio file

    Returns:
        dict with waveform, duration, rms_energy, pause_ratio, speech_rate_category, confidence
    """
    try:
        import librosa
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        return _compute_features(y, sr)
    except ImportError:
        return _dummy_audio_features()
    except Exception as e:
        return {"error": str(e), "success": False}


def _compute_features(y: np.ndarray, sr: int) -> dict:
    """Extract audio features from waveform array."""
    import librosa

    duration = librosa.get_duration(y=y, sr=sr)

    # RMS energy (volume indicator)
    rms = librosa.feature.rms(y=y)[0]
    rms_mean = float(np.mean(rms))
    rms_db = float(librosa.amplitude_to_db(np.array([rms_mean]))[0])

    # Silence / pause detection
    silence_threshold = rms_mean * 0.15
    is_silent = rms < silence_threshold
    pause_ratio = float(np.sum(is_silent) / len(is_silent))

    # Zero-crossing rate (clarity proxy)
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    zcr_mean = float(np.mean(zcr))

    # Spectral centroid (brightness)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    sc_mean = float(np.mean(spectral_centroid))

    # MFCC features (voice quality)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = float(np.mean(np.abs(mfcc)))

    # Confidence score derived from signal features
    confidence = _compute_confidence(rms_mean, pause_ratio, zcr_mean)

    # Waveform downsampled for display
    target_points = 2000
    if len(y) > target_points:
        step = len(y) // target_points
        waveform_display = y[::step][:target_points]
    else:
        waveform_display = y

    # Time axis for waveform display
    times = np.linspace(0, duration, len(waveform_display))

    return {
        "success": True,
        "duration": round(duration, 2),
        "sample_rate": sr,
        "rms_energy": round(rms_mean, 6),
        "rms_db": round(rms_db, 2),
        "pause_ratio": round(pause_ratio, 3),
        "zcr_mean": round(zcr_mean, 6),
        "spectral_centroid": round(sc_mean, 2),
        "mfcc_mean": round(mfcc_mean, 4),
        "confidence": round(confidence, 3),
        "waveform": waveform_display.tolist(),
        "waveform_times": times.tolist(),
        "error": None
    }


def _compute_confidence(rms: float, pause_ratio: float, zcr: float) -> float:
    """
    Heuristic confidence score (0–1) based on audio features.
    High RMS + low pauses + moderate ZCR → high confidence.
    """
    rms_score = min(rms / 0.05, 1.0)          # normalize against typical voice RMS
    pause_score = max(0, 1 - pause_ratio * 2)   # less pauses = better
    zcr_score = 1 - min(zcr / 0.3, 1.0)        # lower ZCR often = clearer speech

    confidence = 0.5 * rms_score + 0.35 * pause_score + 0.15 * zcr_score
    return float(np.clip(confidence, 0.0, 1.0))


def _dummy_audio_features() -> dict:
    """Fallback dummy features when librosa is unavailable."""
    t = np.linspace(0, 30, 2000)
    waveform = np.sin(2 * np.pi * 3 * t) * np.random.uniform(0.3, 0.8, 2000)
    return {
        "success": True,
        "duration": 30.0,
        "sample_rate": 22050,
        "rms_energy": 0.025,
        "rms_db": -32.0,
        "pause_ratio": 0.18,
        "zcr_mean": 0.05,
        "spectral_centroid": 1800.0,
        "mfcc_mean": 12.4,
        "confidence": 0.72,
        "waveform": waveform.tolist(),
        "waveform_times": t.tolist(),
        "error": "Demo mode — librosa not available"
    }


def compute_fluency_score(filler_count: int, pause_ratio: float,
                           speech_rate_wpm: float, confidence: float) -> float:
    """
    Compute fluency score (0–100) from multiple speech signals.

    Weights:
      filler penalty  25%
      pause score     25%
      speech rate     25%
      confidence      25%
    """
    # Filler penalty: 0 fillers = 1.0, 10+ fillers = 0.0
    filler_score = max(0.0, 1.0 - filler_count / 10.0)

    # Pause score: ideal pause_ratio ~0.1–0.25
    if pause_ratio <= 0.25:
        pause_score = 1.0 - (pause_ratio / 0.5)
    else:
        pause_score = max(0, 1.0 - pause_ratio)

    # Speech rate: ideal 120–160 wpm
    if 120 <= speech_rate_wpm <= 160:
        rate_score = 1.0
    elif speech_rate_wpm < 120:
        rate_score = max(0, speech_rate_wpm / 120)
    else:
        rate_score = max(0, 1 - (speech_rate_wpm - 160) / 80)

    fluency = (filler_score * 0.25 + pause_score * 0.25 +
               rate_score * 0.25 + confidence * 0.25) * 100
    return round(float(np.clip(fluency, 0, 100)), 1)
