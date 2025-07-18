import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import io

st.set_page_config(page_title="Klasterisasi Pelanggan Mall", layout="centered")

st.title("🛍️ Klasterisasi Pelanggan Mall 🛍️")
st.write("Klasterisasi berdasarkan **Usia** dan **Pengeluaran Bulanan** menggunakan **Algoritma K-Means**")

# Upload file Excel
uploaded_file = st.file_uploader("📤 Upload file Excel (.xlsx)", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("📊 Data Awal")
    st.dataframe(df.head())

    if 'Usia (17 - 50)' in df.columns and 'Pengeluaran Bulanan' in df.columns:
        data = df[['Usia (17 - 50)', 'Pengeluaran Bulanan']]
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)

        # Elbow Method
        st.subheader("📈 Elbow Method - Menentukan Jumlah Klaster Optimal")
        inertias = []
        K = range(1, 11)
        for k in K:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(scaled_data)
            inertias.append(kmeans.inertia_)

        fig_elbow, ax_elbow = plt.subplots()
        ax_elbow.plot(K, inertias, 'bo-')
        ax_elbow.set_xlabel('Jumlah Klaster (k)')
        ax_elbow.set_ylabel('Inertia')
        ax_elbow.set_title('Metode Elbow')
        st.pyplot(fig_elbow)

        # Pilih jumlah klaster
        st.subheader("🔢 Pilih Jumlah Klaster (k)")
        n_clusters = st.slider("Pilih jumlah klaster berdasarkan grafik Elbow di atas", min_value=2, max_value=10, value=3)

        # KMeans Clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['Cluster'] = kmeans.fit_predict(scaled_data)

        # Visualisasi Klaster
        st.subheader("🧩 Visualisasi Klaster")
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'brown', 'pink', 'gray', 'olive']
        for i in range(n_clusters):
            cluster = df[df['Cluster'] == i]
            ax.scatter(cluster['Usia (17 - 50)'], cluster['Pengeluaran Bulanan'],
                       label=f"Klaster {i}", color=colors[i % len(colors)], s=80)
        ax.set_xlabel("Usia")
        ax.set_ylabel("Pengeluaran Bulanan")
        ax.set_title("Scatter Plot Klaster Pelanggan")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # Tabel hasil klasterisasi
        st.subheader("📄 Tabel Hasil Klasterisasi")
        st.dataframe(df)

        # Ringkasan Klaster
        st.subheader("📌 Ringkasan Tiap Klaster")
        summary = df.groupby('Cluster')[['Usia (17 - 50)', 'Pengeluaran Bulanan']].mean().round(2)
        summary['Jumlah Anggota'] = df['Cluster'].value_counts().sort_index()
        st.dataframe(summary)

        # Download hasil
        @st.cache_data
        def convert_df_to_excel(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Klasterisasi')
            return output.getvalue()

        st.download_button(
            label="⬇️ Download Hasil Klasterisasi",
            data=convert_df_to_excel(df),
            file_name='hasil_klasterisasi.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        st.error("⚠️ File tidak mengandung kolom 'Usia (17 - 50)' dan 'Pengeluaran Bulanan'.")
else:
    st.info("Silakan unggah file Excel berisi data pelanggan.")
