# %%
import getpodcast

# %%
opt = getpodcast.options(
    date_from='2022-02-01',
    root_dir='./podcast')

podcasts = {
    "TalkPython": "https://talkpython.fm/episodes/rss"
}

# %%

getpodcast.getpodcast(podcasts, opt)