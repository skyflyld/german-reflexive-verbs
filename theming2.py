#!/usr/bin/env python3
with open('index.html') as f:
    c = f.read()

# ===== 1. Fix slide-inner overflow so absolute tag isn't clipped =====
# Keep max-height for safety, remove overflow-y:auto
c = c.replace(
    'overflow-y:auto',
    ''
)
print("1️⃣ Removed overflow-y:auto from slide-inner")

# ===== 2. Replace slide-tag CSS with Präteritum style =====
old_tag = '''.slide-tag{display:inline-block;margin-bottom:18px;font-family:'Inter',sans-serif;font-size:.74rem;font-weight:600;letter-spacing:2.5px;text-transform:uppercase;padding:6px 20px;border-radius:20px;background:var(--schwarz);color:var(--gold)}'''

new_tag = '''.slide-tag{position:absolute;top:-16px;left:28px;font-family:'Inter',sans-serif;font-size:.7rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;padding:6px 18px;border-radius:3px;background:var(--schwarz);color:var(--weiss);z-index:2}
.slide-tag.red{background:var(--rot);color:var(--weiss)}
.slide-tag.gold{background:var(--gold);color:var(--schwarz)}'''

c = c.replace(old_tag, new_tag)
print("2️⃣ Replaced slide-tag CSS with Präteritum style (absolute, flat, colored)")

# ===== 3. Update each slide's tag with color classes =====
# slide 1 (Einstieg): default black
# slide 2 (Pronomen): red
# slide 3 (Tabelle): gold
# slide 4 (Typen): default black
# slide 5 (Position 1/2): red
# slide 6 (Position 2/2): gold
# slide 7 (Werkstatt): default black
# slide 8 (Karten): red

tags_map = [
    ('<div class="slide-tag">01 · Einstieg</div>', '<div class="slide-tag">01 · Einstieg</div>'),
    ('<div class="slide-tag">02 · Pronomen</div>', '<div class="slide-tag red">02 · Pronomen</div>'),
    ('<div class="slide-tag">03 · Tabelle</div>', '<div class="slide-tag gold">03 · Tabelle</div>'),
    ('<div class="slide-tag">04 · Typen</div>', '<div class="slide-tag">04 · Typen</div>'),
    ('<div class="slide-tag">05 · Position (1/2)</div>', '<div class="slide-tag red">05 · Position (1/2)</div>'),
    ('<div class="slide-tag">06 · Position (2/2)</div>', '<div class="slide-tag gold">06 · Position (2/2)</div>'),
    ('<div class="slide-tag">07 · Werkstatt</div>', '<div class="slide-tag">07 · Werkstatt</div>'),
    ('<div class="slide-tag">08 · Karten</div>', '<div class="slide-tag red">08 · Karten</div>'),
]

for old, new in tags_map:
    count = c.count(old)
    if count != 1:
        print(f"  ⚠️  Found {count}x '{old}' (expected 1)")
    c = c.replace(old, new)
print("3️⃣ Updated slide tags with alternating colors")

# ===== 4. Fix Ende page dark tags =====
# Make them flatter (border-radius:3px) and slightly wider padding
c = c.replace(
    '.slide.dark .tag{background:rgba(255,255,255,.1);color:var(--weiss);border-color:rgba(255,255,255,.2)}',
    '.slide.dark .tag{background:rgba(255,255,255,.1);color:var(--weiss);border-color:rgba(255,255,255,.25);border-radius:3px;padding:5px 16px;font-size:.72rem}'
)
print("4️⃣ Updated Ende dark tags to flat (border-radius:3px)")

# ===== 5. Cover tags are .cover .tag — keep them as pill, just slightly adjust =====
# Cover tags keep the pill style, no change needed

with open('index.html', 'w') as f:
    f.write(c)
print("\n✅ A方案 applied!")
