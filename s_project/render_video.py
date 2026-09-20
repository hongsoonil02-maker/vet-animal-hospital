import os
import subprocess
import glob

def render_scene_video(frame_png, audio_mp3, out_mp4, pad_sec=1.5):
    # Use ffmpeg to loop image and pad audio
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", frame_png,
        "-i", audio_mp3,
        "-filter_complex", f"[1:a]apad=pad_dur={pad_sec}[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        out_mp4
    ]
    print(f"Running ffmpeg for {os.path.basename(out_mp4)}...")
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Completed {out_mp4}")

def concat_videos(video_list, final_mp4):
    concat_txt = r"C:\Users\master\vet_animal_hospital\s_project\concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for v in video_list:
            # Replace backslashes for ffmpeg concat file
            clean_v = v.replace("\\", "/")
            f.write(f"file '{clean_v}'\n")
            
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        final_mp4
    ]
    print(f"Concatenating all scenes into {final_mp4}...")
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Concatenation complete!")

def main():
    base_dir = r"C:\Users\master\vet_animal_hospital\s_project"
    clips_dir = os.path.join(base_dir, "clips")
    os.makedirs(clips_dir, exist_ok=True)
    
    scene_videos = []
    for i in range(1, 8):
        frame = os.path.join(base_dir, "frames", f"scene_{i:02d}.png")
        audio = os.path.join(base_dir, "audio", f"scene_{i:02d}.mp3")
        clip = os.path.join(clips_dir, f"scene_{i:02d}.mp4")
        render_scene_video(frame, audio, clip, pad_sec=1.5)
        scene_videos.append(clip)
        
    final_output = os.path.join(base_dir, "S-NACF_고농축사료첨가제_제안_홍보영상_삼원팜텍.mp4")
    concat_videos(scene_videos, final_output)
    
    # Check final duration
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', final_output]
    total_dur = float(subprocess.check_output(cmd).decode().strip())
    mins = int(total_dur // 60)
    secs = int(total_dur % 60)
    file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"=== FINAL MASTER VIDEO CREATED ===")
    print(f"Path: {final_output}")
    print(f"Duration: {total_dur:.2f}s ({mins}분 {secs:02d}초)")
    print(f"File Size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    main()
