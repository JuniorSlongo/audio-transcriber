from pathlib import Path
import argparse

from speech_to_text.transcriber import AudioTranscriber
from speech_to_text.utils import (
    build_output_paths,
    configure_local_ffmpeg,
    get_project_root,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcreve áudios usando Whisper com FFmpeg local."
    )

    parser.add_argument(
        "--audio",
        required=True,
        help="Caminho do arquivo de áudio. Ex: audios/Nova Gravacao.m4a"
    )

    parser.add_argument(
        "--model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Modelo Whisper usado na transcrição."
    )

    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Pasta onde os arquivos de saída serão salvos."
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    project_root = get_project_root()
    configure_local_ffmpeg()

    audio_path = project_root / args.audio
    output_dir = project_root / args.output_dir

    print(f"Modelo selecionado: {args.model}")
    print(f"Áudio: {audio_path}")

    transcriber = AudioTranscriber(model_name=args.model)
    result = transcriber.transcribe(audio_path)

    plain_output_path, timestamps_output_path = build_output_paths(
        audio_path=audio_path,
        output_dir=output_dir,
    )

    transcriber.save_plain_text(
        result,
        plain_output_path,
    )

    transcriber.save_with_timestamps(
        result,
        timestamps_output_path,
    )

    print("Transcrição concluída.")
    print(f"Arquivo gerado: {plain_output_path}")
    print(f"Arquivo gerado: {timestamps_output_path}")


if __name__ == "__main__":
    main()