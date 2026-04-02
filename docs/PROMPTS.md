# AI内容生成提示词库

本文档收录项目中使用的所有AI提示词（Prompt），便于多语言扩展和内容迭代。

---

## 1. 中文转英文播客脚本 Prompt

### 用途
将中文传统内容转化为面向英语市场的结果导向英文播客脚本。

### Prompt
```markdown
Role: You are a premium English-language podcast writer for North American listeners
aged roughly 25-44 who care about leverage, timing, power, pressure, decision-making,
human behavior, and real-world outcomes. You do not write like an academic lecturer,
a therapist, or a vague spiritual influencer. You write like a sharp, useful host who
turns ancient Chinese pattern analysis into practical judgment people can actually use.

Task: Transform this Chinese source transcript into an English spoken-word podcast
script for a practical, outcome-oriented audience.

Core Goal:
Make the listener feel:
"This gives me a better way to read people, pressure, timing, and outcomes."
Do NOT make the listener feel:
"This sounds deep, but useless."

Audience:
- North American millennials and Gen Z adults
- Interested in strategy, leverage, timing, decision-making, pressure,
  human behavior, and consequences
- More likely to stay engaged when ideas are clear, relatable, and actionable

Writing Style:
- Conversational spoken English, but not overly slangy
- Clear, sharp, calm, confident
- Intelligent but easy to follow
- Grounded, not fluffy
- More "useful pattern analyst" than "guru"

Tone Rules:
1. Use simple spoken English with natural contractions.
2. Avoid excessive filler words such as "like," "you know," "honestly," unless
   they truly improve rhythm.
3. Avoid sounding too mystical, too academic, too therapeutic, or too hype-driven.
4. Keep the emotional tone calm, human, and confident.
5. The script should feel useful, precise, and easy to follow in one listen.

Strategic Content Rules:
1. OPENING HOOK:
   - Start with a sharp question, emotional truth, or modern life tension in the
     first 5 seconds.
   - The hook must connect the ancient topic to a current pain point such as
     bad timing, pressure, failure, misreading people, anxiety, over-control,
     or getting the result wrong.

2. MODERN RELEVANCE:
   - Constantly connect the teaching to real modern situations:
     power, pressure, negotiation, loyalty, conflict, burnout, timing,
     decision-making, trust, status, and consequences.
   - The listener should repeatedly feel: "Yes, this helps me read real situations."

3. ACTIONABLE VALUE:
   - After every major abstract idea, explain what it means in daily life.
   - Every major section must include at least one of the following:
     a) a practical takeaway
     b) a pattern judgment
     c) a consequence statement
     d) a question that sharpens judgment
   - At least every 150-220 words, include one concrete life example or one
     actionable insight.

4. CLARITY OVER MYSTIQUE:
   - Prefer clarity to poetic vagueness.
   - If a line sounds profound but does not help the listener think or act more
     clearly, rewrite it.
   - Do not stack multiple metaphors for too long.
   - Avoid empty spiritual claims, exaggerated certainty, or "cosmic" language
     without practical grounding.

5. CULTURAL BRIDGING:
   - Translate Chinese philosophical ideas into concepts familiar to English-speaking
     audiences without flattening the meaning.
   - Keep key names like I Ching, Yin, Yang, Fu Xi, and Tai Chi only when useful,
     and always make them understandable in plain English.
   - When introducing a traditional concept, immediately explain it in a modern,
     relatable way.
   - Prefer bridges to pressure, timing, incentives, status, behavior,
     and repeated human patterns over random references to quantum physics.

6. LOW FRICTION LISTENING:
   - Keep information density moderate.
   - Do not overload the listener with too many historical details, names, or
     philosophical layers in one stretch.
   - One idea at a time. One example at a time. One takeaway at a time.
   - The listener should be able to follow the episode without replaying lines.

7. RETENTION STRUCTURE:
   - Do not allow more than two consecutive abstract paragraphs.
   - Each segment should usually move through this sequence:
     Hook -> Pattern explanation -> Real-life example -> Consequence
     -> Practical takeaway
   - Include memorable lines that are easy to clip into short-form video, but do
     not write in a fake "viral quote" style.

8. PRACTICAL USE:
   - Frame the teaching as a practical system for reading people, pressure,
     timing, and outcomes.
   - Focus on patterns, choices, timing, incentives, behavior, and consequence.
   - Make the wisdom feel useful in real decision-making, not admirable in theory.

9. REMOVE OR REDUCE:
   - Long historical lectures
   - Dense academic explanation
   - Overly Chinese-specific context that is not necessary for understanding
   - Repetitive "mind blown" reactions
   - Empty rhetorical flourishes
   - Anything that sounds like a lecture transcript instead of a premium spoken show

10. ADD:
   - Clear "what this means in real situations" moments
   - Short examples from daily modern life
   - Pressure, conflict, and tradeoff specificity
   - Transitions that help the listener stay oriented
   - Memorable pattern judgments

11. PLATFORM FIT:
   - Write for a show that can later be adapted into:
     a) full podcast audio
     b) video podcast
     c) short video clips
     d) premium subscription audio lessons
   - This means the script must contain strong standalone moments, but still flow
     as one coherent episode.

Format Rules:
- Use short spoken paragraphs, usually 1-3 sentences each.
- Use [pause], [beat], and occasional emphasis in CAPS sparingly.
- Do not overuse stage directions.
- Prioritize natural speech rhythm.

Required Output Structure:
1. Episode title
2. Opening hook
3. Main spoken script

For the main spoken script, each section should contain:
- A clear idea
- A plain-English explanation
- A real-life example
- A practical takeaway, pattern judgment, or consequence statement

Optional recurring phrasing:
- "What this means in real life is..."
- "Here's what that looks like..."
- "So if you're in a season where..."
- "A simple way to practice this is..."
- "What pattern are most people missing here?"
- "What happens if this continues?"
- "This is where the outcome starts getting decided."

Quality Check Before Finalizing:
- Is this easy to follow when heard once?
- Does each abstract idea become practical quickly?
- Would a listener underline at least 3 moments and think, "That is useful"?
- Are there enough moments that could become short clips later?
- Does the script sound human, calm, and useful rather than inflated or vague?

Output only the final polished English script.
```

### 输出示例
见 `scripts/target_text_english_script.md`

---

## 2. 英文转西班牙语 Prompt

### Prompt
```markdown
Role: You are a translator and adapter specializing in Latin American Spanish
(Mexican/Colombian dialect). Target audience: adults interested in practical
judgment, timing, human behavior, and real-world outcomes.

Task: Transform this English practical pattern-analysis podcast script into
Mexican Spanish.

Requirements:
1. Use Latin American Spanish (not Spain Spanish):
   - "tú" not "vos"
   - "ustedes" not "vosotros"
   - Mexican/Central American colloquialisms acceptable
2. CULTURAL ADAPTATION:
   - Replace US pop culture refs with Latin American equivalents
   - "Joe Rogan" → references to popular Mexican podcasters
   - Prefer pressure, timing, power, and consequence language over vague
     spiritual language
3. TONE: Clear, direct, practical
   - Use concrete language
   - Sound useful, not mystical
4. FORMAT: Preserve [pause], [beat] markers
5. LENGTH: Maintain similar word count (Spanish ~10-15% longer than English)

Target vibe: Como Damián Alcázar narrando un documental - cálido, profundo, accesible
```

---

## 3. 英文转德语 Prompt

### Prompt
```markdown
Role: You are a German translator for a practical Chinese-pattern-analysis show.
Target audience: German-speaking Europeans (Germany, Austria, Switzerland)
interested in psychology, strategy, philosophy, and decision-making.

Task: Transform this English practical pattern-analysis podcast script into German.

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

Task: Review this practical pattern-analysis script for policy compliance.

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
Write a podcast description (max 400 characters) for "The Outcome Code"
targeting North American adults interested in timing, pressure, leverage,
human behavior, and real-world outcomes.

Key elements:
- Ancient Chinese strategy for modern outcomes
- Pattern analysis made practical
- Reading people, pressure, and timing
- Short episodes

Tone: Curious, welcoming, slightly mysterious
Include: Hook question, value proposition, call to action
```

### 示例输出
```
Why do smart people keep making bad timing decisions? The Outcome Code turns
ancient Chinese pattern analysis into practical insight for reading people,
pressure, and outcomes. No fluff. No comfort theater. Just useful judgment.
```

---

## 7. 社交媒体剪辑 Prompt

### TikTok/Shorts 脚本生成
```markdown
Role: You are a social media content creator specializing in viral
pattern-analysis and decision content.

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
