# 🚀 Future Enhancements — Math Garden

A working plan for growing the game as Sophie moves into middle school.

---

## Adding new math topics (e.g., Grade 6+)

All topic content lives in **`math-garden.html`**. Each new topic needs three edits:

### 1. Add the topic to `BANK`

Find the `BANK` object near the top of the script and add a new entry:

```js
ratios: { name:"Ratios & Rates", emoji:"⚖️", items:[
  { q:"A recipe uses 2 cups of flour for every 3 cups of milk. How much flour for 9 cups of milk?",
    choices:["6 cups","4 cups","8 cups","3 cups"], answer:0,
    explain:"9 is 3 × 3, so multiply the flour too: 2 × 3 = 6 cups." },
  // ... more questions
]},
```

- `answer` is the index (0–3) of the correct choice — it can be at any position; the game shuffles choices.
- Aim for **9+ questions per topic** so the no-repeat logic has room to rotate.
- Write `explain` in a friendly, one-to-two sentence voice — it shows after every answer.

### 2. Add the key to `TOPIC_ORDER`

```js
const TOPIC_ORDER = ["volume","formula","area","shapes",
                     "fracdiv","fracmult","fracdivide","fracexpr","ratios"];
```

This makes the topic appear on the home screen and in "Surprise Me!" mixes.

### 3. Describe the topic in `topicNames` (inside `kimiGenerateQuestion`)

```js
ratios:"ratios, unit rates, and equivalent ratio tables for Grade 6",
```

This is what KIMI uses to generate fresh AI questions for the topic. Be specific —
name the skill and the number range, not just the topic title.

**Everything else is automatic:** coins, garden growth, shop, badges, streaks, and
question diagrams (diagrams appear whenever a question's text contains parseable
dimensions like "4 cm long, 3 cm wide, 2 cm tall" or "2/3 m by 3/4 m").

---

## Recommended workflow per grade level

1. **Drop the curriculum files into `resources/`** (e.g., Eureka/EngageNY Grade 6
   module docx files), like the current Module 4 & 5 files.
2. Ask Claude to read them and generate the question bank — one `BANK` entry per
   topic, grounded in the actual lessons.
3. Play-test 2–3 quizzes per topic; adjust wording or difficulty.
4. Commit and push to GitHub.

### Candidate Grade 6 topics (Eureka sequence)

| Topic key (suggested) | Content | Emoji idea |
|---|---|---|
| `ratios` | Ratios, unit rates, ratio tables | ⚖️ |
| `percent` | Percent of a quantity, fraction/decimal/percent conversions | 💯 |
| `divfrac2` | Fraction ÷ fraction (full division, not just unit fractions) | 🍰 |
| `negatives` | Integers, opposites, number line, absolute value | 🌡️ |
| `expressions` | Variables, evaluating expressions, one-step equations | 🔤 |
| `coordplane` | Coordinate plane, all four quadrants, distance | 🗺️ |
| `stats` | Mean, median, mode, dot plots | 📊 |
| `geometry6` | Area of triangles/polygons, surface area with nets | 📐 |

### Retiring old topics

Don't delete Grade 5 topics — they make great review. Options:
- Keep them all (the topic grid is a scrolling grid; it handles more entries).
- Or group by grade: add a `grade` field per BANK entry and a simple filter
  toggle on the home screen ("Grade 5 review / Grade 6").

---

## Other enhancement ideas (backlog)

- **Diagram support for new topics** — extend `questionViz()` with new patterns:
  number lines for integers, coordinate grids, percent bars, dot plots.
- **Difficulty levels** — easy/medium/hard per topic; harder questions earn more coins.
- **Daily quest** — "Answer 10 ratio questions today" for a bonus chest.
- **Garden expansion** — unlock a 6th and 7th plot at coin milestones.
- **More badges** — per-grade completion badges ("Grade 6 Graduate" 🎓).
- **Timed challenge mode** — optional countdown for extra coins (off by default).
- **Sound toggle** — a 🔊/🔇 button for quiet study time.
- **Progress report for parents** — per-topic accuracy summary from saved stats,
  so you can see which topics need more practice.

---

## Housekeeping notes

- The GitHub repo branch is **`main`** (github.com/leungadh/grade5_math_quiz).
- Git operations on this synced folder can leave stale `.lock` files; if git
  misbehaves, clear them first:
  `rm -f .git/*.lock .git/objects/maintenance.lock .git/objects/*/tmp_obj_*`
- `kimi-key.txt` and `progress.json` stay git-ignored — never commit them.
- After a new grade's questions go in, update the footer text and README topic list
  (they currently say "Grade 5 • Modules 4 & 5").
