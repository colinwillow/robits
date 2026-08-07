import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── 1. THE BIKE JOINS THE MOUNT KNOCK-OFF RULE ──
a="""    const _onManta=!!(this._mantaRide||this._mantaHang);
    if(this._mount||_onManta){   // MOUNT KNOCK-OFF RULE: only a hit that would actually LAUNCH you dismounts you. Explosions always do. A melee/body"""
b="""    const _onManta=!!(this._mantaRide||this._mantaHang);
    // The BIKE is a mount too, and it was the one thing taking hits without obeying the rule: shots and melees alike
    // just shoved the rider around while he stayed welded to the saddle. Same rule as the creatures now — an explosion
    // or a real melee launches you OFF it, a bullet only chips you.
    const _onBike=!!(this._bikeMode&&this._onHoverboard);
    if(this._mount||_onManta||_onBike){   // MOUNT KNOCK-OFF RULE: only a hit that would actually LAUNCH you dismounts you. Explosions always do. A melee/body"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""      if(typeof _dismount==='function')try{ _dismount(false); }catch(_){}"""
b2="""      if(typeof _dismount==='function')try{ _dismount(false); }catch(_){}
      // silent: the knock's own lift/mag below does the flinging, and _bikeDismount re-parks the bike where you fell
      // off it, so you can pick it back up instead of losing it.
      if(_onBike)try{ if(window._bikeDismount)window._bikeDismount(true); }catch(_){}"""
assert s.count(a2)==1
s=s.replace(a2,b2)

a3="""    if(window._SMASH_KB!==false && !this._mount && !_onManta){"""
b3="""    if(window._SMASH_KB!==false && !this._mount && !_onManta && !_onBike){"""
assert s.count(a3)==1
s=s.replace(a3,b3)

# ── 2. RIDING THE BIKE IS ITS OWN STATE: nothing else may claim you ──
a4="""  if(typeof player==='undefined'||!player||!player.alive||player._mount||player._ballActive||player._deathSeq)return false;"""
b4="""  if(typeof player==='undefined'||!player||!player.alive||player._mount||player._ballActive||player._deathSeq)return false;
  if(player._bikeMode&&player._onHoverboard&&window._BIKE_EXCLUSIVE!==false)return false;   // flying the bike past a manta must not hand you to the manta — you are already riding something"""
assert s.count(a4)==1
s=s.replace(a4,b4)

a5="""function _nearestGrab(opts){
  if(!player||player._carryPayload) return null;
  if(!player||player._carryPayload) return null;
  const cands=[];"""
b5="""function _nearestGrab(opts){
  if(!player||player._carryPayload) return null;
  // ── RIDING IS AN EXCLUSIVE STATE ── while you are on the bike no other interact may claim you (boarding a creature,
  // taking a weapon pad, entering the armory...). Getting swapped onto a manta mid-flight left you half-attached to two
  // vehicles at once. Stepping off is the EJECT button's job, not an interact. window._BIKE_EXCLUSIVE=false to revert.
  if(player._bikeMode&&player._onHoverboard&&window._BIKE_EXCLUSIVE!==false) return null;
  const cands=[];"""
assert s.count(a5)==1
s=s.replace(a5,b5)

assert s.count('BUILD &#8734;-CMB1500')==1 and s.count('∞-CMB1500')==1
s=s.replace('BUILD &#8734;-CMB1500','BUILD &#8734;-CMB1501').replace('∞-CMB1500','∞-CMB1501')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
