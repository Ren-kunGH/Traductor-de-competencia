import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import deepl
import random  
import time

duration = 5  # Duration of recording in seconds
samplerate = 44100  # Sample rate in Hz
puntaje = 0 
error_count = 0
max_error = 5

palabras_por_nivel = {
    "facil": ["hola", "adiós", "gracias", "Por Favor", "Sí", "no"],
    "intermedio": ["felicidad", "tristeza", "amistad", "familia", "trabajo", "escuela"],
    "avanzado": ["desarrollo", "tecnología", "inteligencia", "sostenibilidad", "innovación", "colaboración"]
}

print("Bienvenido al juego de pronunciación!")
nivel = input("Elige un nivel de dificultad (facil, intermedio, avanzado): ").lower()
if nivel not in palabras_por_nivel:
    print("Nivel no válido. Se seleccionará 'facil' por defecto.")
    nivel = "facil"

seleccion_nivel = palabras_por_nivel[nivel]
random.shuffle(seleccion_nivel)  # Mezclar las palabras del nivel seleccionado
print(f"Nivel seleccionado: {nivel}. Comenzando el juego pronto... Tienes esta cantidad de errores permitidos: {max_error}.")
print("Veras una palabra en español, pronunciala en inglés. Tienes 5 segundos para pronunciarla. ¡Buena suerte!")
time.sleep(3)  # Wait for 3 seconds before starting the game

for palabra in seleccion_nivel:
    print(f"Palabra: {palabra}")
    print("Habla ahora...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    wav.write("resultado.wav", samplerate, recording)  # Save the recording as a WAV file
    print("Grabación finalizada. Procesando...")
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile("resultado.wav") as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language = "EN-US")
            auth_key = "35870bce-545f-4ac7-9aca-258b24149803:fx" # replace with your key
            deepl_client = deepl.DeepLClient(auth_key)
            result = deepl_client.translate_text(text, target_lang="EN-US")
            print("Tu has dicho:", text)
            print("Tu has dicho en ingles:", result)

            if text == result.text.lower():
                puntaje += 1
                print(f"¡Correcto! Tu puntaje actual es: {puntaje}")
            else:
                error_count += 1
                print(f"Incorrecto. Tu puntaje actual es: {puntaje}. Errores: {error_count}/{max_error}")
                if error_count >= max_error:
                    print("Has alcanzado el número máximo de errores. Fin del juego.")
                    break
    except sr.UnknownValueError:
        print("No se pudo entender el audio.")
    except sr.RequestError as e:
        print("Error del servicio de reconocimiento de voz; {0}".format(e))
print(f"Juego terminado. Tu puntaje final es: {puntaje}")

print("Puedes hablar ahora...")
recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
sd.wait()  # Wait until recording is finished
wav.write("resultado.wav", samplerate, recording)  # Save the recording as a WAV file   
print("Grabación finalizada. Procesando...")
recognizer = sr.Recognizer()
with sr.AudioFile("resultado.wav") as source:
    audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language='EN-US')
        auth_key = "35870bce-545f-4ac7-9aca-258b24149803:fx" # replace with your key
        deepl_client = deepl.DeepLClient(auth_key)
        idioma_destino = input("Introduce el idioma de destino (por ejemplo, EN para inglés, FR para francés): ")
        result = deepl_client.translate_text(text, target_lang=idioma_destino)
        print("Texto reconocido: " + text)
        print("Texto traducido: " + result.text)
    except sr.UnknownValueError:
        print("No se pudo entender el audio.")
    except sr.RequestError as e:
        print("Error al solicitar resultados; {0}".format(e))
    