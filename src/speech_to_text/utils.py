from pathlib import Path
import os
import re
from datetime import datetime


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


def build_output_paths(audio_path: Path, output_dir: Path) -> tuple[Path, Path]:
    safe_stem = sanitize_filename(audio_path.stem)

    plain_path = output_dir / f"{safe_stem}_transcricao.txt"
    timestamps_path = output_dir / f"{safe_stem}_transcricao_com_tempos.txt"

    # If files already exist, append a timestamp to keep previous runs.
    if plain_path.exists() or timestamps_path.exists():
        suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        plain_path = output_dir / f"{safe_stem}_{suffix}_transcricao.txt"
        timestamps_path = output_dir / f"{safe_stem}_{suffix}_transcricao_com_tempos.txt"

    return plain_path, timestamps_path


def sanitize_filename(value: str) -> str:
    safe_value = re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_")
    return safe_value or "audio"