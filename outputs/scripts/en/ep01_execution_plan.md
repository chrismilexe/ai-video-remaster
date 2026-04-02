# EP01 Execution Plan

## Episode

- Working ID: `ep01`
- Show Name: `The Outcome Code`
- Tagline: `A Practical System for Reading People, Pressure, and Timing`
- Working title: `Why Smart People Keep Making Bad Timing Decisions`
- Source topic: `易经的智慧01 阴阳之道`
- Primary language: `English`
- Secondary language later: `Spanish`

## Goal

Turn the existing Chinese source material into:

- 1 English long-form audio episode
- 1 non-face long-form visual podcast video
- 5 short clips for traffic
- 1 reusable production template for later episodes

## Core Promise

This episode should not feel like a lecture on Chinese philosophy.
It should feel like a practical reading of:

- why smart people still misread timing
- why more force often creates worse outcomes
- why anxiety can signal misalignment
- how old pattern logic helps people read pressure and consequences

## Input Files

- Chinese source text: `outputs/target_text.txt`
- Chinese transcript: `outputs/transcripts/易经的智慧01阴阳之道.srt`
- Existing English draft: `scripts/target_text_english_script.md`
- Reference voice text: `outputs/ref_text.txt`
- Reference voice audio: `outputs/reference.wav`

## Output Files

- English master script: `outputs/scripts/en/ep01_master.md`
- English audio sample: `outputs/audio/ep01_sample.wav`
- English full audio: `outputs/audio/ep01_full.wav`
- Visual script: `outputs/visuals/ep01_visual_script.md`
- Clip script pack: `outputs/clips/ep01_clips.md`
- Long video export: `outputs/videos/ep01_full.mp4`

## Production Steps

### Step 1. Clean the Chinese source

Task:
- Merge the transcript and source text into one clean Chinese source draft
- Remove repetition, filler, and weak oral noise
- Keep only the points that support one clear episode arc

Output:
- `outputs/scripts/zh/ep01_source_clean.txt`

Definition of done:
- One clear theme
- No transcript junk
- Easy to rewrite into spoken English

### Step 2. Rewrite the English script

Task:
- Use the new prompt in `docs/PROMPTS.md`
- Rewrite the existing English draft into a more actionable version
- Reduce abstract explanation
- Add modern-life examples
- Add reflection prompts and practical lines

Output:
- `outputs/scripts/en/ep01_master.md`

Definition of done:
- Strong hook in first 30 seconds
- At least 3 short-clip lines
- At least 2 practical takeaways
- No long academic passages

### Step 3. Mark audio performance notes

Task:
- Add pause marks where the cloned voice needs breathing room
- Mark emphasis words
- Split the script into generation chunks if needed

Suggested chunking:
- intro
- concept block 1
- concept block 2
- application block
- closing

### Step 4. Generate a 60-90 second sample

Task:
- Use `outputs/reference.wav` and `outputs/ref_text.txt`
- Generate only the opening 60-90 seconds first

Output:
- `outputs/audio/ep01_sample.wav`

Checklist:
- Does the English sound natural in your cloned voice?
- Are there awkward words or unnatural pauses?
- Is the speed right for contemplative content?

If no:
- edit script first
- then regenerate sample

### Step 5. Generate the full episode audio

Task:
- Render the full English episode after sample approval
- If needed, render in sections and merge later

Output:
- `outputs/audio/ep01_full.wav`

Quality bar:
- calm and premium
- not robotic
- not too fast
- clear emotional rhythm

### Step 6. Split into long video + clips

Task:
- Create one visual-podcast version
- Create five short clips with separate hooks

Clip directions:
1. `Why smart people still get timing wrong`
2. `When more force makes you lose`
3. `What anxiety is really telling you`
4. `Why pressure distorts judgment`
5. `How to read the result before it arrives`

### Step 7. Produce visuals

Long video:
- use the visual script
- use information layers, not only atmosphere
- reserve Seedance for hero shots and transitions

Short clips:
- stronger hook
- faster pacing
- clearer on-screen text

### Step 8. Publish and evaluate

Primary distribution:
- YouTube
- Spotify
- Apple Podcasts

Track:
- title CTR
- first 30-second retention
- average watch/listen duration
- saves
- comments
- which clip theme gets the best response

## Recommended Episode Shape

- Total audio length target: `8-10 min`
- Spoken word target: `1,050-1,250 words`
- Number of major sections: `4-5`

Suggested structure:
1. Hook: smart people still get timing wrong
2. Explain the pattern underneath force and misalignment
3. Show how this appears in work, pressure, and judgment
4. Give a practical way to read the situation earlier
5. Close with one memorable line and one decision prompt

## Editorial Reminders

- Do not over-explain mythology
- Keep old concepts only if they improve judgment
- Replace abstract grandeur with practical clarity
- Every strong line should sharpen pattern recognition
- The episode should create both trust and clip-worthy moments

## Go / No-Go Checklist

Go only if all are true:
- English script sounds human
- audio sample passes
- visual script exists before video production
- 5 clips are identified before long video editing
- the episode has at least one real-life use case for pressure, timing, or decisions
