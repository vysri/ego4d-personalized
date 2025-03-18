
import json
# Filter all json entries that have answers to all language queries

def has_all_filled_answers(video):
    if (len(video["clips"]) == 0):
        return False
    for clip in video["clips"]:
        if (len(clip["annotations"]) == 0):
            return False
        for annotation in clip["annotations"]:
            if (len(clip["annotations"]) == 0):
                return False
            if not all(query.get("answer") for query in annotation["language_queries"]):
                return False
    return True


with open('nlq_train.json', 'r') as file:
    data = json.load(file)

# Filter videos where all language_queries contain an "answer"
filtered_videos = [video for video in data["videos"] if has_all_filled_answers(video)]
filtered_data = {"videos": filtered_videos}

# Optionally, save the filtered data to a new file
with open('nlq_answers_only.json', 'w') as outfile:
    json.dump(filtered_data, outfile, indent=2)