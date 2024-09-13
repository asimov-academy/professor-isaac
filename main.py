import os
import io
import speech_recognition as sr
import base64
import pyaudio
import cv2 as cv

import threading
import keyboard
from time import sleep

from io import BytesIO
from PIL import Image
from openai import OpenAI

from faster_whisper import WhisperModel 
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class ProfessorISAAC:
    def __init__(self, wake_event):
        self.ai_name = 'Professor I.S.A.A.C.'
        self.historico_conversa = ''
        self.contexto = """
            Você é um professor extremamente qualificado e respeitado.
            Você sempre fala em português brasileiro.
            Nunca utilize símbolos ou equações; descreva todos os elementos, símbolos e operações matemáticas por extenso e em português brasileiro, utilizando palavras.
            Incentive o usuário a refletir sobre cada etapa do processo, fazendo perguntas para garantir a compreensão e guiá-lo de forma interativa.
            Se o usuário estiver no caminho certo, elogie e continue oferecendo orientações para que ele avance na solução.
            Explique como abordar e resolver o problema, passo a passo, sem entregar a solução final.
            Dê respostas curtas e objetivas, sempre buscando orientar o usuário.
        """
        self.wake_event = wake_event
        self.pergunta = ''
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.py_audio = pyaudio.PyAudio()
        self.player_stream = self.py_audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=24000,
            output=True,
            frames_per_buffer=1024,
        )
        self.stop_chat = False
        self.current_response_thread = None
        
        self.llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
        self.client = OpenAI()

        self.is_listening = False
        self.is_processing = False
        self.stop_flag = threading.Event()

    def encode_image(self):
        pil_image = Image.open('frames/last_frame.jpg')
        buffered = BytesIO()
        pil_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

    def frame_capture(self):
        if not os.path.exists('frames'):
            os.makedirs('frames')

        fps = 30
        cam_device = 'https://192.168.0.104:8080/video'
        # cam_device = 1
        cap = cv.VideoCapture(cam_device)
        cap.set(cv.CAP_PROP_FPS, fps)

        try:
            while not self.wake_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                img_pil = Image.fromarray(frame)
                buffer = io.BytesIO()
                img_pil.save(buffer, format="JPEG")

                image_path = 'frames/last_frame.jpg'
                img_pil.save(image_path)


        except Exception as e:
            print(f"Erro ao capturar frames: {e}")

        finally:
            cap.release()

    def formatar_pergunta(self, pergunta):
        print('Formatando pergunta...\n')
        try:
            encoded_image = self.encode_image()

            inputs = [
                [HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": f'{self.contexto}\n\nConversa atual:\n{self.historico_conversa}\n\nAluno: {pergunta}\nimagem: \n'
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                )],
            ]
            return inputs
        except Exception as e:
            print(f"Erro ao formatar pergunta: {e}")
            return None

    def obter_resposta(self, pergunta):
        print('Iniciando o processo de obter_resposta \n')
        input = self.formatar_pergunta(pergunta)

        try:
            answer = self.llm.stream(input[0])
            self.historico_conversa += f"Aluno: {pergunta}\n {self.ai_name}:\n"
            buffer = ""
            for resp in answer:
                if self.stop_flag.is_set():
                    print("Processo de obtenção de resposta interrompido.")
                    break
                buffer += resp.content
                while "." in buffer:
                    sentence, buffer = buffer.split(".", 1)
                    print(sentence, end=".", flush=True)
                    self.speak(sentence)
                    self.historico_conversa += f"{sentence}\n"

        except Exception as e:
            print(f"Erro durante a obtenção de resposta: {e}")

    def speak(self, text):
        try:
            with self.client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice="onyx",
                response_format="pcm",
                speed=1.3,
                input=text
            ) as response:
                silence_threshold = 0.01
                stream_start = False
                for chunk in response.iter_bytes(chunk_size=1024):
                    if self.stop_flag.is_set():
                        print("Processo de fala interrompido.")
                        break
                    if stream_start:
                        self.player_stream.write(chunk)
                    else:
                        if max(chunk) > silence_threshold:
                            self.player_stream.write(chunk)
                            stream_start = True
        except Exception as e:
            print(f"Erro durante a síntese de fala: {e}")

    def transcribe_audio(self, audio_data):
        model = WhisperModel("medium")
        audio_test = BytesIO(audio_data)
        clean_prompt = ''
        segments, _ = model.transcribe(audio=audio_test, language='pt', beam_size=5)
        for segment in segments:
            clean_prompt += segment.text
            print(f"{segment.text}")
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        return clean_prompt

    def hear(self):
        with self.microphone as source:
            print("Inicializando Microfone...")
            self.recognizer.adjust_for_ambient_noise(source)
            print("""
                Aperte 'V' para gravar.
                Aperte 'F' para obter resposta.
                Aperte 'Q' para encerrar.
            """)

            while not self.wake_event.is_set():
                self.audio = self.recognizer.listen(source)
                keyboard.add_hotkey('q', lambda: self.wake_event.set())
                print("escutando...")

                while self.is_listening == True:
                    if self.is_processing:
                        print('interrompendo resposta')
                        self.stop_current_processes()
                        self.is_processing = False
                        
                    audio_data = self.audio.get_wav_data()
                    buffer = self.transcribe_audio(audio_data)
                    self.pergunta += buffer
                    sleep(0.1)
                    print(buffer)

                    if 'professor' in self.pergunta.lower():
                        self.is_listening = False
                        self.stop_listening_and_get_response()

    def stop_current_processes(self):
        self.stop_flag.set()
        if self.is_processing:
            print("Interrompendo processos atuais.")
        self.is_processing = False
        self.stop_flag.clear()

    def start_listening(self):
        self.is_listening = True
        print("Iniciando gravação...")
        if self.is_processing == True:
            self.stop_current_processes()
        self.pergunta = ''

    def stop_listening_and_get_response(self):
        if self.is_listening:
            print(f"Você disse: {self.pergunta}")
            self.is_listening = False
            self.is_processing = True
            self.obter_resposta(self.pergunta)

    def run(self):
        self.wake_event = threading.Event()
        self.frames = threading.Thread(target=self.frame_capture)
        self.escutar = threading.Thread(target=self.hear)
        self.frames.start()
        self.escutar.start()


        
        keyboard.add_hotkey('v', self.start_listening)
        keyboard.add_hotkey('f', self.stop_listening_and_get_response)

        self.wake_event.wait()
        self.frames.join()
        self.escutar.join()
        print(f"Encerrando {self.ai_name}...")

if __name__ == "__main__":
    detector = ProfessorISAAC(threading.Event())
    detector.run()
