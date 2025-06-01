import os
import subprocess
import pathlib
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def generate_final_montage(clips_folder: str, music_path: str, output_path: str):
    """
    Create a montage from existing clip files using vid_transition.py directly.
    
    Args:
        clips_folder: Folder containing the kill clips
        music_path: Path to the music file
        output_path: Path for the output video
    """
    # Get list of all clip files sorted by name
    clip_files = sorted([os.path.join(clips_folder, f) for f in os.listdir(clips_folder) 
                         if f.endswith(".mp4")])
    
    if len(clip_files) < 2:
        print(f"Error: Need at least 2 video clips to create transitions. Found {len(clip_files)} clips.")
        return
    
    print(f"Found {len(clip_files)} clips to process")
    
    # Temporary folder for transition outputs
    work_dir = pathlib.Path("temp_transitions")
    work_dir.mkdir(exist_ok=True)
    
    # List to store all clips for final concatenation
    clips_to_concat = []
    
    # Load first clip and get FPS for frame calculations
    first_clip = VideoFileClip(clip_files[0])
    fps = first_clip.fps if first_clip.fps else 30  # Default to 30 FPS if not available
    frames_to_drop = 8
    time_to_drop = frames_to_drop / fps  # Convert frames to time in seconds
    
    # Add the first clip (trimmed - remove last 8 frames)
    first_clip_trimmed = first_clip.subclip(0, first_clip.duration - time_to_drop)
    clips_to_concat.append(first_clip_trimmed)
    
    # Process each pair of consecutive clips with vid_transition.py
    for i in range(len(clip_files) - 1):
        clip1 = clip_files[i]
        clip2 = clip_files[i + 1]
        
        transition_output = work_dir / f"transition_{i}_{i+1}_merged.mp4"
        
        print(f"Creating transition between clip {i+1} and clip {i+2}...")
        
        # Select a transition type - you can change this or make it random
        transition_types = ['rotation', 'zoom_in', 'zoom_out', 'translation', 'translation_inv']
        transition_type = transition_types[i % len(transition_types)]
        
        # Call vid_transition.py directly
        cmd = [
            "python", "vid_transition.py",
            "-i", clip1, clip2,
            "--animation", transition_type,
            "--num_frames", "8",
            "--merge", "true",
            "--output", str(work_dir / f"transition_{i}_{i+1}")
        ]
        
        try:
            subprocess.run(cmd, check=True)
            
            if transition_output.exists():
                # Add the transition to our list
                transition_clip = VideoFileClip(str(transition_output))
                clips_to_concat.append(transition_clip)
                
                # Load the next clip and trim it (remove first 8 frames)
                next_clip = VideoFileClip(clip_files[i + 1])
                
                # If it's not the last clip, trim both ends (first 8 frames and last 8 frames)
                if i < len(clip_files) - 2:
                    # Intermediate clip: remove first 8 frames and last 8 frames
                    next_clip_trimmed = next_clip.subclip(time_to_drop, next_clip.duration - time_to_drop)
                    clips_to_concat.append(next_clip_trimmed)
                else:
                    # Last clip: only remove first 8 frames
                    next_clip_trimmed = next_clip.subclip(time_to_drop)
                    clips_to_concat.append(next_clip_trimmed)
                
                # Close the original next_clip as we're using the trimmed version
 
                
            else:
                print(f"Warning: Transition file {transition_output} was not created")
                # Fallback: add next clip with trimming
                next_clip = VideoFileClip(clip_files[i + 1])
                if i < len(clip_files) - 2:
                    next_clip_trimmed = next_clip.subclip(time_to_drop, next_clip.duration - time_to_drop)
                else:
                    next_clip_trimmed = next_clip.subclip(time_to_drop)
                clips_to_concat.append(next_clip_trimmed)

                
        except subprocess.CalledProcessError as e:
            print(f"Error creating transition: {e}")
            # Fallback: add next clip with trimming
            next_clip = VideoFileClip(clip_files[i + 1])
            if i < len(clip_files) - 2:
                next_clip_trimmed = next_clip.subclip(time_to_drop, next_clip.duration - time_to_drop)
            else:
                next_clip_trimmed = next_clip.subclip(time_to_drop)
            clips_to_concat.append(next_clip_trimmed)

    
    # Close the original first clip as we're using the trimmed version

    
    # Concatenate all clips
    print("Concatenating clips and transitions...")
    final_video = concatenate_videoclips(clips_to_concat, method="compose")
    
    # Add music
    print("Adding music...")
    audio_clip = AudioFileClip(music_path)
    
    # Adjust audio to match video duration
    audio_clip = audio_clip.subclip(0, min(audio_clip.duration, final_video.duration))
    
    # Set the audio for the final video
    final_video = final_video.set_audio(audio_clip)
    
    # Write the final video
    print("Writing final montage...")
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    # Clean up
    for clip in clips_to_concat:
        clip.close()
    
    print(f"Final montage saved at: {output_path}")
    
    # Clean up temporary files if needed
    # import shutil
    # shutil.rmtree(work_dir)

if __name__ == "__main__":
    # Example usage
    generate_final_montage(
        clips_folder="kill_clips",
        music_path="music.mp3",  # Replace with your music file
        output_path="final_montage.mp4"
    )