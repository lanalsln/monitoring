import google.generativeai as genai
import requests
import subprocess

# Masukkan API Key kamu di sini
GEMINI_KEY = "AIzaSyBMwv8aB9UDJfixhq8z7mNgiZk--gq3eKY"
FONNTE_TOKEN = "SwdrcBh3z2HCs1EUczy9"

# 1. Mengambil log SSH (Failed password)
# Gunakan command shell: tail -n 10 /var/log/auth.log | grep "Failed password"
logs = subprocess.check_output('tail -n 10 /var/log/auth.log', shell=True).decode('utf-8')

# 2. Analisis dengan Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')
response = model.generate_content(f"Analisis log berikut, apakah ada tanda serangan brute force? : {logs}")

# 3. Kirim ke WhatsApp via Fonnte
url = "https://api.fonnte.com/send"
data = {
    'target': '085143733866',
    'message': response.text
}
headers = {'Authorization': FONNTE_TOKEN}
requests.post(url, data=data, headers=headers)