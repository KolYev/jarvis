import glob
import os

import soundfile as sf
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
import TTS.tts.models.xtts as xtts_module
from TTS.tts.models.xtts import Xtts


def load_audio(audiopath, sampling_rate):
    data, lsr = sf.read(audiopath, dtype="float32", always_2d=True)  # (n, channels)
    audio = torch.from_numpy(data.T)  # (channels, n)
    if audio.size(0) != 1:
        audio = torch.mean(audio, dim=0, keepdim=True)
    if int(lsr) != sampling_rate:
        audio = torchaudio.functional.resample(audio, int(lsr), sampling_rate)
    audio = audio.clip(-1, 1)
    return audio

xtts_module.load_audio = load_audio

# путь к папке с аудиофайлами голоса
voices_dir = "voices"

# собираем все аудиофайлы из папки
audio_files = [
    os.path.join(voices_dir, f)
    for f in os.listdir(voices_dir)
    if f.endswith(('.wav', '.mp3', '.flac', '.m4a'))
]

if not audio_files:
    raise Exception("В папке voices нет аудиофайлов")

print(f"Найдено файлов для клонирования: {len(audio_files)}")

text_to_speak = "Привет! Меня зовут Джарвис."

candidates = glob.glob(os.path.expanduser(r"~\.cache\huggingface\hub\models--tts-hub--XTTS-v2\snapshots\*"))
local_root = os.path.join(os.environ.get("LOCALAPPDATA", ""), "tts", "tts_models--multilingual--multi-dataset--xtts_v2")
if os.path.isdir(local_root):
    candidates.append(local_root)

model_dir = next(p for p in candidates if os.path.isfile(os.path.join(p, "config.json")))

print(f"Загружаю модель из: {model_dir}")

config = XttsConfig()
config.load_json(os.path.join(model_dir, "config.json"))

tts = Xtts.init_from_config(config)
tts.load_checkpoint(config, checkpoint_dir=model_dir, eval=True)
if torch.cuda.is_available():
    tts.cuda()

print("Модель загружена")

gpt_cond_latent, speaker_embedding = tts.get_conditioning_latents(audio_path=audio_files)

print("Синтез речи")
out = tts.inference(
    text=text_to_speak,
    language="ru",
    gpt_cond_latent=gpt_cond_latent,
    speaker_embedding=speaker_embedding,
)

sf.write("result.wav", out["wav"], 24000, subtype="PCM_16")
print("Файл сохранён в result.wav")