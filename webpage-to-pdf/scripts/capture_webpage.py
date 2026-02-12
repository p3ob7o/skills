#!/usr/bin/env python3
"""
Capture a webpage as a multi-page PDF from browser screenshots.

This script processes a GIF file (created from browser scroll capture)
and converts it to a multi-page PDF where each frame becomes a page.

Usage:
    python capture_webpage.py <gif_path> <output_pdf_path>

Example:
    python capture_webpage.py /path/to/capture.gif /output/webpage.pdf
"""

import sys
import os
import base64
import json
from PIL import Image
from io import BytesIO


def gif_to_pdf(gif_path: str, output_pdf: str) -> bool:
    """
    Convert a GIF file to a multi-page PDF.

    Args:
        gif_path: Path to the input GIF file
        output_pdf: Path for the output PDF file

    Returns:
        True if successful, False otherwise
    """
    try:
        # Open the GIF
        gif = Image.open(gif_path)

        # Extract all frames
        frames = []
        try:
            while True:
                # Convert to RGB (PDF doesn't support palette mode)
                frame = gif.convert('RGB')
                frames.append(frame.copy())
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        if not frames:
            print("Error: No frames extracted from GIF")
            return False

        print(f"Extracted {len(frames)} frames from GIF")

        # Create output directory if needed
        os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

        # Save as PDF
        frames[0].save(
            output_pdf,
            save_all=True,
            append_images=frames[1:] if len(frames) > 1 else [],
            resolution=100.0
        )

        file_size = os.path.getsize(output_pdf)
        print(f"PDF saved: {output_pdf} ({file_size / 1024:.1f} KB)")
        return True

    except Exception as e:
        print(f"Error converting GIF to PDF: {e}")
        return False


def base64_gif_to_pdf(base64_data: str, output_pdf: str) -> bool:
    """
    Convert base64-encoded GIF data to a multi-page PDF.

    Args:
        base64_data: Base64-encoded GIF data
        output_pdf: Path for the output PDF file

    Returns:
        True if successful, False otherwise
    """
    try:
        # Decode base64
        gif_data = base64.b64decode(base64_data)

        # Open as GIF
        gif = Image.open(BytesIO(gif_data))

        # Extract all frames
        frames = []
        try:
            while True:
                frame = gif.convert('RGB')
                frames.append(frame.copy())
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        if not frames:
            print("Error: No frames extracted from GIF")
            return False

        print(f"Extracted {len(frames)} frames")

        # Create output directory if needed
        os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

        # Save as PDF
        frames[0].save(
            output_pdf,
            save_all=True,
            append_images=frames[1:] if len(frames) > 1 else [],
            resolution=100.0
        )

        file_size = os.path.getsize(output_pdf)
        print(f"PDF saved: {output_pdf} ({file_size / 1024:.1f} KB)")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def json_file_to_pdf(json_path: str, output_pdf: str) -> bool:
    """
    Process a JSON file containing base64 GIF data (from MCP filesystem tool).

    Args:
        json_path: Path to JSON file with base64-encoded GIF
        output_pdf: Path for the output PDF file

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Extract base64 data from MCP filesystem format
        if 'content' in data and len(data['content']) > 0:
            content_item = data['content'][0]
            if 'data' in content_item:
                base64_data = content_item['data']
            elif 'blob' in content_item:
                base64_data = content_item['blob']
            else:
                print(f"Error: Could not find image data. Keys: {content_item.keys()}")
                return False
        else:
            print("Error: No content in JSON")
            return False

        return base64_gif_to_pdf(base64_data, output_pdf)

    except Exception as e:
        print(f"Error processing JSON: {e}")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: capture_webpage.py <input_file> <output_pdf>")
        print("  input_file: GIF file or JSON file with base64 GIF data")
        sys.exit(1)

    input_file = sys.argv[1]
    output_pdf = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    # Determine input type
    if input_file.endswith('.json'):
        success = json_file_to_pdf(input_file, output_pdf)
    elif input_file.endswith('.gif'):
        success = gif_to_pdf(input_file, output_pdf)
    else:
        # Try to detect format
        with open(input_file, 'rb') as f:
            header = f.read(4)
        if header[:3] == b'GIF':
            success = gif_to_pdf(input_file, output_pdf)
        else:
            success = json_file_to_pdf(input_file, output_pdf)

    sys.exit(0 if success else 1)
