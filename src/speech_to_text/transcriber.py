from pathlib import Path
import whisper

from speech_to_text.utils import format_timestamp


class AudioTranscriber:
    def __init__(self, model_name: str = "medium") -> None:
        self.model_name = model_name
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path: Path) -> dict:
        if not audio_path.exists():
            raise FileNotFoundError(f"Áudio não encontrado: {audio_path}")

        return self.model.transcribe(
            str(audio_path),
            language="pt",
            verbose=True
        )

    def save_plain_text(self, result: dict, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        text = result.get("text", "").strip()

        with output_path.open("w", encoding="utf-8") as file:
            file.write(text)

    def save_with_timestamps(self, result: dict, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        segments = result.get("segments", [])

        with output_path.open("w", encoding="utf-8") as file:
            for segment in segments:
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                text = segment["text"].strip()

                file.write(f"[{start} - {end}] {text}\n")