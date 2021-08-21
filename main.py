import requests
from fake_useragent import UserAgent
import os
import traceback


USER_AGENT = UserAgent()
HTML_PARSER = "html.parser"
SUBREDDITS = ["Unexpected", "holdmybeer", "ContagiousLaughter",
              "therewasanattempt", "AnimalsBeingDerps"]


def download_video(video_url, title):

    print("DOWNLOADING VIDEO")
    headers = {
        "User-Agent": USER_AGENT.random,
    }
    folder_name = title
    file_name = title + ".mp4"
    file_path = f"{folder_name}\\{file_name}"

    with requests.get(video_url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return file_path


def download_thumbnail(thumbnail_url, title):
    headers = {
        "User-Agent": USER_AGENT.random,
    }
    folder_name = title
    file_name = title + "_thumb" + ".jpg"
    file_path = f"{folder_name}\\{file_name}"

    with requests.get(thumbnail_url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return file_path


def download_audio(audio_url, title):
    headers = {
        "User-Agent": USER_AGENT.random,
    }
    folder_name = title
    file_name = title + "_audio" + ".mp4"
    file_path = f"{folder_name}\\{file_name}"

    with requests.get(audio_url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return file_path


def save_data(title, post_url, up_vote_ratio):
    folder_name = title
    up_vote_ratio = str(up_vote_ratio)
    file_name = title + f" [{up_vote_ratio}] " + "_data" + ".txt"
    file_path = f"{folder_name}\\{file_name}"

    data = f'''
    POST_URL = {post_url}\n
    UPVOTE_RATIO = {up_vote_ratio}\n
    '''

    with open(file_path, 'w') as f:
        f.write(data)


def join_video_audio(title, video_file, audio_file):
    command = f'''ffmpeg -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac "{title}\\{title}_final.mp4"'''
    os.system(command)


def posts_info_from_subreddit(subreddit):

    headers = {
        "User-Agent": USER_AGENT.random,
    }

    subreddit_url = f"https://www.reddit.com/r/{subreddit}.json"

    try:

        request = requests.get(subreddit_url, headers=headers)

    except Exception as e:
        print(traceback.format_exc())
        return f"THERE WAS AS ERROR: {e}"
    if request.status_code == 200:
        data = request.json()

    posts = data["data"]["children"]

    for post in posts:

        post_data = post["data"]
        is_video = post_data["is_video"]
        if is_video is True:

            try:
                post_url = post_data["url"]
                title = post_data["title"]
                up_vote_ratio = post_data["upvote_ratio"]
                thumbnail_url = post_data["thumbnail"]
                video_url = post_data["media"]["reddit_video"]["fallback_url"]
                audio_url = video_url.split(
                    "/DASH_")[0] + "/DASH_audio.mp4?source=fallback"

                chars_to_remove = [':', '*', '?', '"',
                                   '/', '\\', '<', '>', '|', "."]
                for char_to_remove in chars_to_remove:
                    title = title.replace(f"{char_to_remove}", "")

                title = title.encode('ascii', 'ignore').decode(
                    "ascii", "ignore")

                up_vote_ratio = int(float(up_vote_ratio) * 100)

                if up_vote_ratio > 95:
                    print(f"\n\n\n{title}")
                    os.mkdir(title)
                    save_data(title, post_url, up_vote_ratio)
                    video_file = download_video(video_url, title)
                    audio_file = download_audio(audio_url, title)
                    download_thumbnail(thumbnail_url, title)
                    join_video_audio(title, video_file, audio_file)

            except Exception as e:
                print(traceback.format_exc())
                continue
        elif is_video == "False":
            print("THIS POST IS NOT A VIDEO")


def main():
    print("testing...\n")


if __name__ == '__main__':
    main()
