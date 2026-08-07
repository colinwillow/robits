import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── 1. STEERING CLIPS ARE ROTATION-ONLY ──
a1="""      try{ if(gltf.animations&&gltf.animations.length){ const _mx=new THREE.AnimationMixer(bk); BIKE._glbMixer=_mx; BIKE._glbTurn={};
        for(const nm of ['left','right']){ const cl=gltf.animations.find(a2=>a2.name===nm); if(!cl)continue;
          const ac=_mx.clipAction(cl); ac.setLoop(THREE.LoopRepeat,Infinity); ac.clampWhenFinished=false; ac.play(); ac.paused=true; ac.time=0; ac.setEffectiveWeight(0); BIKE._glbTurn[nm]=ac; }
        _mx.update(0); } }catch(_){}"""
b1="""      // A STEERING POSE MAY ONLY ROTATE. Measured in models/hoverbike.glb: the 'right' clip translates handle_bars by
      // [0,0,0] and rotates it -14.8deg; 'left' rotates the exact mirror (+14.8) but ALSO carries a position track of
      // [12.8,-21.1,-2.1]. That is why a left turn slides the bars across the bike instead of turning them, and it is
      // baked into the export rather than introduced by the blend. So every steering clip's position/scale tracks get
      // PINNED to the neutral pose's values and only quaternion tracks are left free — asymmetric authoring can no
      // longer leak into the pose. _BIKE_TURN_ROT_ONLY=false plays the clips exactly as they were exported.
      try{ if(gltf.animations&&gltf.animations.length){ const _mx=new THREE.AnimationMixer(bk); BIKE._glbMixer=_mx; BIKE._glbTurn={}; BIKE._turnPinned=0;
        const _base=gltf.animations.find(a2=>!/^(left|right)$/i.test(a2.name||''));   // the exporter's neutral/rest take
        const _pin={}; if(_base)for(const tr of _base.tracks)_pin[tr.name]=tr.values;
        for(const nm of ['left','right']){ const cl0=gltf.animations.find(a2=>a2.name===nm); if(!cl0)continue;
          let cl=cl0;
          if(window._BIKE_TURN_ROT_ONLY!==false){ try{ cl=cl0.clone();
            for(const tr of cl.tracks){ if(/\\.quaternion$/.test(tr.name))continue;
              const src=_pin[tr.name]; if(!src||!src.length)continue;
              let _ch=0; for(let i=0;i<tr.values.length;i++){ const v=src[i%src.length]; if(tr.values[i]!==v){ tr.values[i]=v; _ch++; } }
              if(_ch)BIKE._turnPinned+=_ch; } }catch(_){ cl=cl0; } }
          const ac=_mx.clipAction(cl); ac.setLoop(THREE.LoopRepeat,Infinity); ac.clampWhenFinished=false; ac.play(); ac.paused=true; ac.time=0; ac.setEffectiveWeight(0); BIKE._glbTurn[nm]=ac; }
        _mx.update(0); } }catch(_){}"""
assert s.count(a1)==1
s=s.replace(a1,b1)

# ── 2. THE RIDER MUST LEAN LESS THAN THE BIKE, AND IN PHASE WITH IT ──
a2="""      const _bk=((this._skLean||0)+(this._hbSway||0))*(window._BIKE_BANK||1.5), _sh=(window._BIKE_SEAT_H!=null?window._BIKE_SEAT_H:24), _h2=this._skHeading||0;"""
b2="""      // Read the bike's OWN smoothed bank (BIKE._bankS) rather than recomputing it from raw lean. The seat is a physical
      // part of the bike, so where it swings to is the bike's business; deriving it separately let the two drift apart.
      const _B0=window.BIKE, _bk=(_B0&&_B0._bankS!=null)?_B0._bankS:(((this._skLean||0)+(this._hbSway||0))*(window._BIKE_BANK!=null?window._BIKE_BANK:1.0)), _sh=(window._BIKE_SEAT_H!=null?window._BIKE_SEAT_H:24), _h2=this._skHeading||0;"""
assert s.count(a2)==1
s=s.replace(a2,b2)

a3="""      this.model.rotation.z=this._onHoverboard?(((this._skLean||0)+(this._hbSway||0))*(this._bikeMode?(window._BIKE_BANK||1.5):1)):((GS.zone===-10)?(this._pipeLean||0):0);   // on the bike the rider rolls WITH the bike's full bank"""
b3="""      // ── RIDER ROLL ── he was rolling HARDER than the machine he is sitting on, and ahead of it. Two causes, both here:
      // this line defaulted _BIKE_BANK to 1.5 while the bike itself (in _bikeTick) defaults it to 1.0, so the rider
      // banked 50% further than the bike on every turn; and it read the RAW per-frame lean while the bike eases toward
      // its bank over _BIKE_BANK_EASE, so the rider also swung out FIRST and the two never lined up. Now he is driven
      // off the bike's own settled bank and scaled to a fraction of it — a rider leans less than his bike, never more.
      const _B1=window.BIKE, _bBank=(_B1&&_B1._bankS!=null)?_B1._bankS:(((this._skLean||0)+(this._hbSway||0))*(window._BIKE_BANK!=null?window._BIKE_BANK:1.0));
      this.model.rotation.z=this._onHoverboard?(this._bikeMode?(_bBank*(window._BIKE_RIDER_BANK!=null?window._BIKE_RIDER_BANK:0.55)):((this._skLean||0)+(this._hbSway||0))):((GS.zone===-10)?(this._pipeLean||0):0);"""
assert s.count(a3)==1
s=s.replace(a3,b3)

assert s.count('BUILD &#8734;-CMB1496')==1 and s.count('∞-CMB1496')==1
s=s.replace('BUILD &#8734;-CMB1496','BUILD &#8734;-CMB1497').replace('∞-CMB1496','∞-CMB1497')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
