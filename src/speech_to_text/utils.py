from pathlib import Path
import os


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def configure_local_ffmpeg() -> None:
    project_root = get_project_root()
    ffmpeg_bin = project_root / "ffmpeg" / "bin"

    if not ffmpeg_bin.exists():
        raise FileNotFoundError(
            f"FFmpeg local não encontrado em: {ffmpeg_bin}"
        )

    os.environ["PATH"] = str(ffmpeg_bin) + os.pathsep + os.environ["PATH"]


def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"