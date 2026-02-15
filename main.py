from pathlib import Path
import os
import subprocess


def resolve_path(raw_path: str) -> Path:
    return Path(os.path.expanduser(os.path.expandvars(raw_path)))


SOURCE_DIR = resolve_path(os.getenv("DJI_SOURCE_DIR", "$HOME/Production/dji-footage"))
OUTPUT_DIR = resolve_path(os.getenv("DJI_OUTPUT_DIR", "$HOME/Production/color-graded"))
LUT_FILE = resolve_path(
    os.getenv("DJI_LUT_FILE", "$HOME/Production/luts/DJI_DLogM_to_Rec709.cube")
)

VIDEO_CODEC = "libx265"
PIXEL_FORMAT = "yuv420p10le"
CRF = "16"
PRESET = "slow"


def build_ffmpeg_command(input_file: Path, output_file: Path) -> list[str]:
    return [
        "ffmpeg",
        "-i",
        str(input_file),
        "-vf",
        f"lut3d='{LUT_FILE.as_posix()}'",
        "-c:v",
        VIDEO_CODEC,
        "-pix_fmt",
        PIXEL_FORMAT,
        "-crf",
        CRF,
        "-preset",
        PRESET,
        "-c:a",
        "copy",
        str(output_file),
    ]


def main() -> None:
    if not SOURCE_DIR.exists():
        raise FileNotFoundError(f"Source folder not found: {SOURCE_DIR}")
    if not LUT_FILE.exists():
        raise FileNotFoundError(f"LUT file not found: {LUT_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    mp4_files = sorted(
        [path for path in SOURCE_DIR.iterdir() if path.is_file() and path.suffix.lower() == ".mp4"]
    )
    if not mp4_files:
        print(f"No .mp4 files found in {SOURCE_DIR}")
        return

    for input_file in mp4_files:
        output_file = OUTPUT_DIR / input_file.name
        if output_file.exists():
            print(f"Skipping (already processed): {input_file} -> {output_file}")
            continue
        print(f"Processing: {input_file} -> {output_file}")
        cmd = build_ffmpeg_command(input_file, output_file)
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
