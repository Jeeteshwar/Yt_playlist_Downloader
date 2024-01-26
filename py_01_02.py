import os
from tqdm import tqdm
from pytube import Playlist, YouTube

def download_videos(playlist_url, output_dir, selected_resolution, start_index, end_index, total_videos):
    # Load the playlist
    playlist = Playlist(playlist_url)

    # Extract the video URLs from the playlist
    video_urls = playlist.video_urls

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Ensure the end_index is within the correct range
    end_index = min(end_index, total_videos)

    # Create a progress bar
    progress_bar = tqdm(total=end_index - start_index + 1, desc="Downloading videos", unit="video")

    video_list = list(enumerate(video_urls, 1))
    for index, video_url in video_list[start_index - 1:end_index]:
        try:
            video = YouTube(video_url)

            # Print the serial number and title of the video
            print(f"{index}/{total_videos}. {video.title}")

            # Get the stream with the selected resolution
            stream = video.streams.filter(res=selected_resolution).first()

            if not stream:
                print(f"No {selected_resolution} stream found for video: {video.title}. Downloading with an available resolution.")
                stream = video.streams.first()
                if not stream:
                    print(f"No available stream found for video: {video.title}. Skipping this video.")
                    continue  # Skip this video if no stream is available

            # Download the video to the output directory
            filename = f"{index}_{video.title}.mp4"
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

# Load the playlist to get the total number of videos
playlist = Playlist(playlist_url)
total_videos = len(playlist.video_urls)
print(f"There are {total_videos} videos in the playlist.")

# Ask the user for the output folder name
output_folder = input("Enter the name of the output folder: ")

# Ask the user to select the desired resolution
selected_resolution = input("Enter the desired resolution (e.g., '480p', '720p', '1080p'): ")

# Ask the user to enter the range of videos to download
start_index, end_index = map(int, input(f"Enter the range of videos to download (e.g., 1-{total_videos}): ").split('-'))

# Provide the output directory
output_dir = os.path.join(os.getcwd(), output_folder)

# Call the function to download the videos from the playlist within the specified range
download_videos(playlist_url, output_dir, selected_resolution, start_index, end_index, total_videos)
