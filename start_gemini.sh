#!/bin/bash
. ~/.bashrc
conda init
conda activate gemini
python3 /gscratch/ubicomp/zacharye/ego4d-personalized/video_uploader.py
