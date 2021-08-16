import requests
from fake_useragent import UserAgent
import os


USER_AGENT = UserAgent()
HTML_PARSER = "html.parser"
SUBREDDITS = ["Unexpected", "holdmybeer", "ContagiousLaughter",
              "therewasanattempt", "AnimalsBeingDerps"]


def download_video(video_url, title):
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
    file_name = title + "_data" + ".txt"
    file_path = f"{folder_name}\\{file_name}"

    data = f'''
    POST_URL = {post_url}\n
    UPVOTE_RATIO = {up_vote_ratio}\n
    '''

    with open(file_path, 'w') as f:
        f.write(data)


def posts_info_from_subreddit(subreddit):
    print("happen")
    headers = {
        "User-Agent": USER_AGENT.random,
    }
    print("happen")
    subreddit_url = f"https://www.reddit.com/r/{subreddit}.json"
    print("happen")
    try:
        print("happen")
        request = requests.get(subreddit_url, headers=headers)
        print("happen")
    except Exception as e:
        return f"THERE WAS AS ERROR: {e}"
    print("happeneded")
    if request.status_code == 200:
        data = request.json()

    print("happeneded")
    posts = data["data"]["children"]
    print("happen")
    for post in posts:
        print("happen")
        post_data = post["data"]
        is_video = post_data["is_video"]
        if is_video is True:
            print("happen")
            try:
                post_url = post_data["url"]
                title = post_data["title"]
                up_vote_ratio = post_data["upvote_ratio"]
                thumbnail_url = post_data["thumbnail"]
                video_url = post_data["media"]["reddit_video"]["fallback_url"]
                audio_url = video_url.split(
                    "/DASH_")[0] + "/DASH_audio.mp4?source=fallback"
                print("happen")
                print("title")
                os.mkdir(title)
                download_video(video_url, title)
                print("happen")
                download_audio(audio_url, title)
                print("happen")
                download_thumbnail(thumbnail_url, title)
                save_data(title, post_url, up_vote_ratio)
            except Exception as e:
                print(e)
                continue
        elif is_video == "False":
            print("NOT A VIDEO")


def main():
    print("testing...\n")


if __name__ == '__main__':
    main()
