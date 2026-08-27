import joblib
import pandas as pd
import streamlit as st

# 1. Memuat model terbaik (.pkl) yang akan di training
model = joblib.load('model_obesitas_terbaik.pkl')

# Konfigurasi Halaman Web
st.title('Sistem Peringatan Dini Resiko Obesitas (Puskesmas)')
st.write(
    'Aplikasi berbasis AI ini dirancang untuk membantu tenaga medis puskesmas'
    'dalam memprediksi tingkat kategori obesitas pasien berdsarkan ukuran tubuh '
    'dan kebiasaan gaya hidup'
)      

# 2. Membuat Formulir Input Data Pasien
with st.form('form_obesitas'):
  st.subheader('Masukkan Data & Kebiasaan Pasien')

  col1, col2 = st.columns(2)
  with col1:
    age = st.number_input('Umur', min_value = 1, max_value = 120, value = 22)
    gender = st.selectbox('Jenis Kelamin', ['Female','Male'])
    height = st.number_input('Tinggi Badan', min_value=1.0, max_value=2.5, value=1.7)
    weight = st.number_input('Berat Badan', min_value=10, max_value = 300, value = 70)
    family_history = st.selectbox('Riwayat Obesitas dalam Keluarga?', ['yes', 'no'])
    favc = st.selectbox('Sering Mengonsumsi Makanan Tinggi Kalori', ['yes', 'no'])
    faf = st.slider('Frekuensi Olahraga per Minggu (0-3)',min_value=0,max_value=3,value=1)

    submit_button = st.form_submit_button('Prediksi Risiko')

# 3. Proses Hasil Prediksi
if submit_button:
  input_data = pd.DataFrame({
      'Gender': [gender],
      'Age': [age],
      'Height': [height],
      'Weight': [weight],
      'family_history_with_overweight': [family_history], 
      'FAVC': [favc],
      'FCVC': [2.0],
      'NCP': [3.0],
      'CAEC': ['Sometimes'],
      'SMOKE': ['no'],
      'CH2O': [2.0],
      'SCC': ['no'],
      'FAF': [faf],
      'TUE': [1.0],
      'CALC': ['Sometimes'],
      'MTRANS': ['Public_Transportation'],
  })

  # Prediksi Menggunakan Model
  hasil = model.predict(input_data) [0]

  st.markdown('----')
  st.subheader('Hasil Diagnosis Sistem:')

  if 'Normal' in hasil:
    st.success(f'✅ **Hasil Normal: Pasien berada dalam kategori {hasil}.'
    ' Pertahankan pola hidup sehat!')
  elif 'Insufficient' in hasil:
    st.warning(f'Perhatian: Pasien terdeteksi {hasil} (Kekurangan berat'
        ' badan). Perlu peningkatan gizi seimbang.')
  elif 'Overweight' in hasil:
    st.error(f'Peringatan Dini:Pasien terdeteksi {hasil}. Disarankan'
        ' untuk mulai mengatur pola makan dan aktivitas fisik.'
    )
  else: # Untuk Obesity type I, II dan III
    st.error(f'Risiko Tinggi:Pasien terdeteksi masuk dalam kategori'
        f'{hasil}. Segera lakukan konseling kesehatan di Puskesmas!')


