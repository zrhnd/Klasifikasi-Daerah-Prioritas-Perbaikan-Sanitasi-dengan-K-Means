# =================================================================
# 1. Memasukkan Library yang dibutuhkan
# =================================================================
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans

# =================================================================
# 2. Persiapan Data
# =================================================================
# Data: [Sanitasi Layak, BAB Sendiri, Air Minum Layak]
data = np.array([
    [77.55, 80.38, 88.79], [82.02, 88.91, 90.89], [68.68, 79.04, 83.40],
    [83.64, 92.30, 89.76], [80.36, 87.90, 79.70], [77.29, 82.81, 84.70],
    [79.81, 88.62, 67.39], [83.89, 91.92, 80.20], [92.24, 92.46, 73.40],
    [91.62, 94.55, 90.83], [95.17, 86.46, 99.86], [71.66, 86.16, 93.24],
    [83.28, 88.66, 93.62], [97.12, 83.80, 95.69], [80.97, 83.80, 95.02],
    [82.89, 88.04, 93.51], [95.95, 85.95, 97.56], [82.85, 73.32, 94.60],
    [73.36, 79.20, 85.40], [78.39, 84.50, 78.76], [73.77, 84.60, 77.05],
    [81.43, 87.24, 76.40], [89.77, 93.53, 85.80], [79.80, 92.44, 86.80],
    [84.85, 81.86, 91.65], [76.06, 76.90, 88.51], [91.57, 88.62, 91.18],
    [85.62, 85.64, 91.94], [78.58, 67.43, 94.57], [80.12, 77.96, 78.35],
    [76.77, 72.87, 93.21], [77.11, 69.73, 88.66], [40.81, 63.34, 64.92],
    [77.89, 75.48, 81.68]
])

provinsi = [
    "Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Jambi", "Sumatera Selatan", 
    "Bengkulu", "Lampung", "Bangka Belitung", "Kepulauan Riau", "DKI Jakarta", 
    "Jawa Barat", "Jawa Tengah", "DI Yogyakarta", "Jawa Timur", "Banten", "Bali", 
    "NTB", "NTT", "Kalimantan Barat", "Kalimantan Tengah", "Kalimantan Selatan", 
    "Kalimantan Timur", "Kalimantan Utara", "Sulawesi Utara", "Sulawesi Tengah", 
    "Sulawesi Selatan", "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat", 
    "Maluku", "Maluku Utara", "Papua", "Papua Barat"
]

# =================================================================
# 3. Permodelan K-Means
# =================================================================
K = 3
kmeans = KMeans(n_clusters=K, init='k-means++', n_init=10, random_state=42)
kmeans.fit(data)

labels = kmeans.predict(data)
centroids = kmeans.cluster_centers_

# Mapping kategori berdasarkan rata-rata nilai (Urutan: Tinggi ke Rendah)
centroid_sums = centroids.sum(axis=1)
sorted_indices = np.argsort(centroid_sums)[::-1]
cluster_map = {sorted_indices[0]: "Baik", sorted_indices[1]: "Cukup", sorted_indices[2]: "Darurat"}
kategori = [cluster_map[label] for label in labels]

# =================================================================
# 4. Pengolahan DataFrame
# =================================================================
df = pd.DataFrame(data, columns=["Sanitasi Layak", "Tempat BAB Sendiri", "Air Minum Layak"])
df["Provinsi"] = provinsi
df["Cluster"] = labels
df["Kategori"] = kategori

df["Kategori"] = pd.Categorical(df["Kategori"], categories=["Baik", "Cukup", "Darurat"], ordered=True)
df_sorted = df.sort_values(by="Kategori")

# Cetak hasil di konsol
print("\n=== Centroid Akhir Untuk Setiap Cluster ===")
print(pd.DataFrame(centroids, columns=["Sanitasi Layak", "Tempat BAB Sendiri", "Air Minum Layak"]))
print("\n=== Hasil Pengelompokan Provinsi ===")
print(df_sorted[["Provinsi", "Kategori"]].to_string(index=False))

# =================================================================
# 5. Visualisasi Interaktif (Plotly 3D)
# =================================================================
fig = go.Figure()

# Plot titik data berdasarkan kategori
colors = {"Baik": "green", "Cukup": "orange", "Darurat": "red"}
for kat in ["Baik", "Cukup", "Darurat"]:
    cluster_data = df[df["Kategori"] == kat]
    fig.add_trace(go.Scatter3d(
        x=cluster_data["Sanitasi Layak"],
        y=cluster_data["Tempat BAB Sendiri"],
        z=cluster_data["Air Minum Layak"],
        mode='markers+text',
        marker=dict(size=6, color=colors[kat]),
        text=cluster_data["Provinsi"],
        textposition="top center",
        name=kat
    ))

# Plot titik centroid
fig.add_trace(go.Scatter3d(
    x=centroids[:, 0],
    y=centroids[:, 1],
    z=centroids[:, 2],
    mode='markers',
    marker=dict(size=10, color='black', symbol='diamond-open'),
    name="Centroid"
))

# Layout setting
fig.update_layout(
    title="Clustering K-Means: Akses Sanitasi & Air Minum Layak",
    scene=dict(
        xaxis_title='Sanitasi Layak (%)',
        yaxis_title='BAB Sendiri (%)',
        zaxis_title='Air Minum Layak (%)',
    ),
    margin=dict(l=0, r=0, b=0, t=40) # Mengoptimalkan tampilan di Colab
)

# Tampilkan langsung di Google Colab
fig.show()
