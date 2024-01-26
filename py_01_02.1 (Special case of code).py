import pytube
import os
from tqdm import tqdm

# Define the function for downloading videos
def download_videos(playlist_url, output_dir, selected_resolution, start_index, end_index):
    # Load the playlist
    playlist = pytube.Playlist(playlist_url)

    # Extract the video URLs from the playlist
    video_urls = playlist.video_urls

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create a progress bar
    progress_bar = tqdm(total=end_index - start_index + 1, desc="Downloading videos", unit="video")

    video_list = list(enumerate(video_urls, 1))
    for index, video_url in video_list[start_index - 1:end_index]:
        try:
            video = pytube.YouTube(video_url)

            # Print the serial number and title of the video
            print(f"{index}. {video.title}")

            # Get the stream with the selected resolution
            stream = video.streams.filter(res=selected_resolution, progressive=True, file_extension='mp4').first()

            if not stream:
                print(f"No {selected_resolution} stream found for video: {video.title}. Downloading with an available resolution.")
                stream = video.streams.filter(progressive=True, file_extension='mp4').first()
                if not stream:
                    print(f"No available stream found for video: {video.title}. Skipping this video.")
                    continue  # Skip this video if no stream is available

            # Download the video with both video and audio to the output directory
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

if __name__ == "__main__":
    # Ask the user for the YouTube playlist URL
    playlist_url = input("Enter the YouTube playlist URL: ")

    # Fetch the number of videos from the playlist and display it to the user
    playlist = pytube.Playlist(playlist_url)
    num_videos = len(playlist.video_urls)
    print(f"There are {num_videos} videos in the playlist.")

    # Ask the user for the output folder name
    output_folder = input("Enter the name of the output folder: ")

    # Provide the available resolutions for the user to select from
    resolutions = ['480p', '720p', '1080p']
    print("Select the desired resolution: ")
    for i, resolution in enumerate(resolutions, 1):
        print(f"{i}. {resolution}")

    # Handle user resolution selection
    resolution_choice = int(input("Enter the number corresponding to your choice: "))
    selected_resolution = resolutions[resolution_choice - 1]

    # Ask the user to enter the range of videos to download
    start_index, end_index = map(int, input(f"Enter the range of videos to download (1-{num_videos}): ").split('-'))

    # Provide the output directory
    output_dir = os.path.join(os.getcwd(), output_folder)

    # Call the function to download the videos from the playlist within the specified range
    download_videos(playlist_url, output_dir, selected_resolution, start_index, end_index)
