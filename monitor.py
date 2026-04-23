import google.generativeai as genai
import requests
import subprocess
import os

# --- KONFIGURASI API ---
# Masukkan API Key yang sudah Anda generate sebelumnya
GEMINI_API_KEY = "AIzaSyBMwv8aB9UDJfixhq8z7mNgiZk--gq3eKY"
FONNTE_TOKEN = "SwdrcBh3z2HCs1EUczy9"
WHATSAPP_NUMBER = "085143733866" # Ganti dengan nomor tujuan

# Konfigurasi Gemini
genai.configure(api_key="AIzaSyBMwv8aB9UDJfixhq8z7mNgiZk--gq3eKY")
model = genai.GenerativeModel('gemini-2.0-flash')

def get_ssh_failed_logs():
    """Mengambil 10 baris terakhir percobaan login gagal dari auth.log"""
    try:
        # Command untuk mencari kata 'Failed password' di log SSH
        command = "sudo grep 'Failed password' /var/log/auth.log | tail -n 10"
        logs = subprocess.check_output(command, shell=True).decode('utf-8')
        return logs if logs else "Tidak ada percobaan login gagal yang terdeteksi."
    except Exception as e:
        return f"Error membaca log: {str(e)}"

def analyze_with_gemini(log_content):
    """Mengirim log ke Gemini AI untuk dianalisis"""
    prompt = f"""
    Saya adalah admin server Ubuntu. Berikut adalah log percobaan login gagal di server saya:
    {log_content}
    
    Tolong berikan analisis singkat:
    1. Apakah ini indikasi serangan brute-force?
    2. Apa rekomendasi keamanan yang harus saya lakukan?
    Berikan jawaban yang singkat dan padat untuk dikirim melalui WhatsApp.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analisis AI: {str(e)}"

def send_whatsapp_notification(message):
    """Mengirim pesan melalui Fonnte Gateway"""
    url = "https://api.fonnte.com/send"
    payload = {
        'target': WHATSAPP_NUMBER,
        'message': f"🚀 *Server Monitoring Alert*\n\n{message}",
        'countryCode': '62', # Kode negara Indonesia
    }
    headers = {
        'Authorization': FONNTE_TOKEN
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error mengirim WhatsApp: {str(e)}"

def main():
    print("Memulai pemindaian log...")
    
    # 1. Ambil Log
    logs = get_ssh_failed_logs()
    
    if "Tidak ada" in logs:
        print("Server Aman. Tidak ada aktivitas mencurigakan.")
        return

    # 2. Analisis dengan Gemini
    print("Menganalisis dengan Gemini AI...")
    analysis = analyze_with_gemini(logs)
    
    # 3. Kirim Alert
    print("Mengirim notifikasi ke WhatsApp...")
    status = send_whatsapp_notification(analysis)
    print("Selesai!", status)

if __name__ == "__main__":
    main()