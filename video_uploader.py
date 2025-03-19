from google import genai
from google.genai import types
import time
import json
from PIL import Image
from IPython.display import display, Markdown, HTML
import torch
from torch.utils.data import Dataset, DataLoader
import re
import json
from dataloader.Ego4DDataset import NLQVideoQueryDataset
import os



with open('../gemini.key', 'r') as file:
    GOOGLE_API_KEY = file.read()[:-1]

client = genai.Client(api_key=GOOGLE_API_KEY)

model_name = "gemini-2.0-flash" # @param ["gemini-1.5-flash-latest","gemini-2.0-flash-lite","gemini-2.0-flash","gemini-2.0-pro-exp-02-05"] {"allow-input":true, isTemplate: true}

def upload_video(video_file_name):
  video_file = client.files.upload(file=video_file_name)

  while video_file.state == "PROCESSING":
      print('Waiting for video to be processed.')
      time.sleep(10)
      video_file = client.files.get(name=video_file.name)

  if video_file.state == "FAILED":
    raise ValueError(video_file.state)
  print(f'Video processing complete: ' + video_file.uri)

  return video_file

with open('data/nlq_answers_only_20.json', 'r') as file:
    videos = json.load(file)
dataset = NLQVideoQueryDataset(videos)
dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

with open('output.json', 'r') as outfile:
    output_data = json.load(outfile)


for batch_idx, entry in enumerate(dataloader):
    print(f"{batch_idx} Video UID: {entry['video_uid']}")
    with open('output.json', 'r') as outfile:
        output_data = json.load(outfile)
    if entry['video_uid'][0] not in output_data:
        video = upload_video(entry['video_path'][0])
        output_data[entry['video_uid'][0]] = []
        ii = 0
        for query in entry['query']:
            prompt = "Here we have uploaded a video shot capturing the first-person perspective of an individual. You will now help the individual by answering their questions about the video. Here is the first question: "+ entry['query'][ii]
            answer = entry['answer'][ii]
            print(f"Video UID: {entry['video_uid'][0]}, Query: {prompt}, Answer: {answer}")
            ii += 1
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    video,
                    prompt,
                ]
            )
            model_output = {
                "query": prompt,
                "answer": answer,
                "response": response.text,
            }
            output_data[entry['video_uid'][0]].append(model_output)
        client.files.delete(name=video.name)
        with open('output.json', 'w') as outfile:
            json.dump(output_data, outfile)

   
# cache dataloader in case script crashes

# for batch_idx, entry in enumerate(dataloader):

#     print(entry)
#     print(f"{batch_idx} Video UID: {entry['video_uid']}")
#     entry['gemini_url'] = upload_video(entry['video_path'][0])
#     torch.save(dataloader, 'dataloader.pth')


