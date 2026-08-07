import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()

# ── SMOKE: the bike tells you it is failing, before it fails ──
a="""  if(window._BIKE_CHASE!==false && !window._menuPaused){ try{ CAM.tyaw=nth+Math.PI; }catch(_){} }   // chase cam: stay square behind the bike so steering reads"""
b="""  // ── DAMAGE SMOKE ── a health bar you read without looking at a health bar. Starts as a thin grey wisp around half
  // health and thickens as it fails; below the fire threshold it starts throwing embers too, so the last stretch
  // before it goes up is unmistakable. Emitted from the tail, drifting back and up with the bike's own motion.
  if(window._BIKE_HP!==false && BIKE.maxHp){
    BIKE._hitFlash=Math.max(0,(BIKE._hitFlash||0)-dt);
    if(BIKE.glow)BIKE.glow.material.opacity=Math.min(1,(BIKE.glow.material.opacity||0.1)+(BIKE._hitFlash>0?0.55:0));
    const hpF=Math.max(0,Math.min(1,BIKE.hp/BIKE.maxHp)), hurt=1-hpF;
    if(hpF<(window._BIKE_SMOKE_AT||0.55) && typeof ps!=='undefined' && ps._spawn){
      const rate=(window._BIKE_SMOKE_RATE||26)*(hurt-(1-(window._BIKE_SMOKE_AT||0.55)));
      BIKE._smokeT=(BIKE._smokeT||0)+dt*Math.max(0,rate);
      while(BIKE._smokeT>=1){ BIKE._smokeT-=1;
        const _v=(BIKE._smV||(BIKE._smV=new THREE.Vector3())).set(rand(-4,4),8,-16); g.localToWorld(_v);
        const k=0.35+Math.random()*0.35;
        ps._spawn(_v.x,_v.y,_v.z, (player.vx||0)*0.25+rand(-14,14), rand(26,54), (player.vz||0)*0.25+rand(-14,14),
          k,k,k*1.05, (window._BIKE_SMOKE_DEC||0.012)+Math.random()*0.008); }   // slow decay = it lingers as a trail
      if(hpF<(window._BIKE_FIRE_AT||0.25) && window._voxEmitFire && Math.random()<(window._BIKE_FIRE_RATE||0.5)){
        const _v2=(BIKE._smV2||(BIKE._smV2=new THREE.Vector3())).set(rand(-4,4),9,-14); g.localToWorld(_v2);
        try{ window._voxEmitFire(_v2.x,_v2.y,_v2.z,(window._BIKE_FIRE_SIZE||3.4), rand(-18,18), rand(30,70), rand(-18,18), 0.7); }catch(_){}
      }
    }
  }
  if(window._BIKE_CHASE!==false && !window._menuPaused){ try{ CAM.tyaw=nth+Math.PI; }catch(_){} }   // chase cam: stay square behind the bike so steering reads"""
assert s.count(a)==1
s=s.replace(a,b)

# ── the hit goes into the VEHICLE ──
a2="""  spawnDmgNum(player.wx, player.py+25, player.wz, dmg, col);
  ps.ring(player.wx,player.wz,[0,1,1],40,120);ps.burst(player.wx,player.wz,[1,1,1],30,120);"""
b2="""  // ── THE VEHICLE EATS THE HIT ── you are riding a machine; the machine is what gets shot. Damage goes into the
  // bike's own health instead of yours, exactly like ball mode shields you, and the bike smokes and eventually
  // detonates under fire (which is what throws you off). Explosives and melee still launch you directly through the
  // mount knock-off rule, so this is not a way to be invulnerable — it is a second health bar that visibly fails.
  // window._BIKE_HP=false routes damage back to the rider.
  if(player._bikeMode && player._onHoverboard && window._BIKE_HP!==false && typeof window._bikeDamage==='function'){
    if(window._bikeDamage(dmg,col)){
      try{ spawnDmgNum(player.wx, player.py+34, player.wz, dmg, (window._BIKE_DMG_COL||'#ffb03c')); }catch(_){}
      if(typeof addTrauma==='function')try{ addTrauma(0.05); }catch(_){}
      return;
    }
  }
  spawnDmgNum(player.wx, player.py+25, player.wz, dmg, col);
  ps.ring(player.wx,player.wz,[0,1,1],40,120);ps.burst(player.wx,player.wz,[1,1,1],30,120);"""
assert s.count(a2)==1
s=s.replace(a2,b2)

# ── the wreck's home leaves with the arena ──
a3="""  try{ if(window._ARENA_BIKE!==false && typeof BIKE!=='undefined' && !BIKE.riding && !BIKE._hop){ BIKE.park=null; window._nearBike=null; if(BIKE.grp)BIKE.grp.visible=false; } }catch(_){}"""
b3="""  try{ if(window._ARENA_BIKE!==false && typeof BIKE!=='undefined' && !BIKE.riding && !BIKE._hop){ BIKE.park=null; BIKE._home=null; BIKE.dead=false; BIKE.regenT=0; BIKE.hp=BIKE.maxHp||(window._BIKE_MAX_HP||45); window._nearBike=null; if(BIKE.grp)BIKE.grp.visible=false; } }catch(_){}"""
assert s.count(a3)==1
s=s.replace(a3,b3)

assert s.count('BUILD &#8734;-CMB1501')==1 and s.count('∞-CMB1501')==1
s=s.replace('BUILD &#8734;-CMB1501','BUILD &#8734;-CMB1502').replace('∞-CMB1501','∞-CMB1502')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
