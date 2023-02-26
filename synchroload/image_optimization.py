import os.path
from shutil import which
import subprocess
from PIL import Image


def check_guetzli_availability() -> bool:
    return bool(which("guetzli"))


def guetzli(input_file: str, output_file: str, jpg_quality: int):
    subprocess.run(["guetzli", "--quality", str(jpg_quality), input_file, output_file])


def compress_lossy(input_file: str, output_file: str, jpg_quality: int = 90):
    guetzli_available = check_guetzli_availability()
    if not guetzli_available:
        print("[image-optimization] Missing guetzli, falling back to PIL.")

    input_size = os.path.getsize(input_file)

    print(f"[image-optimization] Compressing {input_file} -> {output_file} (q={jpg_quality})…")
    if guetzli_available:
        guetzli(input_file, output_file, jpg_quality)
    else:
        i = Image.open(input_file)
        i.save(output_file, "JPEG", quality=jpg_quality)

    output_size = os.path.getsize(output_file)
    print(f"[image-optimization] Reduced by {input_size / output_size:0.1f}, now {(output_size / 1024):0.1f} kB")