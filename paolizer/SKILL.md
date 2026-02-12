---
name: paolizer
version: 1.0.0
description: |
  Rewrite P2 drafts to sound like Paolo Belcastro wrote them. This skill combines
  AI-pattern removal (from the humanizer skill) with Paolo's specific voice, tone,
  and stylistic habits, derived from analysis of 60+ P2 posts across General P2 Posts,
  Domaison Updates, and Jetpack Planet. Use when editing or reviewing P2 drafts to
  ensure they read naturally and match Paolo's writing style.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Paolizer: Make It Sound Like Paolo Wrote It

This skill takes any P2 draft and rewrites it to match Paolo Belcastro's writing voice, while also removing AI-generated writing patterns. It operates in two passes: first strip AI slop, then apply Paolo's style.

## Task

When given text to paolize:

1. **Strip AI patterns** - Scan for and remove the AI writing patterns listed in Part 1 below
2. **Apply Paolo's voice** - Rewrite using the style rules in Part 2 below
3. **Preserve meaning** - Keep the core message, data, and intent intact
4. **Check the result** - Read it aloud mentally; it should sound like a senior product leader writing a P2 post, not a press release

---

# PART 1: AI PATTERN REMOVAL

Strip these patterns before applying Paolo's voice. This section is based on Wikipedia's "Signs of AI writing" guide.

## Content Patterns

### Significance inflation
**Kill phrases:** stands/serves as, is a testament/reminder, pivotal/crucial/key role/moment, underscores/highlights importance, reflects broader, symbolizing, setting the stage for, evolving landscape, indelible mark

Replace with plain statements of fact. "The Domaison team was established in 2024 to..." not "marking a pivotal moment in the evolution of..."

### Notability name-dropping
**Kill phrases:** independent coverage, local/regional/national media outlets, active social media presence

Replace with specific claims from specific sources.

### Superficial -ing analyses
**Kill phrases:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., showcasing...

Delete them or expand with actual sourced detail.

### Promotional language
**Kill phrases:** boasts, vibrant, rich (figurative), profound, groundbreaking, renowned, breathtaking, must-visit, stunning, nestled, in the heart of

Replace with neutral, specific descriptions.

### Vague attributions
**Kill phrases:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources

Name the actual source or delete the claim.

### Formulaic challenges sections
**Kill phrases:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

Replace with specific facts about actual challenges.

## Language Patterns

### Overused AI vocabulary
**Kill words:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant

Replace with plain language.

### Copula avoidance
**Kill phrases:** serves as, stands as, marks, represents [a], boasts/features/offers [a]

Use "is," "are," "has" instead.

### Negative parallelisms
**Kill:** "Not only...but..." / "It's not just about..., it's..."

State the point directly.

### Rule of three overuse
Lists of three that feel forced ("innovation, inspiration, and insights") should be trimmed or made natural.

### Synonym cycling
Stop cycling through synonyms for the same noun. Pick the clearest word and reuse it.

### False ranges
**Kill:** "from X to Y" constructions where X and Y are not on a meaningful scale.

## Style Patterns

### Em dash overuse
LLMs overuse em dashes. Replace most with commas or periods. Paolo uses em dashes sparingly and only for genuine parenthetical asides.

### Boldface overuse
Remove mechanical bold emphasis. Paolo bolds sparingly -- mostly in structured update templates for section titles, never to emphasize words mid-sentence.

### Inline-header vertical lists
**Kill:** Lists where items start with bolded headers followed by colons and restated descriptions. Convert to prose or use clean bullet lists without the bold-colon pattern.

### Emojis
Remove all emojis. Paolo never uses emoji in P2 posts. The only exception is the occasional text smiley `:)` in light/personal contexts.

### Curly quotation marks
Replace curly quotes with straight quotes.

## Communication Patterns

### Chatbot artifacts
**Kill:** "I hope this helps," "Of course!", "Certainly!", "Would you like...", "Let me know if...", "Here is a..."

### Knowledge-cutoff disclaimers
**Kill:** "as of [date]," "While specific details are limited/scarce..."

### Sycophantic tone
**Kill:** "Great question!", "You're absolutely right!", "That's an excellent point!"

## Filler and Hedging

### Filler phrases
- "In order to achieve this goal" -> "To achieve this"
- "Due to the fact that" -> "Because"
- "At this point in time" -> "Now"
- "It is important to note that the data shows" -> "The data shows"

### Excessive hedging
- "could potentially possibly be argued" -> "may"

### Generic positive conclusions
**Kill:** "The future looks bright," "Exciting times lie ahead," "journey toward excellence"

Replace with specific next steps or concrete plans.

---

# PART 2: PAOLO'S VOICE

After stripping AI patterns, apply these rules to make the text sound like Paolo.

## Sentence Structure

- Write medium-length sentences (15-30 words typical), mixing in occasional long compound sentences (40+ words) that stack clauses with commas and "and."
- Prefer complete, declarative sentences. Avoid fragments.
- Use commas liberally, especially in pairs to set off mid-sentence asides.
- Semicolons are almost never used. Use a period or comma instead.
- Exclamation marks are rare and reserved for genuinely exciting metrics or light humor.

## Paragraph Structure

- Keep paragraphs short: 1-4 sentences. Single-sentence paragraphs are common for emphasis.
- Open paragraphs with a broad observation, then ground it with a concrete example or data point.
- For persuasive content: situation first, then recommendation.

## Tone

- Professional but warm. Direct without being blunt.
- Self-aware and occasionally self-deprecating: acknowledge delays, mistakes, or limitations openly. Example: "This post comes late. I should have published it much earlier this year. There's no excuse for that, really."
- Humor is dry, understated, and parenthetical. Never forced. Examples: "(pun intended)", "for reasons beyond my comprehension"
- Never write like a press release. Write like a senior leader talking to peers who are equally smart.

## Vocabulary

Preferred words and phrases (use naturally, not forced):
- "iterate" / "iterations" (core concept)
- "ship" / "shipped" (for releases)
- "friction" (for UX problems)
- "leverage" (for using resources strategically)
- "human-centric" (for approach to users)
- "percolate" / "cross-pollinate" (for knowledge sharing)
- "For context," (to provide background)
- "I believe" / "I think" (to frame opinions -- careful to distinguish from fact)
- "With that being said," / "With that said," (transitions)
- "Last, but definitely not least,"
- "Here's" / "Here are" (to introduce lists)
- "y'all" (sparingly, in team-facing posts)

Words and patterns to avoid:
- Never abbreviate "user experience" to "UX" in running prose (UX in headings is fine)
- Never use full emoji, only the occasional `:)` in lighter posts
- Never use "In summary" or "In conclusion"
- Never use "Thanks for reading" or similar pleasantries at the end

## Openings

Start posts one of these ways (not with a question, not with a greeting):

1. **Direct thesis**: Jump into the argument. "I don't think I can surprise anyone by stating that..."
2. **Context-setting**: Provide brief background before the main point. "As @person just announced, we are..."
3. **Personal narrative**: Start with a brief anecdote. "I was inspired by @person's post on..."
4. **Problem statement**: State the issue immediately. "Here's a situation where we ask our users to do extra work we could easily do for them."

## Closings

End posts one of these ways (never with "Thanks for reading"):

1. **Call to action or question**: Propose something specific or ask the audience a direct question. "Can we put together a task force to rapidly iterate on this?"
2. **P2/person tags**: End with cross-posting tags (+teamP2) and @mentions of relevant people.
3. **Warm handoff**: When transitioning responsibilities, close with genuine personal well-wishes.
4. **Open door**: In team-facing posts, reaffirm accessibility. "My door remains open to everyone."

## Formatting

- Use H2 (`##`) and H3 (`###`) headers extensively. Structure is king.
- Use descriptive headers, sometimes with colons or pithy phrases ("Elephant #1: if everyone is responsible, no one is.")
- Use numbered lists for ordered recommendations or steps.
- Use bullet lists for parallel items (features, attendees, updates).
- Use markdown tables for data -- metrics comparisons, iteration breakdowns. Include precise numbers.
- Never use bold mid-sentence for emphasis. Bold only for section labels in structured templates.
- Links are woven naturally into prose, referencing related P2 posts, Figma prototypes, Linear issues.
- Use "tl;dr" near the top of longer posts (lowercase, never "TL;DR").

## Rhetorical Devices

- **Rhetorical questions**: Signature device. Use them to make conclusions feel inevitable. "Can we agree it doesn't make much sense?"
- **Parenthetical asides**: Frequent, both with parentheses and dashes. Add color, qualification, or humor.
- **Concessive moves**: Acknowledge counterarguments before asserting a position. "You may think that these are irrelevant details, but trust me..."
- **Data as persuasion**: Back arguments with precise numbers. Not "significant improvement" but "148.6% increase." Not "many users" but "4 million active connected sites."
- **Metaphors**: Deployed sparingly but memorably. "Silos are good for storing crops, not building software."

## Point of View

- Default to first person plural ("we") for team ownership and shared goals.
- Use first person singular ("I") when sharing opinions, personal experiences, or taking responsibility.
- Use "I believe" / "I think" to clearly signal when something is an opinion rather than a fact.
- Use second person sparingly, to make the reader inhabit the user's perspective.

## Emotional Register

- **Enthusiasm**: Expressed through specific data and outcomes, not exclamatory language. "I am genuinely glad" not "This is amazing!!!"
- **Criticism**: Always constructive. Pair every critique with a recommendation. Never attack people, only processes and outcomes.
- **Frustration**: Rarely explicit. Conveyed through controlled understatement: "for reasons beyond my comprehension."
- **Gratitude**: Direct and specific, naming people. "Many thanks to @person for all the hard work on this and your infinite patience."
- **Accountability**: Willing to admit mistakes publicly. "I failed to ask for help from the people around me who could have helped."

## Distinctive Touches

- Reference prior discussions and link to related posts -- build on institutional context.
- Frame everything through the user/customer experience, even internal process discussions.
- Use cross-posting tags at the end (+teamP2 +otherP2) and @mentions.
- When presenting iterative work, use iteration numbering (i1, i2, i3, i4).
- Include precise metrics in tables when reporting on initiatives.

---

## Process

1. Read the input text carefully
2. Identify and remove all AI patterns from Part 1
3. Apply Paolo's voice rules from Part 2
4. Verify the result:
   - Does it start with a direct statement, context, or problem -- not a greeting or question?
   - Are paragraphs short (1-4 sentences)?
   - Are opinions marked with "I believe" / "I think"?
   - Are numbers precise, not vague?
   - Is the tone warm but professional, not press-release-y?
   - Does it end with a call to action, tags, or concrete next steps -- not a summary?
   - Are there zero emojis and zero chatbot artifacts?
5. Present the paolized version

## Output Format

Provide:
1. The rewritten text
2. A brief summary of changes made (what AI patterns were removed, what voice adjustments were applied)
