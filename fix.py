import re

with open('index.html') as f:
    c = f.read()

# ===== FIX 1: cursor:pointer on highlight-word =====
c = c.replace(
    '.highlight-word{padding:2px 5px;border-radius:3px;transition:all .2s;font-weight:600;cursor:default}',
    '.highlight-word{padding:2px 5px;border-radius:3px;transition:all .2s;font-weight:600;cursor:pointer}'
)
print("✅ Fix 1: cursor:pointer")

# ===== FIX 2: Color semantic unification =====
# Rule: Akk=red, Dat=gold, sich=gray
c = c.replace(
    '.highlight-word.typ-mich{background:rgba(244,162,97,.2);color:#b87333}',
    '.highlight-word.typ-mich{background:rgba(193,18,31,.08);color:var(--rot)}'
)
c = c.replace(
    '.highlight-word.typ-mir{background:rgba(193,18,31,.1);color:var(--rot)}',
    '.highlight-word.typ-mir{background:rgba(244,162,97,.15);color:var(--gold)}'
)
print("✅ Fix 2a: highlight colors unified")

# Dat class in pronoun cards
c = c.replace(
    '.pronoun-card .dat{font-size:.84rem;color:var(--grau);margin-top:2px}',
    '.pronoun-card .dat{font-size:.84rem;color:var(--gold);margin-top:2px}'
)
# .da class in comparison table
c = c.replace(
    '.comp-table .da{color:var(--grau);font-weight:500}',
    '.comp-table .da{color:var(--gold);font-weight:500}'
)
print("✅ Fix 2b: Dat color → gold in pronoun card + comp-table")

# Update explain map to reflect new colors
old_map = "const map={mich:'💡 ich → <strong>mich</strong> (Akk): 动作承受者是主语自己',mir:'💡 ich → <strong>mir</strong> (Dat): 涉及\"给自己\"做',sich:'💡 er/sie/es/sie → <strong>sich</strong>: 第三人称不分格'};"
new_map = "const map={mich:'🔴 ich → <strong>mich</strong> (Akk): 动作承受者是主语自己',mir:'🟡 ich → <strong>mir</strong> (Dat): 涉及给自己做',sich:'⚪ er/sie/es/sie → <strong>sich</strong>: 第三人称不分格'};"
c = c.replace(old_map, new_map)
print("✅ Fix 2c: explain box color legend")

# ===== FIX 3: Touch-zone + text selection =====
c = c.replace(
    '.touch-zone{position:fixed;top:0;bottom:0;width:25%;z-index:100}',
    '.touch-zone{position:fixed;top:0;bottom:0;width:13%;z-index:100}'
)
print("✅ Fix 3a: touch zones 25% → 13%")

# Add selectable class and content selection
c = c.replace(
    'body{font-family:',
    '.selectable{user-select:text;-webkit-user-select:text}\n'
    '.de,.zh,.pos-example,.beispiel-box,.scene-note,.pronoun-table,.comp-table,'
    '.werkstatt-ta,.game-back,.exit-ticket textarea,.exit-ticket input{'
    'user-select:text;-webkit-user-select:text}\n'
    'body{font-family:'
)
print("✅ Fix 3b: text selection enabled on content")

# Swipe protection
old_swipe = (
    "let tx=0;document.addEventListener('touchstart',e=>{tx=e.changedTouches[0].screenX})"
    ";document.addEventListener('touchend',e=>{let d=tx-e.changedTouches[0].screenX;if(Math.abs(d)>60){d>0?nextSlide():prevSlide()}});"
)
new_swipe = (
    "let tx=0;"
    "function isInteractive(el){"
    "while(el){"
    "if(el.tagName==='INPUT'||el.tagName==='TEXTAREA'"
    "||el.classList.contains('game-card')"
    "||el.classList.contains('chip')"
    "||el.classList.contains('pronoun-card')"
    "||el.classList.contains('scene-box')"
    "||el.classList.contains('start-btn')"
    "||el.classList.contains('nav-btn')"
    "||el.classList.contains('slide-tag')"
    "||el.closest('.game-btn-row'))return true;"
    "el=el.parentElement}return false}"
    "document.addEventListener('touchstart',e=>{tx=e.changedTouches[0].screenX});"
    "document.addEventListener('touchend',e=>{"
    "if(isInteractive(e.target))return;"
    "let d=tx-e.changedTouches[0].screenX;"
    "if(Math.abs(d)>60){d>0?nextSlide():prevSlide()}});"
)
c = c.replace(old_swipe, new_swipe)
print("✅ Fix 3c: swipe protection for inputs/cards/chips")

# ===== FIX 4: Position onblur + Enter =====
c = c.replace('oninput="cPos(this)"', 'onblur="cPos(this)"')
print("✅ Fix 4a: oninput → onblur")

enter_handler = (
    "\ndocument.addEventListener('keydown',function(e){"
    "if(e.key==='Enter'&&e.target.classList.contains('pos-input')){"
    "e.preventDefault();cPos(e.target)}});"
)
c = c.replace(
    "function cPos(el){",
    enter_handler + "\nfunction cPos(el){"
)
print("✅ Fix 4b: Enter key triggers position check")

# ===== FIX 5: Classify reasons =====
old_classify_list = (
    "const classifyList=[\n"
    "  {v:'sich beeilen',m:'赶紧，匆忙',t:'echt'},{v:'sich bedanken',m:'感谢',t:'echt'},\n"
    "  {v:'sich erinnern',m:'记起，想起',t:'echt'},{v:'sich auskennen',m:'熟悉，精通',t:'echt'},\n"
    "  {v:'sich waschen',m:'洗漱',t:'unecht'},{v:'sich anziehen',m:'穿衣服',t:'unecht'},\n"
    "  {v:'sich setzen',m:'坐下',t:'unecht'},{v:'sich verstecken',m:'躲藏',t:'unecht'}\n];"
)
new_classify_list = (
    "const classifyList=[\n"
    "  {v:'sich beeilen',m:'赶紧，匆忙',t:'echt',r:'beeilen 不能单独用: ✗ Ich beeile.'},"
    "{v:'sich bedanken',m:'感谢',t:'echt',r:'bedanken 不能单独用: ✗ Ich bedanke.'},\n"
    "  {v:'sich erinnern',m:'记起，想起',t:'echt',r:'erinnern + sich = 记起. 无 sich = 提醒别人.'},"
    "{v:'sich auskennen',m:'熟悉，精通',t:'echt',r:'aus|kennen 必须带 sich: ✗ Ich kenne aus.'},\n"
    "  {v:'sich waschen',m:'洗漱',t:'unecht',r:'可换宾语: ✓ Ich wasche das Kind.'},"
    "{v:'sich anziehen',m:'穿衣服',t:'unecht',r:'可换宾语: ✓ Ich ziehe den Mantel an.'},\n"
    "  {v:'sich setzen',m:'坐下',t:'unecht',r:'可换宾语: ✓ Ich setze das Kind hin.'},"
    "{v:'sich verstecken',m:'躲藏',t:'unecht',r:'可换宾语: ✓ Ich verstecke den Schatz.'}\n];"
)
c = c.replace(old_classify_list, new_classify_list)
print("✅ Fix 5a: reasons added to classify list")

# Update classify function to show reason
old_classify_fn = (
    "if(right){clsCorrect++;clsResults[type].push(item.v);"
    "fb.textContent='✅ Richtig!';fb.className='classify-fb ok'}\n"
    "  else{fb.textContent=`❌ Falsch! \"${item.v}\" 是${item.t==='echt'?'真':'假'}反身动词`;"
    "fb.className='classify-fb err'}"
)
new_classify_fn = (
    "if(right){clsCorrect++;clsResults[type].push(item.v);"
    "fb.innerHTML='✅ Richtig!<br><span style=font-size:.78rem;color:var(--grau)>'+item.r+'</span>';"
    "fb.className='classify-fb ok'}\n"
    "  else{fb.innerHTML='❌ Falsch!<br><span style=font-size:.78rem;color:var(--grau)>'+item.r+'</span>';"
    "fb.className='classify-fb err'}"
)
c = c.replace(old_classify_fn, new_classify_fn)
print("✅ Fix 5b: classify function shows reason")

# ===== FIX 6: Writing self-check checklist =====
old_charcount = '<div class="char-count" id="charCnt">0</div>'
new_charcount = (
    '<div class="char-count" id="charCnt">0</div>\n'
    '    <div class="self-check" style="margin-top:8px;padding:10px 14px;'
    'background:var(--papier);border-radius:var(--radius);'
    'border:1px solid var(--linie-fein)">\n'
    '      <div style="font-size:.78rem;font-weight:600;margin-bottom:4px">'
    '✅ 自检清单 <span style="font-weight:400;color:var(--grau-light)">'
    '（点击打勾，自我评估）</span></div>\n'
    '      <label style="display:flex;align-items:center;gap:6px;'
    'font-size:.76rem;color:var(--grau);margin:3px 0;cursor:pointer">\n'
    '        <input type="checkbox" '
    'onchange="this.parentElement.style.textDecoration=this.checked?\'line-through\':\'none\'"> '
    '至少用了 3 个反身动词\n'
    '      </label>\n'
    '      <label style="display:flex;align-items:center;gap:6px;'
    'font-size:.76rem;color:var(--grau);margin:3px 0;cursor:pointer">\n'
    '        <input type="checkbox" '
    'onchange="this.parentElement.style.textDecoration=this.checked?\'line-through\':\'none\'"> '
    '包含至少一个 Dativ (mir/dir)\n'
    '      </label>\n'
    '      <label style="display:flex;align-items:center;gap:6px;'
    'font-size:.76rem;color:var(--grau);margin:3px 0;cursor:pointer">\n'
    '        <input type="checkbox" '
    'onchange="this.parentElement.style.textDecoration=this.checked?\'line-through\':\'none\'"> '
    '包含带介词搭配 (sich freuen auf, sich interessieren für…)\n'
    '      </label>\n'
    '    </div>'
)
c = c.replace(old_charcount, new_charcount)
print("✅ Fix 6: writing self-check checklist")

# ===== DEAD CODE: compSection no longer exists on slide 2 =====
c = c.replace(
    "if(allRevealed===proData.length){setTimeout(()=>{document.getElementById('pronounTable').style.display='block'},300);setTimeout(()=>{document.getElementById('compSection').style.display='block'},600)}};",
    "if(allRevealed===proData.length){setTimeout(()=>{document.getElementById('pronounTable').style.display='block'},300)}};"
)
print("✅ Dead code: compSection reference removed from slide 2 JS")

with open('index.html', 'w') as f:
    f.write(c)
print("\n🎉 All 6 fixes applied!")
