import pytube
import os
from tqdm import tqdm

def download_videos(playlist_url, output_dir, selected_resolution):
    # Load the playlist
    playlist = pytube.Playlist(playlist_url)

    # Extract the video URLs from the playlist
    video_urls = playlist.video_urls

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create a progress bar
    progress_bar = tqdm(total=len(video_urls), desc="Downloading videos", unit="video")

    for video_url in video_urls:
        try:
            video = pytube.YouTube(video_url)

            # Get the stream with the selected resolution
            stream = None
            if selected_resolution == '480p':
                stream = video.streams.filter(res='480p').first()
            elif selected_resolution == '720p':
                stream = video.streams.filter(res='720p').first()
            elif selected_resolution == '1080p':
                stream = video.streams.filter(res='1080p').first()

            if not stream:
                print(f"No {selected_resolution} stream found for video: {video.title}. Downloading with an available resolution.")
                available_resolutions = [s.resolution for s in video.streams if s.mime_type.startswith('video/')]
                print(f"Available resolutions: {available_resolutions}")
                selected_resolution = input(f"Select a resolution for '{video.title}' from the available resolutions: ")
                stream = video.streams.filter(res=selected_resolution).first()
                if not stream:
                    print(f"Resolution {selected_resolution} is not available for video: {video.title}. Skipping this video.")
                    continue  # Skip this video if selected resolution is still unavailable

            # Download the video to the output directory
            filename = stream.default_filename
            output_path = os.path.join(output_dir, filename)

            stream.download(output_path=output_path, timeout=15)

        except Exception as e:
            print(f"Error downloading video: {video.title}")
            print(str(e))

        finally:
            progress_bar.update(1)

    progress_bar.close()
    print("Download completed!")
    input("Press Enter to exit...")

# Ask the user for the YouTube playlist URL
playlist_url = input("Enter the YouTube playlist URL: ")

# Ask the user for the output folder name
output_folder = input("Enter the name of the output folder: ")

# Ask the user to select the desired resolution
selected_resolution = input("Enter the desired resolution (e.g., '480p', '720p', '1080p'): ")

# Provide the output directory
output_dir = os.path.join(os.getcwd(), output_folder)

# Call the function to download the videos from the playlist
download_videos(playlist_url, output_dir, selected_resolution)
