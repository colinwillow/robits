import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()

a="""  try{ if(typeof _buildArmoryStation==='function')_buildArmoryStation((window._ARMORY_X!=null?window._ARMORY_X:0),(window._ARMORY_Z!=null?window._ARMORY_Z:-300)); }catch(e){ console.warn('armory',e); }   // boots live IN the armory catalog now — no separate station"""
b="""  try{ if(typeof _buildArmoryStation==='function')_buildArmoryStation((window._ARMORY_X!=null?window._ARMORY_X:0),(window._ARMORY_Z!=null?window._ARMORY_Z:-300)); }catch(e){ console.warn('armory',e); }   // boots live IN the armory catalog now — no separate station
  // ── THE BIKE, PARKED IN THE LEVEL ── it only ever existed inside the circuit zone, so there was no way to ride it in
  // an actual match. Park one beside the armory terminal: walk up and it offers the same right-stick tap-to-mount as
  // every other interact. _bikeDismount re-parks it wherever you step off, so it stays where you leave it.
  // window._ARENA_BIKE=false to leave it out; _ARENA_BIKE_X/_Z/_H to move it.
  try{ if(window._ARENA_BIKE!==false && typeof window._bikePark==='function'){
    window._bikePark((window._ARENA_BIKE_X!=null?window._ARENA_BIKE_X:((window._ARMORY_X!=null?window._ARMORY_X:0)+180)),
                     (window._ARENA_BIKE_Z!=null?window._ARENA_BIKE_Z:((window._ARMORY_Z!=null?window._ARMORY_Z:-300)+60)),
                     (window._ARENA_BIKE_H!=null?window._ARENA_BIKE_H:Math.PI), 0); } }catch(e){ console.warn('arena bike',e); }"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""  try{ if(window._platformArena){ window._platformArena=false; window._arenaVoid=false; window._platformCol=null;"""
b2="""  try{ if(window._ARENA_BIKE!==false && typeof BIKE!=='undefined' && !BIKE.riding && !BIKE._hop){ BIKE.park=null; window._nearBike=null; if(BIKE.grp)BIKE.grp.visible=false; } }catch(_){}   // the parked arena bike leaves with the arena (riding/mid-hop is left alone — tearing the bike out from under a rider is worse than a stray mesh)
  try{ if(window._platformArena){ window._platformArena=false; window._arenaVoid=false; window._platformCol=null;"""
assert s.count(a2)==1
s=s.replace(a2,b2)
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
