from moviepy import VideoFileClip, AudioFileClip
import os
print(os.listdir())
# Load your video and audio files
video = VideoFileClip("downloads/vedio.mp4")
audio = AudioFileClip("downloads/song.mp3")

# Set the audio to the video
video_with_audio = video.with_audio(audio)

# Export the final video
video_with_audio.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")