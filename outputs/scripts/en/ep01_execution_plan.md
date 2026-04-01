# EP01 Execution Plan

## Episode

- Working ID: `ep01`
- Working title: `The Yin-Yang Code: The Source of Everything`
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
It should feel like a modern explanation of:

- why life moves in cycles
- why force creates imbalance
- why timing matters more than control
- how Yin and Yang can help people understand anxiety, relationships, and decision-making

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
1. `Why people force life too hard`
2. `Balance is not 50/50`
3. `Anxiety as lost rhythm`
4. `When to push and when to wait`
5. `Yin and Yang as a decision framework`

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

- Total audio length target: `18-24 min`
- Spoken word target: `2,400-3,200 words`
- Number of major sections: `4-5`

Suggested structure:
1. Hook: life is not static
2. Explain Yin/Yang as living patterns
3. Show how imbalance appears in modern life
4. Give practical decision and relationship applications
5. Close with one memorable line and next-step reflection

## Editorial Reminders

- Do not over-explain mythology
- Keep Fu Xi only if immediately contextualized
- Replace abstract grandeur with practical clarity
- Every deep line should help the listener think or act more clearly
- The episode should create both trust and clip-worthy moments

## Go / No-Go Checklist

Go only if all are true:
- English script sounds human
- audio sample passes
- visual script exists before video production
- 5 clips are identified before long video editing
- the episode has at least one real-life use case for relationships, anxiety, or decisions
