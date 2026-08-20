import glob
import os
import re
import numpy as np
import soundfile as sf
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
import TTS.tts.models.xtts as xtts_module
from TTS.tts.models.xtts import Xtts


def load_audio(audiopath, sampling_rate):
    data, lsr = sf.read(audiopath, dtype="float32", always_2d=True)
    audio = torch.from_numpy(data.T)
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

# лимиты символов для каждого языка
XTTS_CHAR_LIMITS = {
    "en": 250, "ru": 182, "de": 253, "fr": 273, "es": 239, "it": 213,
    "pt": 203, "pl": 224, "tr": 226, "nl": 251, "cs": 186, "ar": 166,
    "zh-cn": 82, "ja": 71, "hu": 224, "ko": 95,
}


def split_text(text, max_chars=180):
    """
    Разбивает текст на части по предложениям, не превышая max_chars.
    Если предложение само длиннее max_chars — режем по запятым, а если
    и это не помогает — по словам (без разрывания слов посередине).
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""

    def split_long_sentence(sentence, limit, out):
        parts = re.split(r'(?<=[,;:])\s+', sentence)
        piece = ""
        for part in parts:
            if len(piece) + len(part) + 1 <= limit:
                piece = (piece + " " + part).strip()
            else:
                if piece:
                    out.append(piece)
                if len(part) > limit:
                    words = part.split(" ")
                    buf = ""
                    for w in words:
                        if len(buf) + len(w) + 1 <= limit:
                            buf = (buf + " " + w).strip()
                        else:
                            if buf:
                                out.append(buf)
                            buf = w
                    piece = buf
                else:
                    piece = part
        if piece:
            out.append(piece)

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_chars:
            current = (current + " " + sentence).strip() if current else sentence
        else:
            if current:
                chunks.append(current)
                current = ""
            if len(sentence) > max_chars:
                split_long_sentence(sentence, max_chars, chunks)
            else:
                current = sentence
    if current:
        chunks.append(current)
    return chunks


def text_to_speech(text_to_speak, language="ru"):
    print("Синтез речи")
    limit = XTTS_CHAR_LIMITS.get(language, 200) - 10
    chunks = split_text(text_to_speak, max_chars=limit)

    all_audio = []
    sample_rate = 24000

    for idx, chunk in enumerate(chunks, 1):
        print(f"Обработка части {idx}/{len(chunks)}: {chunk[:40]}...")
        out = tts.inference(
            text=chunk,
            language=language,
            gpt_cond_latent=gpt_cond_latent,
            speaker_embedding=speaker_embedding,
        )
        audio = out["wav"]
        all_audio.append(audio)

    full_audio = np.concatenate(all_audio, axis=0)
    sf.write("result.wav", full_audio, sample_rate, subtype="PCM_16")
    print("Файл сохранён в result.wav")