import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── the reusable brain, in front of the manta ──
a="""const _mantaK=()"""
b="""// ════════════════════════════════════════════════════════════
//  WILD ANIMAL BRAIN — shared by every free-roaming creature (the manta today, the sky dragon next).
//  A wild animal is NEUTRAL. It is not a spawned attacker with a target; it is a thing that lives here and is off
//  doing its own business until something gives it a reason not to be. Two rules follow from that:
//    · IT DOES NOT KNOW WHO THE PLAYER IS. Prey is "nearest of the human and every AI bot", so it stops reading as a
//      scripted hunter pointed at you. Whoever strays too close is whoever it goes for.
//    · IT ONLY ENGAGES ON PROVOCATION. Someone enters its notice radius, or someone hurts it. Interest then decays,
//      and once nothing has provoked it for a while it goes back to wandering — it does not hold a grudge forever.
//  Shooting it from range aims it at the SHOOTER specifically: knock() records the direction the hit came from, and
//  the prey pick prefers whoever lies along it, so sniping the thing has consequences.
//  Returns {prey, engaged}. window._WILD=false makes every creature permanently hostile again (the old behaviour).
// ════════════════════════════════════════════════════════════
window._wildProvoke=function(self,dirX,dirZ,sec){ try{
  self._provokeT=Math.max(self._provokeT||0,(sec!=null?sec:(window._WILD_PROVOKE_SEC||1.2)));
  if(dirX!=null){ const l=Math.hypot(dirX,dirZ)||1; self._provokeDir={x:-dirX/l, z:-dirZ/l}; }   // knock() pushes AWAY from the attacker, so the attacker lies back down the reverse
}catch(_){} };
window._wildTick=function(self,dt,o){ o=o||{};
  const NOTICE=(o.notice!=null?o.notice:(window._WILD_NOTICE_R||300));
  const FORGET=(o.forget!=null?o.forget:(window._WILD_FORGET_R||760));
  const AGRO=(o.agro!=null?o.agro:(window._WILD_AGRO_SEC||11));
  self._agroT=Math.max(0,(self._agroT||0)-dt);
  if((self._provokeT||0)>0)self._provokeT=Math.max(0,self._provokeT-dt);
  // EVERY player counts, human or not
  const list=[];
  try{ if(typeof player!=='undefined'&&player&&player.alive&&!player._deathSeq)list.push(player); }catch(_){}
  try{ if(typeof GS_bots!=='undefined'&&GS_bots)for(const b of GS_bots){ if(b&&b.alive!==false)list.push(b); } }catch(_){}
  if(!list.length){ self._prey=null; return {prey:null, engaged:false, nearD:1e9}; }
  let near=null, nd=1e18;
  for(const t of list){ const d=Math.hypot((t.wx||0)-self.wx,(t.wz||0)-self.wz); if(d<nd){ nd=d; near=t; } }
  // ── PROVOCATION ──
  let trigger=null;
  if(nd<NOTICE)trigger=near;                                            // you strayed into its space
  if((self._provokeT||0)>0){                                            // ...or you hurt it, from wherever
    trigger=near;
    const D=self._provokeDir;
    if(D){ let bestA=null, bs=-2;                                       // prefer whoever lies along the hit's incoming line
      for(const t of list){ const ddx=(t.wx||0)-self.wx, ddz=(t.wz||0)-self.wz, l=Math.hypot(ddx,ddz)||1;
        const dot=(ddx/l)*D.x+(ddz/l)*D.z; if(dot>bs && l<(window._WILD_RETALIATE_R||1400)){ bs=dot; bestA=t; } }
      if(bestA&&bs>(window._WILD_RETALIATE_DOT||0.35))trigger=bestA; }
  }
  if(trigger){ self._agroT=AGRO; self._prey=trigger; }
  if(self._agroT<=0){ self._prey=null; return {prey:null, engaged:false, near, nearD:nd}; }
  const pr=self._prey;
  if(!pr || pr.alive===false || Math.hypot((pr.wx||0)-self.wx,(pr.wz||0)-self.wz)>FORGET) self._prey=near;   // lost it: fall back to whoever is closest
  return {prey:self._prey||near, engaged:true, near, nearD:nd};
};
const _mantaK=()"""
assert s.count(a)==1
s=s.replace(a,b,1)

# ── the manta uses it: pick its own prey, and wander when nothing has provoked it ──
a2="""  update(p,dt){ this.baseUpdate(); this.t+=dt; if(this.hitFlash>0)this.hitFlash--; else try{ this._rig.eyeMat.color.setHex(0x9d5cff); }catch(_){}
    const px=p.wx, pz=p.wz, dx=px-this.wx, dz=pz-this.wz, d=Math.hypot(dx,dz)||1;"""
b2="""  update(p,dt){ this.baseUpdate(); this.t+=dt; if(this.hitFlash>0)this.hitFlash--; else try{ this._rig.eyeMat.color.setHex(0x9d5cff); }catch(_){}
    // It picks its OWN prey (see _wildTick): the caller always hands it the human, which is exactly why it felt like
    // the match had been pointed at you. An ally manta keeps fighting for you and skips the neutral state entirely.
    const _W=(window._wildTick&&window._WILD!==false&&window._MANTA_WILD!==false&&!this._ally)?window._wildTick(this,dt,{
      notice:(window._MANTA_NOTICE_R||330), forget:(window._MANTA_FORGET_R||760), agro:(window._MANTA_AGRO_SEC||11)}):null;
    if(_W&&_W.prey)p=_W.prey;
    const _wander=!!(_W&&!_W.engaged&&!this._riderOn&&!this._hangOn);
    if(_W&&!_W.prey&&!_wander)p=(typeof player!=='undefined'?player:p);
    const px=p.wx, pz=p.wz, dx=px-this.wx, dz=pz-this.wz, d=Math.hypot(dx,dz)||1;"""
assert s.count(a2)==1
s=s.replace(a2,b2)

a3="""    if(this._riderOn&&this._state==='swoop')this._state='orbit';   // can't dive at prey that's standing on your back
    if(this._state==='swoop'){"""
b3="""    if(this._riderOn&&this._state==='swoop')this._state='orbit';   // can't dive at prey that's standing on your back
    if(_wander){
      // ── NEUTRAL ── nothing has provoked it, so it is simply somewhere else being a creature: a slow drift between
      // waypoints across the arena, at its own altitude, chasing nobody. No volleys, no eye laser, no dives. It is
      // still perfectly mountable while it does this — a wild animal you can catch a ride on, not a boss encounter.
      this._state='wander';
      if(!this._wpt || Math.hypot(this.wx-this._wpt.x,this.wz-this._wpt.z)<(window._WILD_WPT_R||110) || (this._wptT=(this._wptT||0)-dt)<=0){
        const _c=(typeof zoneCenter==='function'&&typeof GS!=='undefined')?zoneCenter(GS.zone):{x:0,z:0};
        const _RR=(window._WILD_ROAM_R||900), _wa=Math.random()*TAU, _wr=_RR*(0.3+Math.random()*0.7);
        this._wpt={x:_c.x+Math.cos(_wa)*_wr, z:_c.z+Math.sin(_wa)*_wr};
        this._wptT=(window._WILD_WPT_SEC||8)+Math.random()*6;
      }
      tx=this._wpt.x; tz=this._wpt.z; sp=this.spd*(window._WILD_CRUISE_K||0.62);   // an unhurried cruise reads as "busy elsewhere"
      wantY=(window._MANTA_WANDER_Y||124)+Math.sin(this.t*0.6)*16;                 // its OWN altitude — not yours
      this._swoopT=Math.max(this._swoopT||0,1.5);                                  // noticing you must not instantly become a dive
      this._laserT=Math.max(this._laserT==null?3:this._laserT,2.5);
    }
    else if(this._state==='swoop'){"""
assert s.count(a3)==1
s=s.replace(a3,b3)

# ── hurting it provokes it ──
a4="""  hit(dmg=1){ this.hitFlash=6; try{ this._rig.eyeMat.color.setHex(0xffffff); }catch(_){} return super.hit(dmg); }"""
b4="""  hit(dmg=1){ this.hitFlash=6; try{ this._rig.eyeMat.color.setHex(0xffffff); }catch(_){} try{ if(window._wildProvoke)window._wildProvoke(this); }catch(_){} return super.hit(dmg); }   // shoot it and it stops minding its own business"""
assert s.count(a4)==1
s=s.replace(a4,b4)

a5="""    const l=Math.hypot(dx,dz)||1, nx=dx/l, nz=dz/l;
    const sp=Math.max((window._MANTA_KB_MIN||320),(mag||6)*(window._MANTA_KB_SPEED||55));"""
b5="""    const l=Math.hypot(dx,dz)||1, nx=dx/l, nz=dz/l;
    try{ if(window._wildProvoke)window._wildProvoke(this,nx,nz,(window._WILD_PROVOKE_SEC||1.2)); }catch(_){}   // and it comes looking for whoever it came from
    const sp=Math.max((window._MANTA_KB_MIN||320),(mag||6)*(window._MANTA_KB_SPEED||55));"""
assert s.count(a5)==1
s=s.replace(a5,b5)

# ── it arrives in the WORLD, not on top of you ──
a6="""    const a=Math.random()*TAU, r=500+Math.random()*200;
    const e=new MantaRay(player.wx+Math.cos(a)*r, player.wz+Math.sin(a)*r, 1); e.y=140;   // glides in from high up"""
b6="""    // Placed against the ARENA, not against you. Spawning it in a ring around the player meant that even a perfectly
    // neutral creature appeared to have come for you — the entrance itself was the tell.
    const a=Math.random()*TAU, r=(window._MANTA_SPAWN_R||760)+Math.random()*260;
    const _c=(typeof zoneCenter==='function'&&typeof GS!=='undefined')?zoneCenter(GS.zone):{x:0,z:0};
    const e=new MantaRay(_c.x+Math.cos(a)*r, _c.z+Math.sin(a)*r, 1); e.y=140;   // glides in from high up"""
assert s.count(a6)==1
s=s.replace(a6,b6)

assert s.count('BUILD &#8734;-CMB1502')==1 and s.count('∞-CMB1502')==1
s=s.replace('BUILD &#8734;-CMB1502','BUILD &#8734;-CMB1503').replace('∞-CMB1502','∞-CMB1503')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
