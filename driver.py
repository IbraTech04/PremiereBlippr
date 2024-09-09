from DetectBlips import analyze_video_audio_activity


print(analyze_video_audio_activity(video_path=
    r"C:\Users\Cheha\Videos\2024-09-02 15-34-19.mp4",
    project_path=r"C:\Users\Cheha\Desktop\PremiereBlippr", 
    track_number=3,
    threshold=-50.0,
    chunk_size=None,
    fps=60,
    in_time=None,
    out_time=None
))
