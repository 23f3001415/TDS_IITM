# Question 20: Extracting Audio and Transcripts

## Final Answer (submit this transcript)
No idea what you're supposed to do here, just pick the static version, so that's what we're gonna do. Basically, the idea is the static version contains all of FFmpeg in one .exe file, which for our purposes is the most convenient. So I would recommend that as well. Go ahead and download the latest version for whatever bitness your computer is, and you'll realize that what you end up with is an archive. Open the archive in an archive manager of some sort.

## ELI15 Step-by-Step (for a complete novice)
1. Open a terminal in your `20/` folder.
2. Download audio from the YouTube video:
   - `python -m yt_dlp -f "ba[abr<50]/worstaudio" --extract-audio --audio-format mp3 --audio-quality 32k -o "audio.%(ext)s" "https://www.youtube.com/watch?v=MPV7JXTWPWI"`
3. Cut only the required 30-second clip:
   - `ffmpeg -ss 00:02:00 -to 00:02:30 -i audio.mp3 -c copy segment.mp3`
4. Transcribe `segment.mp3` using `faster-whisper` or subtitles.
5. Copy the spoken text and submit it in the answer box.

## Files generated
- `audio.mp3`
- `segment.mp3`
- `video.en.vtt`
- `video.en-orig.vtt`
