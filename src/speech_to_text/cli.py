from pathlib import Path
import argparse

from speech_to_text.queue_manager import TranscriptionQueue
from speech_to_text.utils import (
    configure_local_ffmpeg,
    get_project_root,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcreve áudios usando Whisper com FFmpeg local."
    )

    parser.add_argument(
        "--audio",
        action="append",
        dest="audios",
        help="Caminho de um arquivo de áudio. Pode ser usado múltiplas vezes. Ex: --audio audios/audio1.m4a --audio audios/audio2.m4a"
    )

    parser.add_argument(
        "--audio-dir",
        help="Caminho de um diretório com múltiplos áudios para transcrever em fila."
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

    parser.add_argument(
        "--save-log",
        action="store_true",
        help="Salva um log JSON da fila após o processamento."
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Validar argumentos
    if not args.audios and not args.audio_dir:
        print("Erro: Especifique pelo menos um arquivo (--audio) ou um diretório (--audio-dir)")
        return

    project_root = get_project_root()
    configure_local_ffmpeg()

    output_dir = project_root / args.output_dir

    # Criar fila de transcrição
    queue = TranscriptionQueue(model_name=args.model)

    print(f"Modelo selecionado: {args.model}")
    print(f"Diretório de saída: {output_dir}\n")

    # Adicionar arquivos à fila
    if args.audios:
        for audio in args.audios:
            audio_path = project_root / audio
            try:
                queue.add_task(audio_path, output_dir)
            except FileNotFoundError as e:
                print(f"✗ Erro: {e}")

    if args.audio_dir:
        audio_dir_path = project_root / args.audio_dir
        if not audio_dir_path.exists():
            print(f"✗ Erro: Diretório não encontrado: {audio_dir_path}")
            return
        print(f"Adicionando áudios do diretório: {audio_dir_path}\n")
        queue.add_tasks_from_directory(audio_dir_path, output_dir)

    # Processar fila
    queue.process_queue()

    # Salvar log se solicitado
    if args.save_log:
        log_path = output_dir / "transcription_log.json"
        queue.save_queue_log(log_path)


if __name__ == "__main__":
    main()