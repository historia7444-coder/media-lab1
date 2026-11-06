"""实验二：估算 128B 对话模型的容量，比较三种主机的价格和性能。"""

# 2026-11-06 美国税前报价，换算时按 1 美元 = 7 元。
parts_usd = {
    "RTX 5090 Founders Edition": 1999.99,
    "Ryzen 9 9900X": 439.00,
    "ProArt X870E-Creator WiFi": 509.99,
    "Kingston FURY Beast 2×64 GB": 2149.99,
    "Kingston NV3 2 TB": 295.99,
    "Corsair RM1200e": 234.99,
    "LANCOOL III RGB": 159.99,
    "Phantom Spirit 120 SE": 54.99,
}
yuan_per_dollar = 7

print("128B 模型权重")
parameters = 128 * 10**9
for precision, bits in [("FP16", 16), ("INT8", 8), ("INT4", 4)]:
    weight_bytes = parameters * bits / 8
    print(f"{precision}: {weight_bytes / 10**9:.0f} GB，约 {weight_bytes / 2**30:.1f} GiB")

# 32K 上下文，每路 KV 缓存按 2–4 GB，运行缓冲另留 4 GB。
int4_gb = parameters * 4 / 8 / 10**9
for requests in [1, 2]:
    kv_min, kv_max = 2 * requests, 4 * requests
    total_gb = int4_gb + kv_max + 4
    print(f"{requests} 路：KV 缓存 {kv_min}–{kv_max} GB，按上限合计约 {total_gb:.0f} GB")

single_usd = sum(parts_usd.values())
spark_usd = 6949.99
# 双卡沿用单卡配置，再加一张 5090，并将电源换为 1600 W 的 MSI Ai1600T。
dual_usd = single_usd + parts_usd["RTX 5090 Founders Edition"] - parts_usd["Corsair RM1200e"] + 769.99

print("\n单卡配置（美元）")
for part, price in parts_usd.items():
    print(f"{part}: {price:,.2f}")
print(f"合计：{single_usd:,.2f}")

# 32K 单路解码。每个词元假设读 3 GB 活跃权重，单步耗时等于各侧读时加额外开销。
ram_gb_s, vram_gb_s = 45, 900
single_seconds = 1.8 / ram_gb_s + 1.2 / vram_gb_s + 0.005
spark_seconds = 3 / 190 + 0.009
dual_seconds = 0.6 / ram_gb_s + 2.4 / vram_gb_s + 0.008

# 5 秒有声视频，FastH3 Trim、8 步、预热后耗时，依次为 480p 和 768p。
# FastVideo 团队公开数据：https://haoailab.com/blogs/fasth3-rtx/
# 双卡方案只用一张卡生成单条短片，沿用单卡参照值。
video_5090 = (13.4, 35.4)
video_spark = (125.8, 340.1)
plans = [
    ("单 RTX 5090", single_usd, single_seconds, video_5090),
    ("DGX Spark", spark_usd, spark_seconds, video_spark),
    ("双 RTX 5090", dual_usd, dual_seconds, video_5090),
]

print("\n三方案对比")
for name, price_usd, seconds_per_token, video_times in plans:
    cost_yuan = price_usd * yuan_per_dollar
    # 与报告表 2 一致，先将估算出词速度取整，再计算每万元的速度。
    tokens_per_second = round(1 / seconds_per_token)
    speed_per_10000 = tokens_per_second / (cost_yuan / 10000)
    print(f"{name}：{cost_yuan:,.0f} 元，估算 {tokens_per_second} tok/s，"
          f"每万元 {speed_per_10000:.1f} tok/s，"
          f"视频参考耗时 {video_times[0]} / {video_times[1]} 秒")
