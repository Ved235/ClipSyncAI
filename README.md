# AI Video Editor for Valorant Kills

This AI-powered video editor simplifies creating montage clips from Valorant gameplay videos. Using a trained YOLO model, it automates kill detection, clip extraction, and final video generation.

## Features:

- **Kill Detection**: Automatically detects kills in Valorant gameplay videos using a custom-trained YOLO model.
- **Clip Extraction**: Extracts kill moments into individual clips for easy editing or direct use.
- **Montage Generation**: Syncs clips with music and adds transitions for a cinematic final video.
- **User-Friendly Interface**: Intuitive GUI for selecting files, managing settings, and monitoring progress.

## Requirements:

- Python 3.x
- Dependencies listed in `requirements.txt` (install using `pip install -r requirements.txt`)
- A trained YOLO model (`best.pt`)

## How to Use:

1. Launch the application.
2. Select a gameplay video file.
3. Detect kills using the AI model.
4. Extract kill clips automatically.
5. Add a music file and generate the final video.

## License:

This project is licensed under the [MIT License](LICENSE).
