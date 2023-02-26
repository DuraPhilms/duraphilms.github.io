import os
from dataclasses import dataclass
from math import sqrt, ceil
from tempfile import TemporaryDirectory
import subprocess
from pathlib import Path
from PIL import Image


@dataclass
class VttConfig:
    # Time in seconds between frames
    frame_delta: int = 5
    # Width of video frames in pixels
    frame_width: int = 100
    # Filename of the image sprite used in the vtt text file (optional)
    referenced_image_filename: str = str()


@dataclass
class ImageSize:
    width: int
    height: int


def run_command(args: list[str], debug: bool = False):
    if debug:
        print("[gen-vtt] " + " ".join(args))
    return subprocess.check_output(args, stderr=subprocess.STDOUT).decode("utf-8")


def extract_video_snapshots(video_source: str, output_directory: str, vtt_config: VttConfig) -> list[str]:
    run_command([
        "ffmpeg", "-i", video_source, "-f", "image2", "-bt", "20M",
        "-vf", f"fps=1/{vtt_config.frame_delta},scale={vtt_config.frame_width}:-1",
        "-aspect", "16:9",
        f"{output_directory}/f%03d.png"
    ])

    return sorted(str(f) for f in Path(output_directory).iterdir() if f.is_file())


def get_image_size(image_file: str) -> ImageSize:
    i = Image.open(image_file)
    return ImageSize(i.size[0], i.size[1])


def glue_vtt_sprite(output_file: str, frame_files: list[str], frame_size: ImageSize, grid_width: int):
    run_command([
        "montage",
        *frame_files,
        "-tile", f"{grid_width}",
        "-geometry", f"{frame_size.width}x{frame_size.height}+0+0",
        output_file
    ])


def serialize_vtt_file(frame_count: int,
                       frame_size: ImageSize,
                       grid_width: int,
                       vtt_config: VttConfig) -> str:
    out = ["WEBVTT\n\n"]

    def writeln(s: str = str()):
        out.append(s + "\n")

    def frame_position(i: int) -> tuple[int, int]:
        x = i % grid_width
        y = i // grid_width
        return x * frame_size.width, y * frame_size.height

    def format_timestamp(seconds: int) -> str:
        assert seconds >= 0
        ss = seconds % 60
        mm = (seconds // 60) % 60
        hh = (seconds // 60 // 60) % 24

        return f"{hh:02d}:{mm:02d}:{ss:02d}.000"

    for i in range(frame_count):
        start = format_timestamp(i * vtt_config.frame_delta)
        end = format_timestamp((i + 1) * vtt_config.frame_delta)

        x, y = frame_position(i)

        writeln(f"{start} --> {end}")
        writeln(f"{vtt_config.referenced_image_filename}#xywh={x},{y},{frame_size.width},{frame_size.height}")
        writeln()

    return str().join(out)


def generate_vtt_thumbnails(video_source: str, image_filename: str, vtt_filename: str, vtt_config: VttConfig):
    print(f"[gen-vtt] Generating WebVTT thumbnails for {video_source}…")

    # fallback values
    vtt_config.referenced_image_filename = vtt_config.referenced_image_filename or os.path.basename(image_filename)

    # create temporary directory for video snapshots
    tmp_directory = TemporaryDirectory()

    # generate video snapshots
    frame_files = extract_video_snapshots(video_source, tmp_directory.name, vtt_config)

    assert len(frame_files) > 0

    grid_width = int(ceil(sqrt(len(frame_files))))
    image_size = get_image_size(frame_files[0])

    # create image file
    glue_vtt_sprite(image_filename, frame_files, image_size, grid_width)

    # generate the actual vtt text file
    vtt_file_data = serialize_vtt_file(len(frame_files), image_size, grid_width, vtt_config)
    with open(vtt_filename, "w") as f:
        f.write(vtt_file_data)

    print(f"[gen-vtt] Generated WebVTT with n={len(frame_files)}, image size={os.path.getsize(image_filename)}")
