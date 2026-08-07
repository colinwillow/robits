import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── clip lookup: match by MEANING, not by exact string ──
a="""        const _base=gltf.animations.find(a2=>!/^(left|right)$/i.test(a2.name||''));   // the exporter's neutral/rest take
        const _pin={}; if(_base)for(const tr of _base.tracks)_pin[tr.name]=tr.values;
        for(const nm of ['left','right']){ const cl0=gltf.animations.find(a2=>a2.name===nm); if(!cl0)continue;"""
b"""placeholder"""
b="""        // Match the steering takes by MEANING, not by an exact string. Exports rename them freely — this rig's two
        // revisions ship 'left'/'right' and 'left turn'/'right_turn' — and an exact-match lookup fails SILENTLY: no
        // clip, no pose, no error, and the bars simply never turn. Anything containing left/right is the turn take;
        // whatever contains neither is the neutral one.
        const _cn=(a2)=>String((a2&&a2.name)||'').toLowerCase().replace(/[^a-z]/g,'');
        const _isL=(a2)=>/left/.test(_cn(a2)), _isR=(a2)=>/right/.test(_cn(a2));
        const _base=gltf.animations.find(a2=>!_isL(a2)&&!_isR(a2));   // the exporter's neutral/rest take
        const _pick={left:gltf.animations.find(_isL), right:gltf.animations.find(_isR)};
        BIKE._turnNames={left:_pick.left&&_pick.left.name, right:_pick.right&&_pick.right.name, base:_base&&_base.name};
        const _pin={}; if(_base)for(const tr of _base.tracks)_pin[tr.name]=tr.values;
        for(const nm of ['left','right']){ const cl0=_pick[nm]; if(!cl0)continue;"""
assert s.count(a)==1
s=s.replace(a,b)

# ── grip lookup: same problem, same fix ──
a2="""  if(!BIKE._grips){ BIKE._grips={}; try{ BIKE._glb.traverse(o=>{ const nm=(o.name||'').toLowerCase(); if(nm==='hand_grip_l')BIKE._grips.l=o; else if(nm==='hand_grip_r')BIKE._grips.r=o; }); }catch(_){} }"""
b2="""  // Same lesson as the turn clips: exact node names do not survive a re-export (this rig went hand_grip_l/r ->
  // left_hand/right_hand between revisions), and a miss here is silent — the hands just stop reaching the bars.
  // Identify the grips by what they ARE: a hand/grip node, on a side. 'handlebars' contains 'hand' but has no side,
  // so it can never be mistaken for one.
  if(!BIKE._grips){ BIKE._grips={}; try{ BIKE._glb.traverse(o=>{ const nm=(o.name||'').toLowerCase().replace(/[^a-z0-9]/g,'');
    if(!/hand|grip/.test(nm))return;
    if(/left/.test(nm)||/l$/.test(nm)){ if(!BIKE._grips.l)BIKE._grips.l=o; }
    else if(/right/.test(nm)||/r$/.test(nm)){ if(!BIKE._grips.r)BIKE._grips.r=o; } }); }catch(_){} }"""
assert s.count(a2)==1
s=s.replace(a2,b2)

assert s.count('BUILD &#8734;-CMB1497')==1 and s.count('∞-CMB1497')==1
s=s.replace('BUILD &#8734;-CMB1497','BUILD &#8734;-CMB1498').replace('∞-CMB1497','∞-CMB1498')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
