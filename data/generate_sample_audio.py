"""
data/generate_sample_audio.py
Generates a sample synthetic .wav file for testing VBCUA without a real recording.

Run with: python data/generate_sample_audio.py
"""

import numpy as np
import wave
import struct
import os


def generate_sample_audio(output_path: str = "assets/audio/sample_explanation.wav",
                           duration: float = 20.0, sr: int = 22050):
    """Generate a synthetic speech-like waveform (sine sweeps + noise envelope)."""
    t = np.linspace(0, duration, int(sr * duration))

    # Simulate speech-like amplitude envelope with pauses
    envelope = np.ones_like(t)
    pause_zones = [(3, 3.5), (8, 8.7), (14, 14.4)]
    for start, end in pause_zones:
        envelope[(t >= start) & (t <= end)] *= 0.05

    # Mix a few "formant-like" frequencies with amplitude modulation
    signal = (
        0.3 * np.sin(2 * np.pi * 150 * t) +
        0.2 * np.sin(2 * np.pi * 300 * t) +
        0.15 * np.sin(2 * np.pi * 600 * t)
    )
    signal *= envelope
    signal += np.random.normal(0, 0.02, len(t))  # slight noise

    # Normalize
    signal = signal / np.max(np.abs(signal)) * 0.7

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with wave.open(output_path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        pcm = (signal * 32767).astype(np.int16)
        wf.writeframes(pcm.tobytes())

    print(f"✅ Sample audio generated at: {output_path} ({duration}s, {sr}Hz)")


if __name__ == "__main__":
    generate_sample_audio()
