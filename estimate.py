"""实验1：数制转换与存储容量估算。"""
# 数字媒体1班 黄偌宸 2025310543
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("实验1：数制转换与存储容量估算")
print("1 B = 8 bit；1 MB = 10^6 B；1 MiB = 2^20 B")
print("1 GB = 10^9 B；1 GiB = 2^30 B")

print("\n一、数制转换")
decimal_value = int("10110101", 2)
print("10110101₂ = 1×2^7 + 0×2^6 + 1×2^5 + 1×2^4")
print("            + 0×2^3 + 1×2^2 + 0×2^1 + 1×2^0")
print(f"          = 128 + 32 + 16 + 4 + 1 = {decimal_value}")
print(f'int("10110101", 2) = {decimal_value}')
print(f"255 ÷ 16 = 15 余 15；hex(255) = {hex(255)}，即 FF₁₆")
from_hex = int("1A", 16)
binary_value = bin(from_hex)
eight_bits = format(from_hex, "08b")
print(f'1A₁₆ = 1×16 + 10 = {from_hex}；bin(int("1A", 16)) = {binary_value}')
print(f"补足8位：{eight_bits}，按四位分组为 0001 1010")
print(f'int("11010", 2) = {int("11010", 2)}；int("00011010", 2) = {int(eight_bits, 2)}')
print(f"补零前后数值相等：{int(binary_value, 2) == int(eight_bits, 2)}")

print("\n二、存储容量估算")
# 未压缩照片：宽 × 高 × 每像素位数 ÷ 8。
photo_bytes = 1920 * 1080 * 24 // 8
print(f"照片：1920 × 1080 × 24 ÷ 8 = {photo_bytes:,} B")
print(f"     = {photo_bytes / 10**6:.6f} MB = {photo_bytes / 2**20:.6f} MiB")

# 未压缩 PCM 音频：秒数 × 采样率 × 采样位深 × 声道数 ÷ 8。
audio_bytes = 4 * 60 * 44100 * 16 * 2 // 8
print(f"歌曲：240 × 44,100 × 16 × 2 ÷ 8 = {audio_bytes:,} B")
print(f"     = {audio_bytes / 10**6:.6f} MB = {audio_bytes / 2**20:.6f} MiB")

# 电影按8 Mbps为总平均码率估算，忽略封装开销。
movie_bytes = 2 * 3600 * 8 * 10**6 // 8
print(f"电影：7,200 × 8,000,000 ÷ 8 = {movie_bytes:,} B")
print(f"     = {movie_bytes / 10**9:.6f} GB = {movie_bytes / 2**30:.6f} GiB")
print("照片、音频结果不含文件头；电影若仅给出视频码率，还需另计音频。")

print("\n三、手机截图核对")
# 本次JPEG截图已核对为1272×2772像素，按24位RGB估算。
width, height = 1272, 2772
image_path = Path(__file__).with_name("手机截图.jpg")
if image_path.is_file():
    file_bytes = image_path.stat().st_size
else:
    file_bytes = 369153
    print("未找到截图文件，采用本次已记录的369,153字节复算。")
raw_bytes = width * height * 24 // 8
ratio = file_bytes / raw_bytes
print(f"RGB数据量：{width} × {height} × 24 ÷ 8 = {raw_bytes:,} B")
print(f"         = {raw_bytes / 10**6:.6f} MB = {raw_bytes / 2**20:.6f} MiB")
print(f"JPEG文件：{file_bytes:,} B = {file_bytes / 10**3:.3f} KB")
print(f"         = {file_bytes / 2**10:.6f} KiB = {file_bytes / 10**6:.6f} MB")
print(f"实际文件占RGB数据量的 {ratio:.4%}，相对减少 {1 - ratio:.4%}。")
print("文件大小差异与JPEG压缩、文件头等因素有关。")

print("\n四、拓展：256 GB手机的照片容量")
# 每张2 MB为估计值，不是实拍测量；20%为示例预留比例。
storage_bytes = 256 * 10**9
average_photo_bytes = 2 * 10**6
count = storage_bytes // average_photo_bytes
reserved_count = storage_bytes * 80 // 100 // average_photo_bytes
print("照片平均2 MB为估计值，非实测；按十进制单位，256 GB = 256,000 MB。")
print(f"理论数量：256,000 ÷ 2 = {count:,} 张")
print(f"预留20%空间的示例：256,000 × 80% ÷ 2 = {reserved_count:,} 张")
print("实际数量取决于可用空间和照片大小，减小文件时也需要考虑画质。")
