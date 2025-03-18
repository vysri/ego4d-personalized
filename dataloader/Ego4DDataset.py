import torch
from torch.utils.data import Dataset, DataLoader
import re
import json

class NLQVideoQueryDataset(Dataset):
    def __init__(self, video_data):
        self.data = []
        for video in video_data["videos"]:
            video_uid = video["video_uid"]
            for clip in video["clips"]:
                annotations = clip["annotations"]
                for annotation in annotations:
                    for language_query in  annotation["language_queries"]:
                        query = language_query["query"]
                        answer = language_query["answer"]
                        answer = re.sub(r'^Answer \(Optional\):\s*', '', answer)
                        self.data.append({
                            "query": query,
                            "answer": answer,
                            "video_uid": video_uid,
                            "video_path": f'/data/ego4d/v2/full_scale/{video_uid}.mp4'
                    })

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        return item
    

## Usage example
# with open('../data/nlq_answers_only_20.json', 'r') as file:
#     videos = json.load(file)
# dataset = NLQVideoQueryDataset(videos)
# dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

# for batch_idx, entry in enumerate(dataloader):
#     print(entry)
    # print(f"{batch_idx} Video UID: {entry['video_uid']}, Query: {entry['query']}, Answer: {entry['answer']}")