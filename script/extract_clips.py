import cv2
import os

def extract_kill_clips(video_path: str, timestamps_file: str, buffer_duration: float = 0.5, max_gap: float = 0.5):
    """
    Extracts clips based on kill timestamps with a buffer before and after the kill event.
    """
    # Create the output directory for the clips
    output_dir = "kill_clips"
    os.makedirs(output_dir, exist_ok=True)

    # Load the video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Check if FPS is valid
    if fps <= 0:
        print("Error: Unable to retrieve FPS. Exiting.")
        exit()

    # Read timestamps from the file
    with open(timestamps_file, "r") as f:
        timestamps = [float(line.strip()) for line in f.readlines()]

    # Group the kills based on proximity (e.g., 4 seconds apart for the same kill sequence)
    grouped_timestamps = []
    current_group = []

    for i in range(len(timestamps)):
        if not current_group:
            current_group.append(timestamps[i])
        else:
            if timestamps[i] - current_group[-1] <= max_gap:
                current_group.append(timestamps[i])
            else:
                grouped_timestamps.append(current_group)
                current_group = [timestamps[i]]
    
    if current_group:
        grouped_timestamps.append(current_group)

    # Function to extract the kill clip with a buffer for a group of timestamps
    def extract_kill_clip(start_time, end_time, output_path):
        start_frame = max(int((start_time - buffer_duration) * fps), 0)
        end_frame = int((end_time) * fps)

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        start_frame = max(0, min(start_frame, total_frames - 1))
        end_frame = max(0, min(end_frame, total_frames - 1))

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

        for _ in range(start_frame, end_frame):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        out.release()

    # Create and save the clips
    clip_paths = []
    for idx, group in enumerate(grouped_timestamps):
        start_time = min(group)
        end_time = max(group)

        output_clip_path = os.path.join(output_dir, f"kill{idx + 1}.mp4")
        extract_kill_clip(start_time, end_time, output_clip_path)

        print(f"Kill clip for group {idx + 1} saved: {output_clip_path}")
        clip_paths.append(output_clip_path)

    cap.release()
    return clip_paths
