import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── CSS: the sun SETS. Rides the transition .sw-sun already declares, and beats the void-sky !important rule.
a="""body.sunset-black #synthwave-bg .sw-sky{opacity:0.10}"""
b = """/* ── THE SUN SETS, IT DOES NOT VANISH ──────────────────────────────────────────────────────────────────────────
   The sun is a DOM element inside #synthwave-bg. On deploy, _voidSunSet demotes that whole layer behind the canvas
   AND hands the scene an opaque gradient in the same breath, so the scene's own sky occludes the sun instantly - it
   pops out of existence in one frame. .sw-sun has carried a 1.2s opacity/transform transition the whole time; it
   simply never got the chance to run. body.sun-setting is added when DEPLOY is pressed, which is ~1.6s ahead of the
   handoff, so the sun sinks and fades on screen and there is nothing left to pop by the time the scene takes over.
   The !important beats body.void-sky's transform rule; killing the glow animation stops it fighting the fade. */
body.sun-setting #synthwave-bg .sw-sun{opacity:0 !important;animation:none !important;transform:translate(calc(-50% + var(--swPar,0px)),18%) scale(0.9) !important;transition:opacity var(--sunSetMs,1150ms) ease, transform var(--sunSetMs,1150ms) ease !important}
body.sunset-black #synthwave-bg .sw-sky{opacity:0.10}"""
assert s.count(a)==1
s=s.replace(a,b)

# ── start the set the moment DEPLOY is pressed, which is already ~1.6s ahead of the background handoff
a2="""  window._sunSetPending=true;
  try{ clearTimeout(window._sunSetT); }catch(_){}"""
b2 = """  // Start the SUN SETTING now. The gradient handoff below is deliberately deferred (see above) until the stage has
  // painted, which buys the sun ~1.6s of runway to sink and fade while the DOM layer is still the thing on screen.
  // By the time the scene's own sky takes over there is no sun left to pop.
  try{ if(window._SUN_SET_FADE!==false)document.body.classList.add('sun-setting'); }catch(_){}
  window._sunSetPending=true;
  try{ clearTimeout(window._sunSetT); }catch(_){}"""
assert s.count(a2)==1
s=s.replace(a2,b2)

# ── and it rises again whenever the menus come back, or the next deploy has no sun to set
a3="""  try{ if(name==='character'){ if(window._SUNSET!==false && !window._DRESS_MODE && window._SELECT_FULL_SKY===false)document.body.classList.add('sunset-select'); }"""
b3 = """  try{ document.body.classList.remove('sun-setting'); }catch(_){}   // back on a menu: the sun is up again, ready to set on the next deploy
  try{ if(name==='character'){ if(window._SUNSET!==false && !window._DRESS_MODE && window._SELECT_FULL_SKY===false)document.body.classList.add('sunset-select'); }"""
assert s.count(a3)==1
s=s.replace(a3,b3)

assert s.count('BUILD &#8734;-CMB1516')==1 and s.count('∞-CMB1516')==1
s=s.replace('BUILD &#8734;-CMB1516','BUILD &#8734;-CMB1517').replace('∞-CMB1516','∞-CMB1517')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
