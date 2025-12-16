import argparse
import os
import sys
import zipfile
from pillow_heif import register_heif_opener
from PIL import Image
from moviepy import VideoFileClip


def convert_heic_to_png(input_path: str, output_path: str) -> None:
    """
    Convert a HEIC image to PNG format.

    Args:
        input_path (str): Path to the source HEIC file.
        output_path (str): Path where the PNG file will be saved.
    """
    try:
        register_heif_opener()
        print(f"Reading HEIC file: {input_path}")
        image = Image.open(input_path)
        print(f"Saving to PNG: {output_path}")
        image.save(output_path, format="PNG")
        print("Conversion successful.")
    except Exception as e:
        print(f"Error converting HEIC to PNG: {e}", file=sys.stderr)


def convert_mov_to_mp4(input_path: str, output_path: str) -> None:
    """
    Convert a MOV video to MP4 format.

    Args:
        input_path (str): Path to the source MOV file.
        output_path (str): Path where the MP4 file will be saved.
    """
    try:
        print(f"Reading MOV file: {input_path}")
        # Load the video clip
        clip = VideoFileClip(input_path)
        print(f"Writing to MP4: {output_path}")
        # Write the video file to MP4 format with audio
        clip.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac"
        )
        clip.close()
        print("Conversion successful.")
    except Exception as e:
        print(f"Error converting MOV to MP4: {e}", file=sys.stderr)


def process_file(input_file: str) -> None:
    """
    Process a single file based on its extension.

    Args:
        input_file (str): Path to the file to process.
    """
    # Get file extension (lowercase for comparison)
    _, ext = os.path.splitext(input_file)
    ext = ext.lower()

    # Determine output filename (replace extension)
    base_name = os.path.splitext(input_file)[0]

    if ext == ".heic":
        output_file = f"{base_name}.png"
        convert_heic_to_png(input_file, output_file)
    elif ext == ".mov":
        output_file = f"{base_name}.mp4"
        convert_mov_to_mp4(input_file, output_file)
    else:
        # Silently skip unsupported files in batch mode? 
        # Or just print info. Doing print info for now.
        pass 


def process_directory(directory_path: str) -> None:
    """
    Walk through a directory and process compatible files.

    Args:
        directory_path (str): Path to the directory.
    """
    print(f"scanning directory: {directory_path}...")
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            if ext.lower() in [".heic", ".mov"]:
                process_file(file_path)


def handle_zip(zip_path: str) -> None:
    """
    Extract a zip file and process its contents.

    Args:
        zip_path (str): Path to the zip file.
    """
    base_dir = os.path.dirname(zip_path)
    zip_name = os.path.splitext(os.path.basename(zip_path))[0]
    extract_dir = os.path.join(base_dir, f"extracted_{zip_name}")

    try:
        print(f"Extracting zip file: {zip_path} to {extract_dir}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        process_directory(extract_dir)
        print("Zip processing complete.")

    except zipfile.BadZipFile:
        print(f"Error: '{zip_path}' is not a valid zip file.", file=sys.stderr)
    except Exception as e:
        print(f"Error processing zip file: {e}", file=sys.stderr)


def main() -> None:
    """
    Main function to parse arguments and dispatch conversion.
    """
    parser = argparse.ArgumentParser(
        description="Convert HEIC to PNG, MOV to MP4, or process a ZIP containing them."
    )
    parser.add_argument(
        "filename", 
        type=str, 
        help="The path to the file to convert (HEIC, MOV, or ZIP)."
    )

    args = parser.parse_args()
    input_file = args.filename

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    _, ext = os.path.splitext(input_file)
    ext = ext.lower()

    if ext == ".zip":
        handle_zip(input_file)
    elif ext in [".heic", ".mov"]:
         process_file(input_file)
    else:
        print(
            f"Unsupported file extension: {ext}. "
            "Supported formats are .heic, .mov, and .zip"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
