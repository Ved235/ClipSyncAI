import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def generate_final_montage(clips_folder: str, music_path: str, output_path: str):
    """
    Generate the final video montage by concatenating the extracted kill clips and syncing it with the provided music.
    """
    # Step 1: Load the music (audio) file
    audio_clip = AudioFileClip(music_path)

    # Step 2: Load all the extracted video clips
    clip_files = [os.path.join(clips_folder, f) for f in sorted(os.listdir(clips_folder)) if f.endswith(".mp4")]

    if not clip_files:
        print("Error: No video clips found in the specified folder.")
        return

    # Step 3: Load each clip and store them in a list
    video_clips = [VideoFileClip(clip_file) for clip_file in clip_files]

    # Step 4: Get the fps of the first clip
    fps = video_clips[0].fps

    # Step 5: Concatenate the video clips without transitions
    final_video = concatenate_videoclips(video_clips, method="compose")

    # Step 6: Adjust the music to the length of the video montage
    final_audio = audio_clip.subclip(0, final_video.duration)  # Trim music to match the video length

    # Step 7: Set the audio for the final video
    final_video = final_video.set_audio(final_audio)

    # Step 8: Write the final video with synchronized audio and the same fps as the input
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=fps)

    print(f"Final synchronized montage saved at: {output_path}")
