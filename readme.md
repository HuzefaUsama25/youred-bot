# youtube-reddit-video-bot

## Algorithm:

- when run:
- goto some sub reddits and get new posts

  - for each subrediit:
    - download json page `GET REQUEST`
    - find videos that havent been downloaded by checking downloaded_already.txt
    - check each post and append to new list if post is a video
      - for each video
        - extract:
          - video url
          - audio_url
          - authors
          - thumbnail
          - upvote ratio
        - download all of the following and save to folder:
          - video `GET REQUEST`
          - audio `GET REQUEST`
          - thumbnail `GET REQUEST`
        - merge video + audio
        - save url to downloaded_already.txt

- upload video to youtube:
  title: post_title
  thumbnail: reddit thumbnail of post + yellow text (which is the title)
