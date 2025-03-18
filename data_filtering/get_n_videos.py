import json

NUM_VIDEOS = 20
with open('nlq_answers_only.json', 'r') as file:
    data = json.load(file)

n_videos = []
for i in range(NUM_VIDEOS):
    video = data["videos"][i]
    n_videos.append(video)

n_videos = {"videos": n_videos}
with open(f'nlq_answers_only_{NUM_VIDEOS}.json', 'w') as outfile:
    json.dump(n_videos, outfile, indent=2)
