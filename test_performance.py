"""
Performance Test - Stego Security System
Table 3.1: Recommended Acceptable Response Times
Run with: python test_performance.py
"""

import time
import io
import hashlib
from PIL import Image

THRESHOLDS = {
    "Text Classification":     {"ideal": 1.0, "max": 2.0},
    "Encryption":              {"ideal": 0.5, "max": 1.0},
    "Steganography Embedding": {"ideal": 3.0, "max": 5.0},
    "Extraction / Decryption": {"ideal": 2.0, "max": 3.0},
    "Password Validation":     {"ideal": 0.5, "max": 1.0},
}

results = []

def evaluate(name, elapsed):
    t = THRESHOLDS[name]
    if elapsed <= t["ideal"]:
        status = "PASS (Ideal)"
    elif elapsed <= t["max"]:
        status = "PASS (Acceptable)"
    else:
        status = "FAIL (Too Slow)"
    results.append((name, elapsed, t["ideal"], t["max"], status))
    print(f"  {status}  |  {elapsed:.5f} s  |  {name}")

print("=" * 65)
print("   Stego Security System — Performance Test (Table 3.1)")
print("=" * 65)

print("\n[1] Text Classification")
from classification import classify_message
times = []
for msg in ["Hello, how are you?", "Employee salary details for Q1", "Top secret nuclear launch codes"]:
    t0 = time.perf_counter()
    classify_message(msg)
    times.append(time.perf_counter() - t0)
evaluate("Text Classification", max(times))

print("\n[2] Encryption")
from encryption import encrypt
enc_times = []
for level, pwd in [("Public", None), ("Restricted", None), ("Confidential", "test123")]:
    t0 = time.perf_counter()
    encrypt("Top secret nuclear launch codes", level, password=pwd)
    enc_times.append(time.perf_counter() - t0)
evaluate("Encryption", max(enc_times))

print("\n[3] Steganography Embedding")
from steganography import embed_message
img = Image.new("RGB", (512, 512), color=(100, 150, 200))
buf = io.BytesIO()
img.save(buf, format="PNG")
embed_times = []
for level in ["Public", "Restricted", "Confidential"]:
    t0 = time.perf_counter()
    embed_message(io.BytesIO(buf.getvalue()), b"Test message", output_path=None, level=level)
    embed_times.append(time.perf_counter() - t0)
evaluate("Steganography Embedding", max(embed_times))

print("\n[4] Extraction / Decryption")
from steganography import extract_message
from encryption import decrypt
buf.seek(0)
stego_img = embed_message(io.BytesIO(buf.getvalue()), b"Extraction test", output_path=None, level="Public")
stego_buf = io.BytesIO()
stego_img.save(stego_buf, format="PNG")
t0 = time.perf_counter()
level_out, data_out = extract_message(io.BytesIO(stego_buf.getvalue()))
extract_time = time.perf_counter() - t0
enc_result = encrypt("Extraction test", "Restricted")
t1 = time.perf_counter()
decrypt({"data": enc_result["data"], "level": "Restricted"})
decrypt_time = time.perf_counter() - t1
evaluate("Extraction / Decryption", extract_time + decrypt_time)

print("\n[5] Password Validation")
stored_hash = hashlib.sha256("test123".encode()).hexdigest()
t0 = time.perf_counter()
for _ in range(100):
    hashlib.sha256("test123".encode()).hexdigest() == stored_hash
pwd_time = (time.perf_counter() - t0) / 100
evaluate("Password Validation", pwd_time)

print("\n" + "=" * 65)
print("   SUMMARY")
print("=" * 65)
print(f"{'Operation':<28} {'Actual':>10} {'Ideal':>8} {'Max':>6}  Result")
print("-" * 65)
for name, elapsed, ideal, max_t, status in results:
    icon = status.split()[0]
    print(f"{name:<28} {elapsed:>9.5f}s {ideal:>7.1f}s {max_t:>5.1f}s  {icon}")
passed = sum(1 for r in results if "FAIL" not in r[4])
print("-" * 65)
print(f"\n  Passed: {passed}/{len(results)}  |  Failed: {len(results)-passed}/{len(results)}")
print("=" * 65)