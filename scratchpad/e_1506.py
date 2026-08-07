import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

a="""window.MantaRay=MantaRay;"""
b = """window.MantaRay=MantaRay;
// ════════════════════════════════════════════════════════════
//  MECH LIGHTNING DRAGON — the manta's BRAIN with a different body.
//  Everything that makes the manta work already lives in MantaRay and _wildTick: the neutral wander, the provoke
//  rules, prey selection across the human and every bot, orbiting, the dive and its sting, eye bolts, the charge-up
//  laser, knockback, the ride/hang offsets. None of that is manta-SPECIFIC, so none of it is rebuilt here.
//  The trick is where the model goes: _rig.group is the object every one of those systems rotates, so the GLB is
//  parented INSIDE that group and the procedural manta meshes are simply hidden. The dragon then inherits the whole
//  flight rig for free - bank, tanh-saturated roll/spin, dive pitch, mount offsets - and this class only has to
//  handle what is genuinely new: fitting the model, its animation clips, and its own materials.
//  Clips shipped: idle_fly_1 / idle_fly_2 (hovering), fly_fast (travelling), entrance (bursts up from below).
// ════════════════════════════════════════════════════════════
class MechDragon extends MantaRay{
  constructor(wx,wz,wave,opts){
    super(wx,wz,wave);
    opts=opts||{};
    this._isDragon=true; this.glow=[0.45,0.8,1];
    this.hp=(window._DRAGON_HP!=null?window._DRAGON_HP:44); this.score=900;
    const _k=(window._DRAGON_SPAN||150)/110;
    this.size=52*_k; this._hitR=(window._DRAGON_HITR||78*_k); this._tall=150*_k; this._barY=64*_k;
    this.spd=(window._DRAGON_SPD||135);
    this.y=(window._DRAGON_CRUISE||118);
    this._dragonEntrance=!!opts.entrance;
    // the procedural manta body stands down; the GROUP it lives in stays, because that group IS the flight rig
    try{ this._rig.group.children.forEach(o=>{ o.visible=false; }); }catch(_){}
    this._loadDragon();
  }
  _loadDragon(){ try{
    const _gl=new GLTFLoader();
    _gl.load((typeof window._DRAGON_GLB==='string'?window._DRAGON_GLB:'models/mech_lightning_dragon.glb'), (gltf)=>{ try{
      const d=gltf.scene; d.updateMatrixWorld(true);
      // FIT. The export arrives sub-unit (its bind mesh spans ~0.1), so nothing is assumed about authored scale:
      // measure the longest axis and solve for the world span we want, accounting for the rig group's own scale.
      let bb=new THREE.Box3().setFromObject(d); let sz=bb.getSize(new THREE.Vector3());
      const raw=Math.max(sz.x,sz.y,sz.z)||1e-3;
      const gs=(this._rig.group.scale&&this._rig.group.scale.x)||1;
      d.scale.multiplyScalar((window._DRAGON_SPAN||150)/(raw*gs));
      d.updateMatrixWorld(true); bb.setFromObject(d); sz=bb.getSize(new THREE.Vector3());
      d.position.y-=(bb.min.y+bb.max.y)*0.5;                                    // centre it on the rig origin so the ride/hang offsets still line up
      d.rotation.y=(window._DRAGON_YAW!=null?window._DRAGON_YAW:-Math.PI/2);    // the rig flies along +Z; this export's long axis is +X
      // MATERIALS — honour an authored emissive map (this export ships one) instead of promoting the diffuse over it,
      // which is the exact mistake the bike loader used to make and which throws away which parts are meant to glow.
      d.traverse(o=>{ if(!o.material)return; (Array.isArray(o.material)?o.material:[o.material]).forEach(m=>{ if(!m)return;
        if(m.emissiveMap){ m.emissive=new THREE.Color(0xffffff); if(!(m.emissiveIntensity>1))m.emissiveIntensity=(window._DRAGON_EGLOW||2.0); }
        else if(m.map){ m.emissiveMap=m.map; m.emissive=new THREE.Color(0xffffff); m.emissiveIntensity=(window._DRAGON_GLOW||2.2); }
        if('toneMapped' in m)m.toneMapped=false; m.needsUpdate=true; }); });
      try{ if(window._DRAGON_WIRE!==false&&typeof _quadWireTwin==='function'){ const wc=new THREE.Color(window._DRAGON_WIRE_COL!=null?window._DRAGON_WIRE_COL:0x66e0ff);
        d.traverse(o=>{ if(o.isMesh&&o.geometry&&!o._isWireTwin){ try{ const w=_quadWireTwin(o,wc,(window._DRAGON_WIRE_OP!=null?window._DRAGON_WIRE_OP:0.45)); w._isWireTwin=true; (o.parent||d).add(w); }catch(_){} } }); } }catch(_){}
      d.traverse(o=>{ o.frustumCulled=false; });
      this._rig.group.add(d); this._dragon=d; this._dragonSpan=Math.max(sz.x,sz.y,sz.z);
      // the head doubles as the laser/bolt origin the manta code already looks for
      try{ let hd=null; d.traverse(o=>{ if(!hd&&/head/i.test(o.name||''))hd=o; }); if(hd)this._rig.eyes=[hd,hd]; }catch(_){}
      try{ let rd=null; d.traverse(o=>{ if(!rd&&/^ride$/i.test(o.name||''))rd=o; }); this._rideNode=rd; }catch(_){}   // the export ships a 'ride' bone - the saddle, for when mounting comes
      // CLIPS
      try{ if(gltf.animations&&gltf.animations.length){
        const mx=new THREE.AnimationMixer(d); this._mx=mx; this._clips={};
        const pick=(re)=>gltf.animations.find(a=>re.test(a.name||''));
        const reg=(key,cl)=>{ if(!cl)return; const ac=mx.clipAction(cl); ac.setLoop(THREE.LoopRepeat,Infinity); ac.setEffectiveWeight(0); ac.play(); this._clips[key]=ac; };
        reg('idle', pick(/idle_fly_1/i)||pick(/idle/i));
        reg('idle2',pick(/idle_fly_2/i));
        reg('fly',  pick(/fly_fast/i)||pick(/fly/i));
        const ent=pick(/entrance/i);
        if(ent){ const ea=mx.clipAction(ent); ea.setLoop(THREE.LoopOnce,1); ea.clampWhenFinished=true; this._clips.entrance=ea; }
        const first=this._clips.idle||this._clips.fly; if(first)first.setEffectiveWeight(1);
        this._clipCur=this._clips.idle?'idle':'fly';
        if(this._dragonEntrance&&this._clips.entrance){ const ea=this._clips.entrance;
          Object.values(this._clips).forEach(a=>{ if(a!==ea)a.setEffectiveWeight(0); });
          ea.reset().setEffectiveWeight(1).play(); this._entT=(ent.duration||1.33); this._clipCur='entrance'; }
      } }catch(_){}
    }catch(e){ console.warn('dragon fit',e); } }, undefined, (e)=>{ console.warn('dragon load',e); });
  }catch(_){} }
  hit(dmg=1){ try{ if(this._dragon)this._dragonFlash=(window._DRAGON_FLASH||0.16); }catch(_){} return super.hit(dmg); }
  update(p,dt){
    super.update(p,dt);
    if(this._mx){ try{
      this._mx.update(dt);
      // travelling vs hovering: the same speed the flight rig is already using, so the clip matches what you SEE
      const sp=Math.hypot(this.vx||0,this.vz||0);
      let want=(sp>(window._DRAGON_FLY_SPD||70))?'fly':'idle';
      if((this._entT||0)>0){ this._entT-=dt; want='entrance'; }
      if(want!==this._clipCur){
        const nx=this._clips[want], cu=this._clips[this._clipCur];
        if(nx){ const bl=(window._DRAGON_BLEND||0.35);
          nx.reset().setEffectiveWeight(1).play(); if(cu&&cu!==nx)nx.crossFadeFrom(cu,bl,false);
          Object.keys(this._clips).forEach(k=>{ if(k!==want&&k!==this._clipCur)try{ this._clips[k].setEffectiveWeight(0); }catch(_){} });
          this._clipCur=want; }
      }
    }catch(_){} }
    if((this._dragonFlash||0)>0 && this._dragon){ this._dragonFlash-=dt;
      try{ const on=this._dragonFlash>0; this._dragon.traverse(o=>{ if(!o.material||o._isWireTwin)return;
        (Array.isArray(o.material)?o.material:[o.material]).forEach(m=>{ if(m&&m.emissive)m.emissiveIntensity=on?(window._DRAGON_FLASH_GLOW||6):(window._DRAGON_EGLOW||2.0); }); }); }catch(_){}
    }
  }
}
window.MechDragon=MechDragon;
// debug/one-tap: drop a dragon in front of you. window._dragonTest(true) plays the burst-from-below entrance.
window._dragonTest=function(entrance){ try{
  if(typeof GS==='undefined'||typeof player==='undefined'||!player)return null;
  const a=(player.aim||0), r=(window._DRAGON_TEST_R||320);
  const e=new MechDragon(player.wx+Math.cos(a)*r, player.wz+Math.sin(a)*r, 1, {entrance:!!entrance});
  if(e.addToScene)e.addToScene(); (GS.enemies||(GS.enemies=[])).push(e);
  if(typeof announce==='function')announce('MECH LIGHTNING DRAGON','#66e0ff');
  return e;
}catch(e){ console.warn('dragonTest',e); return null; } };"""
assert s.count(a)==1
s=s.replace(a,b)

# make it spawnable from the test range's enemy pads, like every other creature
a2="""const _VR_ENEMIES=[['DIAMOND','Diamond'],['BOUNCER','Bouncer'],['PINWHEEL','Pinwheel'],['SEEKER','Seeker'],['DRIFTER','Drifter'],['SPIDER','Crawler'],['SHIELDER','Shielder'],['TURRET','Turret'],['GHOST','Ghost'],['BOMBER','HoverBomber'],['TANK','Tank'],['DRONE','BomberDrone'],['DRAGON','BlueDragon'],['CERBERUS','ThreeHeadedDog'],['DROIDEKA','DroidekaBot'],['MANTA','MantaRay']];"""
b2 = """const _VR_ENEMIES=[['DIAMOND','Diamond'],['BOUNCER','Bouncer'],['PINWHEEL','Pinwheel'],['SEEKER','Seeker'],['DRIFTER','Drifter'],['SPIDER','Crawler'],['SHIELDER','Shielder'],['TURRET','Turret'],['GHOST','Ghost'],['BOMBER','HoverBomber'],['TANK','Tank'],['DRONE','BomberDrone'],['DRAGON','BlueDragon'],['CERBERUS','ThreeHeadedDog'],['DROIDEKA','DroidekaBot'],['MANTA','MantaRay'],['MECHDRAGON','MechDragon']];"""
assert s.count(a2)==1
s=s.replace(a2,b2)

a3="""        const REG={Diamond,Bouncer,Pinwheel,Seeker,Drifter,Crawler,Shielder,Turret,Ghost,HoverBomber,Tank,BomberDrone,BlueDragon,ThreeHeadedDog,DroidekaBot,MantaRay};"""
b3 = """        const REG={Diamond,Bouncer,Pinwheel,Seeker,Drifter,Crawler,Shielder,Turret,Ghost,HoverBomber,Tank,BomberDrone,BlueDragon,ThreeHeadedDog,DroidekaBot,MantaRay,MechDragon};"""
assert s.count(a3)==1
s=s.replace(a3,b3)

assert s.count('BUILD &#8734;-CMB1505')==1 and s.count('∞-CMB1505')==1
s=s.replace('BUILD &#8734;-CMB1505','BUILD &#8734;-CMB1506').replace('∞-CMB1505','∞-CMB1506')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
