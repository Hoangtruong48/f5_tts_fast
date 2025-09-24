# Ubuntu: sudo apt install ffmpeg
# Windows please refer to https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/

import os
import time

import text_convert
import numpy as np
import soundfile as sf
os.environ["CUDA_VISIBLE_DEVICES"] = "0" # Tell it which GPU to use (or ignore if you're CPU-bound and patient!)

from vinorm import TTSnorm # Gotta normalize that Vietnamese text first
from f5tts_wrapper import F5TTSWrapper # Our handy wrapper class

# --- Config ---
# Path to the model checkpoint you downloaded from *this* repo
# MAKE SURE this path points to the actual .pth or .ckpt file!
eraX_ckpt_path = "model_48000.safetensors" # <-- CHANGE THIS!

# Path to the voice you want to clone
ref_audio_path = "test_2.wav" # <-- CHANGE THIS!

# Path to the vocab file from this repo
vocab_file = "vocab.txt" # <-- CHANGE THIS!

# Where to save the generated sound
output_dir = "output_audio"

# --- Texts ---
# Text matching the reference audio (helps the model learn the voice). Please make sure it match with the referrence audio!
text_file_ref = "ref_text.txt"
with open(text_file_ref, "r", encoding="utf-8") as f1:
    ref_text = f1.read().strip()
# ref_text = "Thậm chí không ăn thì cũng có cảm giác rất là cứng bụng, chủ yếu là cái phần rốn...trở lên. Em có cảm giác khó thở, và ngủ cũng không ngon, thường bị ợ hơi rất là nhiều"
print("Referent text = " + ref_text)
# The text you want the cloned voice to speak
# text_to_generate = "Trong khi đó, tại một chung cư trên địa bàn P.Vĩnh Tuy (Q.Hoàng Mai), nhiều người sống trên tầng cao giật mình khi thấy rung lắc mạnh nên đã chạy xuống sảnh tầng 1. Cư dân tại đây cho biết, họ chưa bao giờ cảm thấy ảnh hưởng của động đất mạnh như hôm nay."
text_file = "texttest2.txt"
with open(text_file, "r", encoding="utf-8") as f2:
    text_to_generate = f2.read().strip()

print("text gen = " + text_to_generate)
# --- Let's Go! ---
print("Initializing the TTS engine... (Might take a sec)")
tts = F5TTSWrapper(
    vocoder_name="vocos", # Using Vocos vocoder
    ckpt_path=eraX_ckpt_path,
    vocab_file=vocab_file,
    use_ema=False, # ALWAYS False as we converted from .pt to safetensors and EMA (where there is or not) was in there
)

# Normalize the reference text (makes it easier for the model)
ref_text_norm = TTSnorm(ref_text)

# Prepare the output folder
os.makedirs(output_dir, exist_ok=True)

print("Processing the reference voice...")
# Feed the model the reference voice ONCE
# Provide ref_text for better quality, or set ref_text="" to use Whisper for auto-transcription (if installed)
tts.preprocess_reference(
    ref_audio_path=ref_audio_path,
    ref_text=ref_text_norm,
    clip_short=True # Keeps reference audio to a manageable length (~12s)
)
print(f"Reference audio duration used: {tts.get_current_audio_length():.2f} seconds")

# --- Generate New Speech ---
print("Generating new speech with the cloned voice...")

# Normalize the text we want to speak
text_norm = TTSnorm(text_to_generate)

# You can generate multiple sentences easily
# Just add more normalized strings to this list
sentences = [text_norm]

for i, sentence in enumerate(sentences):
    output_path = os.path.join(output_dir, f"generated_speech_{i+1}.wav")

    # THE ACTUAL GENERATION HAPPENS HERE!
    # tts.generate(
    #     text=sentence,
    #     output_path=output_path,
    #     nfe_step=30,               # Denoising steps. More = slower but potentially better? (Default: 32)
    #     cfg_strength=2,          # How strongly to stick to the reference voice style? (Default: 2.0)
    #     speed=1.0,                 # Make it talk faster or slower (Default: 1.0)
    #     cross_fade_duration=0.15,  # Smooths transitions if text is split into chunks (Default: 0.15)
    #
    #     # ok : 30, 2.2, 1.0, 0.15
    #     # Denoising steps. Nhiều bước hơn -> chậm hơn nhưng chất lượng giọng có thể mượt hơn (mặc định: 32)
    #     # Mức độ bám sát giọng mẫu tham chiếu. Cao quá thì dễ bị méo, thấp quá thì giọng dễ khác mẫu (mặc định: 2.0)
    #     # Tốc độ đọc: 1.0 = bình thường, >1.0 = nhanh hơn, <1.0 = chậm hơn (mặc định: 1.0)
    #     # Thời gian cross-fade (giảm/ tăng âm chồng nhau) khi text bị cắt thành nhiều chunk nhỏ. Giúp chuyển mượt mà (mặc định: 0.15 giây)
    # )
    res = text_convert.convertTextToArrayTextLessThanXCharacter(sentence, 1500)
    print("Res size " + str(len(res)))
    all_waves = []
    i = 0
    for text in res:
        wav = tts.generate_wav_only(
            text=text,
            nfe_step=28,  # Denoising steps. More = slower but potentially better? (Default: 32)
            cfg_strength=2.2,  # How strongly to stick to the reference voice style? (Default: 2.0)
            speed=1.0,  # Make it talk faster or slower (Default: 1.0)
            cross_fade_duration=0.15,  # Smooths transitions if text is split into chunks (Default: 0.15)

            # ok : 30, 2.2, 1.0, 0.15
            # Denoising steps. Nhiều bước hơn -> chậm hơn nhưng chất lượng giọng có thể mượt hơn (mặc định: 32)
            # Mức độ bám sát giọng mẫu tham chiếu. Cao quá thì dễ bị méo, thấp quá thì giọng dễ khác mẫu (mặc định: 2.0)
            # Tốc độ đọc: 1.0 = bình thường, >1.0 = nhanh hơn, <1.0 = chậm hơn (mặc định: 1.0)
            # Thời gian cross-fade (giảm/ tăng âm chồng nhau) khi text bị cắt thành nhiều chunk nhỏ. Giúp chuyển mượt mà (mặc định: 0.15 giây)
        )
        all_waves.append(wav)
        time.sleep(2)
        print("Đã xong đoạn thứ " + str(i + 1))
        i += 1

    final_wave = np.concatenate(all_waves)
    final_wave = final_wave / np.max(np.abs(final_wave))
    sf.write(output_path, final_wave, samplerate=tts.target_sample_rate, subtype="PCM_16")
    print(f"Boom! Audio saved to: {output_path}")

print("\nAll done! Check your output folder.")