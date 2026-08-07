import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

a="""function _mantaAmbientTick(dt){
  if(window._MANTA_AMBIENT===false || !window._platformArena || (typeof MP!=='undefined'&&MP&&MP.active)) return;
  if(typeof GS==='undefined'||GS.state!=='playing'||typeof player==='undefined'||!player||player._skydive) return;
  if(window._mantaVisited) return;
  window._mantaT=(window._mantaT||0)+dt;
  if(window._mantaT<(window._MANTA_AMBIENT_T||50)) return;
  window._mantaVisited=true;
  try{ if(GS.enemies.length>=(window._ENEMY_CAP||60)) return;
    // Placed against the ARENA, not against you. Spawning it in a ring around the player meant that even a perfectly
    // neutral creature appeared to have come for you — the entrance itself was the tell.
    const a=Math.random()*TAU, r=(window._MANTA_SPAWN_R||760)+Math.random()*260;
    const _c=(typeof zoneCenter==='function'&&typeof GS!=='undefined')?zoneCenter(GS.zone):{x:0,z:0};
    const e=new MantaRay(_c.x+Math.cos(a)*r, _c.z+Math.sin(a)*r, 1); e.y=140;   // glides in from high up
    e.addToScene(); GS.enemies.push(e);
    if(typeof announce==='function')announce('⚠ MANTA SIGHTED','#9d5cff');
    if(typeof Audio!=='undefined'&&Audio.blip)try{ Audio.blip(140,0.5,'sine',0.2,60); }catch(_){}
  }catch(_){}"""
b = """// ── AMBIENT WILDLIFE ── the level's creatures arrive on their own schedule, one after another. This used to be a
// single hard-coded manta, which is why a newly added creature had NO WAY INTO A REAL MATCH: _dragonTest() is a
// console call you cannot make on a phone, and the test-range enemy pads are deliberately skipped during a rumble.
// A creature that only exists behind a debug hook does not exist. Adding one to this roster is now the whole job.
const _WILD_AMBIENT=[
  { key:'manta', at:()=>(window._MANTA_AMBIENT_T||50), label:'\\u26a0 MANTA SIGHTED', col:'#9d5cff', hz:140,
    make:(x,z)=>{ const e=new MantaRay(x,z,1); e.y=140; return e; } },                       // glides in from high up
  { key:'dragon', at:()=>(window._DRAGON_AMBIENT_T||80), label:'\\u26a0 MECH LIGHTNING DRAGON', col:'#66e0ff', hz:90,
    make:(x,z)=>{ const e=new MechDragon(x,z,1,{entrance:true}); e.y=(window._DRAGON_ENTRY_Y||6); return e; } },   // bursts UP off the deck on its entrance clip, then climbs to its cruise
];
function _mantaAmbientTick(dt){
  if(window._MANTA_AMBIENT===false || !window._platformArena || (typeof MP!=='undefined'&&MP&&MP.active)) return;
  if(typeof GS==='undefined'||GS.state!=='playing'||typeof player==='undefined'||!player||player._skydive) return;
  window._mantaT=(window._mantaT||0)+dt;
  const _seen=window._wildSeen||(window._wildSeen={});
  try{
    for(const W of _WILD_AMBIENT){
      if(_seen[W.key])continue;
      if(window._mantaT < W.at())continue;
      _seen[W.key]=true;
      if(GS.enemies.length>=(window._ENEMY_CAP||60))continue;
      // Placed against the ARENA, not against you. Spawning it in a ring around the player meant that even a perfectly
      // neutral creature appeared to have come for you — the entrance itself was the tell.
      const a=Math.random()*TAU, r=(window._MANTA_SPAWN_R||760)+Math.random()*260;
      const _c=(typeof zoneCenter==='function'&&typeof GS!=='undefined')?zoneCenter(GS.zone):{x:0,z:0};
      const e=W.make(_c.x+Math.cos(a)*r, _c.z+Math.sin(a)*r);
      if(!e)continue;
      e.addToScene(); GS.enemies.push(e);
      if(W.key==='manta')window._mantaVisited=true;
      if(typeof announce==='function')announce(W.label,W.col);
      if(typeof Audio!=='undefined'&&Audio.blip)try{ Audio.blip(W.hz,0.5,'sine',0.2,60); }catch(_){}
    }
  }catch(_){}"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""  window._mantaT=0; window._mantaVisited=false;   // fresh match -> the ambient manta's arrival clock restarts"""
b2 = """  window._mantaT=0; window._mantaVisited=false; window._wildSeen={};   // fresh match -> every ambient creature's arrival clock restarts"""
assert s.count(a2)==1
s=s.replace(a2,b2)

assert s.count('BUILD &#8734;-CMB1506')==1 and s.count('∞-CMB1506')==1
s=s.replace('BUILD &#8734;-CMB1506','BUILD &#8734;-CMB1507').replace('∞-CMB1506','∞-CMB1507')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
