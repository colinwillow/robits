import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── park: remember HOME (where the level put it) so a regenerated bike comes back somewhere sane ──
a="""  BIKE.grp.visible=true; BIKE.riding=false; BIKE._hop=null;
  BIKE.park={x:x||0, z:(z||0), h:(h||0), y:(y||0)};
  return BIKE.park;"""
b="""  BIKE.grp.visible=true; BIKE.riding=false; BIKE._hop=null;
  BIKE.park={x:x||0, z:(z||0), h:(h||0), y:(y||0)};
  if(!BIKE._home)BIKE._home={x:BIKE.park.x, z:BIKE.park.z, h:BIKE.park.h, y:BIKE.park.y};   // the FIRST park of a level is its home: a wreck regenerates there, not wherever it happened to die
  if(BIKE.hp==null)BIKE.hp=(BIKE.maxHp=(window._BIKE_MAX_HP||45));
  return BIKE.park;"""
assert s.count(a)==1
s=s.replace(a,b)

# ── a destroyed bike must not re-park itself when the knock-off dismounts you ──
a2="""  if(BIKE.grp){ if(window._BIKE_REPARK!==false && player){ _bikePark(player.wx+Math.sin(player._skHeading||0)*26, player.wz+Math.cos(player._skHeading||0)*26, player._skHeading||0, 0); }"""
b2="""  if(BIKE.grp){ if(window._BIKE_REPARK!==false && player && !BIKE.dead){ _bikePark(player.wx+Math.sin(player._skHeading||0)*26, player.wz+Math.cos(player._skHeading||0)*26, player._skHeading||0, 0); }"""
assert s.count(a2)==1
s=s.replace(a2,b2)

# ── THE DAMAGE LOOP ── inserted just before _bikeTick
a3="""// per-frame: park the bike under the rider, bank it with the lean, pitch it with the carve, run the FX
function _bikeTick(dt){
  try{ _bikeEjectBtn(); }catch(_){}
  if(!player){ return; }"""
b3="""// ════════════════════════════════════════════════════════════
//  BIKE DAMAGE — the vehicle is the thing that takes the hits, not the rider on it. Shots go into its health;
//  it smokes as it fails, then it detonates, shatters, throws you clear, and rebuilds itself on a timer at the
//  spot the level parked it. Explosives/melee still throw you off directly (the mount knock-off rule) — this is
//  what happens to the MACHINE. window._BIKE_HP=false disables the whole system (bike becomes indestructible).
// ════════════════════════════════════════════════════════════
window._bikeDamage=function(dmg,col){ try{
  if(window._BIKE_HP===false||BIKE.dead||!BIKE.riding)return false;
  if(BIKE.hp==null)BIKE.hp=(BIKE.maxHp=(window._BIKE_MAX_HP||45));
  BIKE.hp=Math.max(0,BIKE.hp-(dmg||1)*(window._BIKE_DMG_MUL||1));
  BIKE._hitFlash=(window._BIKE_HIT_FLASH||0.18);
  const g=BIKE.grp; if(g){ try{ if(typeof ps!=='undefined'){ ps.spark(g.position.x+rand(-8,8), g.position.z+rand(-8,8), [1,0.75,0.25], g.position.y+12); } }catch(_){} }
  try{ if(typeof Audio!=='undefined'&&Audio.blip)Audio.blip(180,0.05,'square',0.1,90); }catch(_){}
  if(BIKE.hp<=0){ _bikeBlowUp(); return true; }   // absorbed AND destroyed — the blast itself is what throws you off
  return true;
}catch(_){ return false; } };

function _bikeBlowUp(){ try{
  if(BIKE.dead)return; BIKE.dead=true; BIKE.hp=0;
  const g=BIKE.grp, x=g?g.position.x:player.wx, y=(g?g.position.y:0)+10, z=g?g.position.z:player.wz;
  // SHATTER + FIREBALL — the same vox/debris machinery every other explosion in the game uses, so it reads as one world
  try{ if(window._voxExplosion)window._voxExplosion(x,y,z,(window._BIKE_BOOM_SCALE||34),{upKick:(window._BIKE_BOOM_UP||60)}); }catch(_){}
  try{ if(window._voxEmit)window._voxEmit(x,y,z,(window._BIKE_SHARDS||46),(window._BIKE_SHARD_COL!=null?window._BIKE_SHARD_COL:0x9fe8ff),(window._BIKE_SHARD_SIZE||5),16,14); }catch(_){}   // the chassis itself, coming apart
  try{ if(typeof spawnDebris==='function')spawnDebris(x,z,(window._BIKE_DEBRIS||8),1.4); }catch(_){}
  try{ if(typeof ps!=='undefined'){ ps.ring(x,z,[1,0.6,0.2],34,220,y); ps.burst(x,z,[1,0.85,0.4],34,220,y); } }catch(_){}
  try{ if(typeof gridSheetsBlast==='function')gridSheetsBlast(x,y,z,(window._BIKE_BOOM_PW||22),(window._BIKE_BOOM_R||130),0xff9a3c,0.8); }catch(_){}
  try{ if(window._boomSfx)window._boomSfx('large',1,x,z,(window._BIKE_BOOM_VOL||1)); }catch(_){}
  try{ if(typeof addTrauma==='function')addTrauma(0.35); }catch(_){}
  // THROW THE RIDER CLEAR. blast:true so the mount knock-off rule launches him for certain; BIKE.dead is already set,
  // so the dismount inside knock() will NOT re-park the wreck.
  try{ if(player&&BIKE.riding){ const a=Math.random()*Math.PI*2;
    player.knock(Math.cos(a),Math.sin(a),(window._BIKE_BOOM_KB||16),(window._BIKE_BOOM_LIFT||520),26,{blast:true}); } }catch(_){}
  try{ if(player){ player._bikeMode=false; player._onHoverboard=false; } }catch(_){}
  BIKE.riding=false; BIKE._hop=null; BIKE.park=null; window._nearBike=null;
  if(g)g.visible=false;
  BIKE.regenT=(window._BIKE_REGEN_SEC||14);
  try{ if(typeof announce==='function')announce('BIKE DESTROYED — REBUILDING','#ff6a3c'); }catch(_){}
}catch(_){} }

function _bikeRegen(){ try{
  BIKE.dead=false; BIKE.hp=(BIKE.maxHp=(window._BIKE_MAX_HP||45)); BIKE._smokeT=0;
  const H=BIKE._home||{x:0,z:0,h:0,y:0};
  _bikePark(H.x,H.z,H.h,H.y||0);
  try{ if(typeof ps!=='undefined'){ ps.ring(H.x,H.z,[0.3,0.92,1],28,150,10); ps.burst(H.x,H.z,[0.5,0.95,1],22,130,14); } }catch(_){}
  try{ if(window._voxEmit)window._voxEmit(H.x,12,H.z,26,0x33e8ff,4,10,10); }catch(_){}
  try{ if(typeof Audio!=='undefined'&&Audio.blip){ Audio.blip(320,0.14,'sine',0.18,760); Audio.blip(640,0.1,'square',0.12,980); } }catch(_){}
  try{ if(typeof announce==='function')announce('BIKE REBUILT','#39ffa0'); }catch(_){}
}catch(_){} }
window._bikeBlowUp=_bikeBlowUp; window._bikeRegen=_bikeRegen;

// per-frame: park the bike under the rider, bank it with the lean, pitch it with the carve, run the FX
function _bikeTick(dt){
  try{ _bikeEjectBtn(); }catch(_){}
  if(!player){ return; }
  // ── DESTROYED — nothing to drive; the wreck rebuilds itself on a timer ──
  if(BIKE.dead){ BIKE.regenT=(BIKE.regenT||0)-dt; if(BIKE.regenT<=0)_bikeRegen(); return; }"""
assert s.count(a3)==1
s=s.replace(a3,b3)

open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
