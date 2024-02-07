import random
import webbrowser
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# Karşılama mesajları
greetings = ["Merhaba!", "Selam!", "Nasılsınız?", "Size nasıl yardımcı olabilirim?"]

# Fonksiyonlar
def assist(user_input):
    if "merhaba" in user_input.lower():
        return random.choice(greetings)
    elif "teşekkür" in user_input.lower():
        return "Rica ederim!"
    elif "nasılsın" in user_input.lower():
        return "Ben sadece bir programım, ancak işler yolunda, teşekkür ederim! Siz nasılsınız?"
    elif "yardım" in user_input.lower():
        return "Nasıl yardımcı olabilirim?"
    elif "youtube aç" in user_input.lower():
        video_name = user_input[len("youtube aç") + 1:]  # 'youtube aç' ifadesini çıkarıp geri kalanı al
        youtube_search_url = f"https://www.youtube.com/results?search_query={video_name}"
        webbrowser.open(youtube_search_url)
        return f"{video_name} için YouTube araması yapılıyor..."
    elif "ara" in user_input.lower():
        search_query = user_input[len("ara") + 1:]  # 'ara' ifadesini çıkarıp geri kalanı al
        search_url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(search_url)
        return f"'{search_query}' için web araması yapılıyor..."
    elif "topla" in user_input.lower():
        numbers = [int(word) for word in user_input.split() if word.isdigit()]
        if len(numbers) != 2:
            return "Lütfen iki sayı girin."
        return f"{numbers[0]} ile {numbers[1]} toplamı {numbers[0] + numbers[1]}"
    elif "çarp" in user_input.lower():
        numbers = [int(word) for word in user_input.split() if word.isdigit()]
        if len(numbers) != 2:
            return "Lütfen iki sayı girin."
        return f"{numbers[0]} ile {numbers[1]} çarpımı {numbers[0] * numbers[1]}"
    elif "enes" in user_input.lower():
        return "Kral Enes, selam!"
    else:
        return "Üzgünüm, bunu anlayamadım. Başka bir şey denemek ister misiniz?"

# Etkileşim yöntemi
def select_interaction_method():
    while True:
        choice = input("Etkileşim yöntemini seçin (yazı/ses): ").lower()
        if choice == "yazı" or choice == "ses":
            return choice
        else:
            print("Geçersiz seçim. Lütfen 'yazı' veya 'ses' olarak seçin.")

# ses girişini almak için
def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dinleniyor...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Ses tanınmaya çalışılıyor...")
            text = recognizer.recognize_google(audio, language="tr-TR")  # Türkçe sesi tanıma
            return text.lower()
        except sr.UnknownValueError:
            return "Üzgünüm, anlayamadım."
        except sr.RequestError as e:
            return f"Bağlantı hatası: {e}"

# sesli yanıtını oluşturmak için
def generate_response_text(user_input):
    return assist(user_input)

# asistanın sesli yanıtını çalıştırmak için
def speak(text):
    tts = gTTS(text=text, lang='tr')
    tts.save("response.mp3")
    playsound("response.mp3")

# etkileşim
interaction_method = select_interaction_method()
while True:
    if interaction_method == "yazı":
        user_input = input("Soru veya komutunuzu girin: ")
        if "ses" in user_input.lower():
            interaction_method = "ses"
            print("Sesli etkileşim moduna geçildi.")
            continue
    elif interaction_method == "ses":
        user_input = get_audio()
        if "yazı" in user_input.lower():
            interaction_method = "yazı"
            print("Yazılı etkileşim moduna geçildi.")
            continue
    else:
        print("Geçersiz etkileşim yöntemi.")
        break

    print("Kullanıcı: ", user_input)
    response_text = generate_response_text(user_input)
    print("Asistan: ", response_text)
    speak(response_text)
    if "kapat" in user_input.lower():
        print("Program sonlandırılıyor...")
        break

# github.com/wyltre
