import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── A. PHASE-LOCK the rider's roll to the bike's ──
a="""  g.rotation.z=BIKE._bankS;
  if(window._BIKE_AIM_LOCK!==false){ player.aim=Math.PI/2-g.rotation.y; player._visAim=player.aim; }   // the right stick must not swivel the CHARACTER — he faces where the bike points"""
b="""  g.rotation.z=BIKE._bankS;
  // ...and the RIDER's roll is written from the SAME value in the same breath. player.draw() runs EARLIER in the frame
  // than this tick, so anything it derives from _bankS is always one frame stale — which let the rider's roll exceed
  // the bike's for a frame around every zero crossing. Writing it here (the last writer of the frame) locks them.
  try{ if(player.model&&window._BIKE_RIDER_LOCK!==false)player.model.rotation.z=BIKE._bankS*(window._BIKE_RIDER_BANK!=null?window._BIKE_RIDER_BANK:0.55); }catch(_){}
  if(window._BIKE_AIM_LOCK!==false){ player.aim=Math.PI/2-g.rotation.y; player._visAim=player.aim; }   // the right stick must not swivel the CHARACTER — he faces where the bike points"""
assert s.count(a)==1
s=s.replace(a,b)

# ── B. JET EXHAUST: real particles, out the back under throttle / out the bottom on lift ──
a2="""  { const bj=BIKE.boostJet, jetK=player._bikeJetK||0, thr=Math.max(0,player._skThrottle||0);
    const k=Math.max(jetK, thr*0.35+sp*0.3);
    bj.material.opacity=k*0.75;
    bj.scale.set(1+jetK*0.6, 0.6+k*1.4+Math.random()*0.12, 1+jetK*0.6);
    bj.rotation.z=0; bj.rotation.x=(Math.PI/2)*(1-jetK*0.85)+ (player._skSteer||0)*0;   // horizontal (=flame back) -> swivels toward vertical (flame down) as up-boost rises
    bj.rotation.y=-(player._skSteer||0)*0.5;
  }"""
b2="""  { const bj=BIKE.boostJet, jetK=player._bikeJetK||0, thr=Math.max(0,player._skThrottle||0);
    // ── JET EXHAUST ── the boost FX used to be this one cone mesh, swivelled and scaled. A cone is a SHAPE, not
    // exhaust, which is exactly why it read as cheap. Each of the bike's jet cans now emits a real particle stream,
    // and the stream's DIRECTION is the thrust reaction: straight out the BACK under throttle, straight DOWN when
    // you're climbing, and the normalised blend of the two while you do both — so the same four jets sell both moves.
    // window._BIKE_JET_FX=false restores the cone.
    if(window._BIKE_JET_FX===false){
      const k=Math.max(jetK, thr*0.35+sp*0.3);
      bj.material.opacity=k*0.75;
      bj.scale.set(1+jetK*0.6, 0.6+k*1.4+Math.random()*0.12, 1+jetK*0.6);
      bj.rotation.z=0; bj.rotation.x=(Math.PI/2)*(1-jetK*0.85);
      bj.rotation.y=-(player._skSteer||0)*0.5;
    } else {
      bj.material.opacity=0;                                                    // the cone stands down
      const bw=thr*0.9+sp*0.45, dw=jetK*1.4, tot=bw+dw;                         // how much of the thrust is FORWARD vs UP
      BIKE._jetK=tot;
      if(tot>(window._BIKE_JET_MIN||0.05) && typeof ps!=='undefined' && ps._spawn){
        const kb=bw/tot, kd=dw/tot;
        const fx2=Math.sin(nth), fz2=Math.cos(nth);
        let ex=-fx2*kb, ey=-kd, ez=-fz2*kb; const el=Math.hypot(ex,ey,ez)||1; ex/=el; ey/=el; ez/=el;   // reaction = opposite the thrust
        const SP=(window._BIKE_JET_SPD||300)*(0.5+Math.min(1.4,tot)*0.8);
        const N=Math.max(1,Math.round((window._BIKE_JET_N||(IS_MOBILE?1:2))*Math.min(1.7,tot)));
        const _v=(BIKE._jv||(BIKE._jv=new THREE.Vector3()));
        const pts=BIKE._jpts||(BIKE._jpts=[]); pts.length=0;
        if(BIKE.flames&&BIKE.flames.length){ for(const fl of BIKE.flames){ if(!fl)continue; _v.copy(fl.position); g.localToWorld(_v); pts.push(_v.x,_v.y,_v.z); } }
        if(!pts.length){ _v.set(0,9.5,-18); g.localToWorld(_v); pts.push(_v.x,_v.y,_v.z); }
        const C=(window._BIKE_JET_COL||[0.34,1,0.72]), SPR=(window._BIKE_JET_SPREAD||0.24);
        const cvx=(player.vx||0)*(window._BIKE_JET_CARRY||0.22), cvz=(player.vz||0)*(window._BIKE_JET_CARRY||0.22);   // exhaust inherits some of the bike's own motion so it trails instead of hanging
        for(let q=0;q<pts.length;q+=3){ for(let k2=0;k2<N;k2++){
          const s2=SP*(0.55+Math.random()*0.8), hot=(Math.random()<(window._BIKE_JET_HOT||0.3));
          ps._spawn(pts[q]+rand(-1.3,1.3), pts[q+1]+rand(-1.3,1.3), pts[q+2]+rand(-1.3,1.3),
            (ex+rand(-SPR,SPR))*s2+cvx, (ey+rand(-SPR,SPR))*s2, (ez+rand(-SPR,SPR))*s2+cvz,
            hot?1:C[0], hot?1:C[1], hot?1:C[2], (window._BIKE_JET_DEC||0.05)+Math.random()*0.035);
        } }
      }
    }
  }"""
assert s.count(a2)==1
s=s.replace(a2,b2)

# ── C. FLYING MOTORCYCLE: replace the hover SPRING with real flight ──
a3="""      const _hHold=this._bikeMode&&this._bikeHoverHold;
      this._hbHopVy=(this._hbHopVy||0)+((_hHold?0:-(this._hbHopY||0)*_K)-(this._hbHopVy||0)*(_hHold?4.5:_D))*dt;   // hover-hold: no spring pull, heavy damping -> he hangs where he is until the stick is released
      this._hbHopY=(this._hbHopY||0)+this._hbHopVy*dt;
      const _ceil=(window._HB_JET_CEIL||700); if(this._hbHopY>_ceil){ this._hbHopY=_ceil; if(this._hbHopVy>0)this._hbHopVy=0; }"""
b3="""      const _hHold=this._bikeMode&&this._bikeHoverHold;
      // ── FLYING MOTORCYCLE ── the hover model pulled height back to the cushion with a SPRING (-hopY*K), so the higher
      // you climbed the harder it yanked you down: it could never be more than a hover, by construction. In flight mode
      // there is no spring at all — the jet is the only thing that lifts you, and letting go leaves a gentle constant
      // sink with drag, so you SETTLE back down instead of dropping. That is the whole difference between "a bike that
      // hovers" and "a bike you fly": altitude you gained is yours until you stop paying for it.
      // _BIKE_FLY=false restores the hover spring. _BIKE_FLY_SINK/_DRAG set how fast it comes down.
      const _fly=this._bikeMode&&window._BIKE_FLY!==false;
      if(_fly){
        const _sink=_hHold?0:(window._BIKE_FLY_SINK!=null?window._BIKE_FLY_SINK:135);   // hover-hold = neutral buoyancy, it just hangs
        this._hbHopVy=(this._hbHopVy||0)-_sink*dt;
        this._hbHopVy*=Math.max(0,1-(window._BIKE_FLY_DRAG!=null?window._BIKE_FLY_DRAG:1.8)*dt);   // drag -> a terminal speed both ways, so neither the climb nor the fall runs away
      } else {
        this._hbHopVy=(this._hbHopVy||0)+((_hHold?0:-(this._hbHopY||0)*_K)-(this._hbHopVy||0)*(_hHold?4.5:_D))*dt;   // hover-hold: no spring pull, heavy damping -> he hangs where he is until the stick is released
      }
      this._hbHopY=(this._hbHopY||0)+this._hbHopVy*dt;
      const _ceil=_fly?(window._BIKE_FLY_CEIL||2600):(window._HB_JET_CEIL||700); if(this._hbHopY>_ceil){ this._hbHopY=_ceil; if(this._hbHopVy>0)this._hbHopVy=0; }"""
assert s.count(a3)==1
s=s.replace(a3,b3)

open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
