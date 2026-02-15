# color-grade-dji

Batch color grading for DJI `.mp4` footage using `ffmpeg` and a `.cube` LUT.

The script processes every `.mp4` in an input folder and writes graded files to an output folder with the same filenames.
If an output file already exists, it is skipped so reruns only process new files.

## What this does

- Input: all `.mp4` files in `DJI_SOURCE_DIR`
- Filter: `lut3d` with your `.cube` file
- Video encode: `libx265`, `yuv420p10le`, `-crf 16`, `-preset slow`
- Audio: copied (`-c:a copy`)
- Output: same filename in `DJI_OUTPUT_DIR`

## Requirements

- Python 3.12+
- `ffmpeg` available on your `PATH`
- A LUT file (`.cube`) for grading

Quick check:

```bash
ffmpeg -version
python3 --version
```

## Configuration

`main.py` uses environment variables so you do not need to commit machine-specific absolute paths.

- `DJI_SOURCE_DIR` (default: `$HOME/Production/dji-footage`)
- `DJI_OUTPUT_DIR` (default: `$HOME/Production/color-graded`)
- `DJI_LUT_FILE` (default: `$HOME/Production/luts/DJI_DLogM_to_Rec709.cube`)

Both `$HOME` and `~` are supported.

## Run

Use defaults:

```bash
python3 main.py
```

or if you have uv

```bash
uv run main.py
```

Override paths for one run:

```bash
DJI_SOURCE_DIR="$HOME/my-input" \
DJI_OUTPUT_DIR="$HOME/my-output" \
DJI_LUT_FILE="$HOME/luts/DJI_DLogM_to_Rec709.cube" \
python3 main.py
```

## Typical folder setup

```text
Production/
  dji-footage/
    DJI_20260207012613_0022_D.MP4
    ...
  luts/
    DJI_DLogM_to_Rec709.cube
  color-graded/
    (generated files)
```

## Notes

- Rerunning is safe: existing output files are skipped.
- If source folder or LUT file is missing, the script exits with a clear error.
