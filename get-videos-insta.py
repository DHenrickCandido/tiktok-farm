import instaloader
from tiktok_uploader.upload import upload_video
from tiktok_uploader.auth import AuthBackend as Auth_tiktok
import os
import glob

def download_latest_videos(users):
    L = instaloader.Instaloader()

    for user in users:
        profile_name = user
        profile = instaloader.Profile.from_username(L.context, profile_name)
        for post in profile.get_posts():
            try:
                L.download_post(post, user)
            except:
                pass


def fix_hashtag(content):
    content = content.strip()
    return content



def upload_tiktok_video(video_file_name, desc_file_name, cookie_file="cookies.txt"):

    auth = Auth_tiktok(cookies=cookie_file)

    with open("uploaded_videos.txt", "r") as file:
        content = file.read()

        if video_file_name in content:
            print("video already uploaded")
            return

        else:
            upload_video(video_file_name,
                    description=desc_file_name,
                    cookies=cookie_file)
            with open("uploaded_videos.txt", 'a') as file:
                file.write(video_file_name)

def get_video_to_upload(user):
    files_txt = glob.glob(os.path.join(user, "*.txt"))
    files_mp4 = glob.glob(os.path.join(user, "*.mp4"))

    files_mp4_sorted = sorted(files_mp4, key=lambda x: os.path.basename(x))
    files_txt_sorted = sorted(files_txt, key=lambda x: os.path.basename(x))

    for file_mp4, file_txt in zip(files_mp4_sorted, files_txt_sorted):
        with open("uploaded_videos.txt", "r") as f:
            content = f.read()
            if file_mp4 in content:
                pass
            else:
                video_file_name = file_mp4
                with open(file_txt, "r") as f:
                    desc = f.read()
                    desc = fix_hashtag(desc)
                desc_file_name = desc

    return video_file_name, desc_file_name

def main():
    # users = ["hl.1mp", "sapphicprint", "k_pop._edits._", "kchrated", "ateezstage", "akipeeeeeeee", "_.hii_rixky._", "jihyo.jypt", "_kpop_._addict", "kpopgirls.stan"]
    users = ["onlylesserafimm"]
    # download_latest_videos(users)
    
    for user in users:
        video_file_name, desc_file_name = get_video_to_upload(user)
        upload_tiktok_video(video_file_name=video_file_name, desc_file_name=desc_file_name)

if __name__ == "__main__":
    main()
