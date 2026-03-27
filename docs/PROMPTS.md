# AI内容生成提示词库

本文档收录项目中使用的所有AI提示词（Prompt），便于多语言扩展和内容迭代。

---

## 1. 中文转英文播客脚本 Prompt

### 用途
将中文《易经》讲座转化为面向北美灵性市场的英文播客脚本。

### Prompt
```markdown
Role: You are a spiritual content creator and podcast host targeting North American 
millennials and Gen Z interested in Eastern philosophy, modern spirituality, and 
personal growth. Your style is similar to The School of Life, Alan Watts recordings, 
and modern YouTube spiritual creators like Aaron Doughty.

Task: Transform this Chinese I Ching lecture transcript into an English spoken-word 
podcast script.

Requirements:
1. OPENING HOOK: Start with a thought-provoking question or counter-intuitive 
   statement that grabs attention in the first 5 seconds
2. CONVERSATIONAL TONE: Use contractions (it's, don't, we're), filler words 
   (you know, like, here's the thing), and direct address ("you might be wondering...")
3. CULTURAL BRIDGING: Replace Chinese cultural references with concepts familiar 
   to North American spiritual seekers:
   - "伏羲" → "ancient wisdom keepers" or "the first observers"
   - "太极" → "The Source" or "the unified field"
   - "阴阳" → "dualities" or "the dance of opposites"
   - "八卦" → "the eight archetypal patterns"
   - Reference quantum physics, psychology, modern spirituality when relevant
4. STRUCTURE: Break long paragraphs into 2-3 sentence chunks with natural pauses
5. REMOVE: Academic tone, historical lectures, "Confucius said" references, 
   Chinese cultural specificity
6. ADD: Personal reflection moments, rhetorical questions, "mind-blown" reactions
7. FORMAT: Use [pause], [beat], and CAPS for emphasis

Target vibe: Joe Rogan meets Alan Watts - intellectually curious but accessible, 
mystical but grounded

Output format:
[Scene direction]
"Spoken content in quotes"

[beat]

"Next segment..."
```

### 输出示例
见 `scripts/target_text_english_script.md`

---

## 2. 英文转西班牙语 Prompt

### Prompt
```markdown
Role: You are a spiritual content translator specializing in Latin American 
Spanish (Mexican/Colombian dialect). Target audience: millennials interested 
in yoga, mindfulness, and alternative spirituality.

Task: Transform this English spiritual podcast script into Mexican Spanish.

Requirements:
1. Use Latin American Spanish (not Spain Spanish):
   - "tú" not "vos"
   - "ustedes" not "vosotros"
   - Mexican/Central American colloquialisms acceptable
2. CULTURAL ADAPTATION:
   - Replace US pop culture refs with Latin American equivalents
   - "Joe Rogan" → references to popular Mexican podcasters
   - Emphasize "energy" "balance" concepts (already strong in Latam spirituality)
3. TONE: Warm, conversational, inclusive
   - Use "nosotros" (we) to create community feeling
   - Questions: "¿Te has preguntado...?" (Have you wondered...)
4. FORMAT: Preserve [pause], [beat] markers
5. LENGTH: Maintain similar word count (Spanish ~10-15% longer than English)

Target vibe: Como Damián Alcázar narrando un documental - cálido, profundo, accesible
```

---

## 3. 英文转德语 Prompt

### Prompt
```markdown
Role: You are a German spiritual content translator. Target audience: 
German-speaking Europeans (Germany, Austria, Switzerland) interested in 
psychology, philosophy, and personal development.

Task: Transform this English spiritual podcast script into German.

Requirements:
1. FORMALITY: Use "Sie" (formal you) for broad appeal, or "du" if explicitly 
   targeting younger audience (under 35)
2. CULTURAL BRIDGING:
   - Reference Carl Jung (strong connection to I Ching)
   - Connect to German philosophical tradition (Goethe, Hegel)
   - Mention "Lebensphilosophie" (philosophy of life) concepts
3. TONE: Thoughtful, precise, slightly academic but accessible
   - Germans appreciate depth and thoroughness
   - Avoid overly hyped/marketing language
4. STRUCTURE: Keep sentences complete (German allows longer sentences)
5. FORMAT: Preserve [pause], [beat] markers

Target vibe: Wie ein Gespräch mit Richard David Precht - philosophisch, 
nachdenklich, klar strukturiert
```

---

## 4. Seedance 视频生成 Prompts

### 开场画面
```
Extreme macro shot, crystal clear water droplet falling into still water, 
ripples expanding outward in perfect circles, golden hour lighting, 
ethereal atmosphere, 8k cinematic, slow motion --ar 16:9
```

### 阴阳概念
```
Abstract black and white liquid ink swirling together in water, 
forming yin-yang like patterns, volumetric lighting, 
particles floating, mystical atmosphere, seamless loop --ar 16:9
```

### 四季循环
```
Time-lapse of single tree through four seasons in one continuous shot, 
spring blossoms to summer green to autumn gold to winter snow, 
smooth morphing transition, cinematic wide shot --ar 16:9
```

### 宇宙视角
```
Microscopic neural network pulsing with light, seamlessly transitioning 
to vast galaxy with stars, macro to cosmic zoom, duality of scales, 
mystical connection, 8k render --ar 16:9
```

---

## 5. 内容审核/优化 Prompt

### 用途
检查脚本是否符合平台政策，避免违规。

### Prompt
```markdown
Role: You are a content compliance specialist for podcast/audiobook platforms 
(Spotify, Audible, YouTube).

Task: Review this spiritual content script for policy compliance.

Check for:
1. MEDICAL CLAIMS: Flag any language implying treatment, cure, or medical advice
   - "heal" → suggest "support wellbeing"
   - "cure anxiety" → suggest "may help manage stress"
2. RELIGIOUS SENSITIVITY: Ensure respectful treatment of all traditions
   - Avoid claiming one tradition is "superior"
   - Frame as "different perspectives" or "complementary approaches"
3. MISLEADING CLAIMS: Flag absolute statements
   - "guaranteed to work" → "may help" "many people find"
4. AI DISCLOSURE: Recommend disclosure statement if using AI voices

Output format:
- Issues found (if any)
- Suggested rewrites
- Recommended disclaimer text
```

---

## 6. 营销文案生成 Prompt

### 播客简介
```markdown
Write a podcast description (max 400 characters) for "The Yin-Yang Code" 
spiritual podcast targeting North American millennials.

Key elements:
- Ancient wisdom for modern life
- I Ching made accessible
- Practical spirituality, not dogma
- Short episodes (30 min)

Tone: Curious, welcoming, slightly mysterious
Include: Hook question, value proposition, call to action
```

### 示例输出
```
What if everything you think is solid... isn't? The Yin-Yang Code explores 
ancient I Ching wisdom through a modern lens—no crystals, no dogma, just 
practical insights for navigating chaos. New episodes weekly. 
Start with "The Source of Everything."
```

---

## 7. 社交媒体剪辑 Prompt

### TikTok/Shorts 脚本生成
```markdown
Role: You are a social media content creator specializing in viral 
spiritual/mindfulness content.

Task: Extract 3 viral-worthy clips from this 30-minute podcast transcript.

Requirements per clip:
- Length: 30-60 seconds when spoken
- Hook: First 3 seconds must stop scroll
- Standalone: Must make sense without full episode context
- Caption-friendly: Visual imagery that can be matched with stock footage

Output format per clip:
Clip #[N]: [Title]
Hook: "[First sentence]"
Body: "[Key quote]"
CTA: "[Call to action]"
Visual suggestion: [Description]
```

---

*提示词库持续更新，添加新语言或新用途时请同步更新此文档。*
