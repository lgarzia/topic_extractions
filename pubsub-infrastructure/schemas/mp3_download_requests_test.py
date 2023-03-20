# %%
import mp3_download_request_pb2

# %%

dir(mp3_download_request_pb2)
# %%
m = mp3_download_request_pb2.MP3DownloadRequest()
# %%
dir(m)
# %%
m.collection_id = '4656556'  
m.episode_id = '47557'
m.episode_url = 'http-I-will-download.ulr'
# %%
m.IsInitialized()
# %%
str(m)
# %%
m.SerializeToString()
# %%
m.ParseFromString(m.SerializeToString())
# %%
