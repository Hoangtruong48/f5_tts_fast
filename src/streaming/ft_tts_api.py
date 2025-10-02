import time

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import io
import os
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import text_convert
from vinorm import TTSnorm  # Chuẩn hóa text tiếng Việt
from f5tts_wrapper import F5TTSWrapper  # Wrapper TTS
from fastapi import HTTPException
import logging
from typing import Optional
import paramiko
import tempfile
from fastapi.responses import JSONResponse
import yaml
import requests
import os


class TTSRequest(BaseModel):
    input: str
    speed: float = 1.0


class TTSRequestV2(BaseModel):
    input: str
    speed: float = 1.0
    path: str
    filename: str


class VoiceOption(BaseModel):
    voice_id: Optional[str] = None
    model: Optional[str] = None
    speed: float = 1.0


class TTSRequestV3(BaseModel):
    option: Optional[VoiceOption] = None
    server_id: str
    content: str
    path: str


app = FastAPI(title="TTS API")
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
logger = logging.getLogger("tts_api")

# Load model ngay khi khởi động server
eraX_ckpt_path = "model_last.pt"
vocab_file = "vocab.txt"
ref_audio_path = "test_2.wav"
text_file_ref = "ref_text.txt"

with open(text_file_ref, "r", encoding="utf-8") as f1:
    ref_text = f1.read().strip()

tts = F5TTSWrapper(
    vocoder_name="vocos",
    ckpt_path=eraX_ckpt_path,
    vocab_file=vocab_file,
    use_ema=False,
)

ref_text_norm = TTSnorm(ref_text)
tts.preprocess_reference(
    ref_audio_path=ref_audio_path,
    ref_text=ref_text_norm,
    clip_short=True
)


@app.post("/tts")
async def tts_endpoint(request: TTSRequest):
    try:
        text_to_generate = request.input
        text_norm = TTSnorm(text_to_generate.encode("utf-8").decode("utf-8"))
        sentences = [text_norm]

        all_waves = []
        for sentence in sentences:
            try:
                wav = tts.generate_wav_only(
                    text=sentence,
                    nfe_step=25,
                    cfg_strength=2.0,
                    speed=request.speed,
                    cross_fade_duration=0.1
                )
                all_waves.append(wav)
            except Exception as e:
                logger.error(f"Lỗi khi generate wav cho câu: {sentence}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Lỗi generate wav: {str(e)}")

        # Gộp lại và chuẩn hóa
        final_wave = np.concatenate(all_waves)
        final_wave = final_wave / np.max(np.abs(final_wave))

        # Ghi vào memory buffer (không ghi ra file)
        wav_bytes = io.BytesIO()
        sf.write(wav_bytes, final_wave, samplerate=tts.target_sample_rate, format="WAV")
        wav_bytes.seek(0)

        # convert sang mp3 (bitrate 64k hoặc 128k)
        audio = AudioSegment.from_file(wav_bytes, format="wav")
        mp3_bytes = io.BytesIO()
        audio.export(mp3_bytes, format="mp3", bitrate="48k")
        mp3_bytes.seek(0)

        return StreamingResponse(
            mp3_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": 'inline; filename=\"output.mp3\"'}
        )

    except Exception as e:
        logger.error("Lỗi tổng quát trong endpoint /tts", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


@app.post("/tts-v2")
async def tts_endpoint(request: TTSRequestV2):
    try:
        text_to_generate = request.input
        text_norm = TTSnorm(text_to_generate.encode("utf-8").decode("utf-8"))
        sentences = [text_norm]

        all_waves = []
        for sentence in sentences:
            try:
                wav = tts.generate_wav_only(
                    text=sentence,
                    nfe_step=25,
                    cfg_strength=2.0,
                    speed=request.speed,
                    cross_fade_duration=0.1
                )
                all_waves.append(wav)
            except Exception as e:
                logger.error(f"Lỗi khi generate wav cho câu: {sentence}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Lỗi generate wav: {str(e)}")

        # Gộp lại và chuẩn hóa
        final_wave = np.concatenate(all_waves)
        final_wave = final_wave / np.max(np.abs(final_wave))

        # Ghi vào memory buffer (không ghi ra file)
        wav_bytes = io.BytesIO()
        sf.write(wav_bytes, final_wave, samplerate=tts.target_sample_rate, format="WAV")
        wav_bytes.seek(0)

        # convert sang mp3 (bitrate 64k hoặc 128k)
        audio = AudioSegment.from_file(wav_bytes, format="wav")
        mp3_bytes = io.BytesIO()
        audio.export(mp3_bytes, format="mp3", bitrate="48k")
        mp3_bytes.seek(0)

        # ================== Lưu ra file theo path + filename ==================
        try:
            save_dir = request.path
            save_filename = request.filename
            os.makedirs(save_dir, exist_ok=True)  # tạo folder nếu chưa có
            save_path = os.path.join(save_dir, save_filename)

            with open(save_path, "wb") as f:
                f.write(mp3_bytes.getbuffer())

            logger.info(f"File đã được lưu: {save_path}")
        except Exception as e:
            logger.error("Lỗi khi lưu file ra disk", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Lỗi khi lưu file: {str(e)}")

        return StreamingResponse(
            mp3_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": 'inline; filename=\"output.mp3\"'}
        )

    except Exception as e:
        logger.error("Lỗi tổng quát trong endpoint /tts", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


@app.post("/tts-v3")
async def tts_endpoint(request: TTSRequestV3):
    try:
        print(request)
        server_id = request.server_id
        path = request.path
        speed = request.option.speed
        text_to_generate = request.content
        text_norm = TTSnorm(text_to_generate.encode("utf-8").decode("utf-8"))
        sentences = [text_norm]

        all_waves = []
        for sentence in sentences:
            try:
                wav = tts.generate_wav_only(
                    text=sentence,
                    nfe_step=25,
                    cfg_strength=2.0,
                    speed=speed,
                    cross_fade_duration=0.1
                )
                all_waves.append(wav)
            except Exception as e:
                logger.error(f"Lỗi khi generate wav cho câu: {sentence}", exc_info=True)
                return JSONResponse(
                    status_code=500,
                    content={"rc": -1, "rd": f"Lỗi generate wav: {str(e)}"}
                )

        # Gộp lại và chuẩn hóa
        final_wave = np.concatenate(all_waves)
        final_wave = final_wave / np.max(np.abs(final_wave))

        # Ghi vào memory buffer (không ghi ra file)
        wav_bytes = io.BytesIO()
        sf.write(wav_bytes, final_wave, samplerate=tts.target_sample_rate, format="WAV")
        wav_bytes.seek(0)

        # convert sang mp3
        audio = AudioSegment.from_file(wav_bytes, format="wav")
        mp3_bytes = io.BytesIO()
        audio.export(mp3_bytes, format="mp3", bitrate="48k")
        mp3_bytes.seek(0)
        file_size = mp3_bytes.getbuffer().nbytes
        logger.info(f"Kích thước file BytesIO: {file_size} bytes")
        # Upload qua SSH
        # get config ssh
        server = get_server_config("config.yml", server_id)
        ssh_host = server["ip"]
        ssh_port = server["port"]
        ssh_user = server["user"]
        ssh_password = server["password"]

        print("Check SSH connection" + str(ssh_host) + "port= " + str(ssh_port) + "user=" + str(ssh_user) +
              "password=" + str(ssh_password))

        # xử lí path
        full_path = path
        file_name = os.path.basename(full_path)
        dir_path = os.path.dirname(full_path)
        try:
            current_ip = get_public_ip()
            print(current_ip)
            if ssh_host == current_ip and ssh_port == 2202:
                # Lưu trực tiếp
                save_file_locally(mp3_bytes, dir_path, file_name)
                print("Lưu file trực tiếp tại server hiện tại")
            else:
                print("Lưu file bằng ssh")
                try:
                    upload_bytesio_via_ssh(
                        mp3_bytes,
                        remote_dir=dir_path,
                        filename=file_name,
                        ssh_host=ssh_host,
                        ssh_user=ssh_user,
                        ssh_pass=ssh_password,
                        ssh_port=ssh_port
                    )
                except Exception as ex:
                    print("Exception : {}", ex)
        except Exception as e:
            print("Lỗi khi upload file SSH")
            return JSONResponse(
                status_code=500,
                content={"rc": -1, "rd": f"Lỗi upload SSH: {str(e)}"}
            )

        return JSONResponse(
            status_code=200,
            content={"rc": 0, "rd": "Thành công"}
        )

    except Exception as e:
        print("Lỗi tổng quát trong endpoint /tts-v3")
        return JSONResponse(
            status_code=500,
            content={"rc": -1, "rd": f"Lỗi hệ thống: {str(e)}"}
        )


def upload_bytesio_via_ssh(
        file_bytes: io.BytesIO,
        remote_dir: str,
        filename: str,
        ssh_host: str,
        ssh_user: str,
        ssh_pass: str,
        ssh_port: int
):
    file_bytes.seek(0)
    try:
        transport = paramiko.Transport((ssh_host, ssh_port))
        transport.connect(username=ssh_user, password=ssh_pass)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Đảm bảo thư mục tồn tại (nếu chưa có thì tạo)
        try:
            sftp.chdir(remote_dir)
        except IOError:
            # nếu chưa tồn tại thì tạo từng cấp
            current_dir = ""
            for folder in remote_dir.strip("/").split("/"):
                current_dir += f"/{folder}"
                try:
                    sftp.chdir(current_dir)
                except IOError:
                    sftp.mkdir(current_dir)
                    sftp.chdir(current_dir)

        # Ghép full path
        remote_path = os.path.join(remote_dir, filename)

        # Ghi trực tiếp stream lên server
        with sftp.file(remote_path, "wb") as remote_file:
            remote_file.write(file_bytes.read())

        info = sftp.stat(remote_path)
        print(f"Uploaded {remote_path} ({info.st_size} bytes) lên {ssh_host}")

        sftp.close()
        transport.close()
        print(f"Uploaded directly to {remote_path} on {ssh_host}")

    except paramiko.AuthenticationException:
        raise Exception("Lỗi upload SSH: Authentication failed (sai user/pass hoặc server cấm password).")
    except Exception as e:
        raise Exception(f"Lỗi upload SSH: {str(e)}")


def get_server_config(yaml_file: str, server_id: str):
    with open(yaml_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    servers = config.get("server_config", [])
    for server in servers:
        if server.get("id") == server_id:
            return {
                "ip": server.get("ip"),
                "port": server.get("port"),
                "user": server.get("user"),
                "password": server.get("password")
            }
    raise ValueError(f"Server id '{server_id}' not found in config")


def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text.strip()
    except Exception:
        print("Exception while get ip public")
        return None


def save_file_locally(file_bytes, dir_path, file_name):
    # Nếu là BytesIO thì convert sang bytes
    if isinstance(file_bytes, io.BytesIO):
        file_bytes = file_bytes.getvalue()

    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    file_size = os.path.getsize(file_path)
    print(f"File lưu tại: {file_path}, size = {file_size} bytes")

    return file_path
