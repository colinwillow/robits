import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

a="""  update(p,dt){ this.baseUpdate(); this.t+=dt; if(this.hitFlash>0)this.hitFlash--; else try{ this._rig.eyeMat.color.setHex(0x9d5cff); }catch(_){}
    const px=p.wx, pz=p.wz, dx=px-this.wx, dz=pz-this.wz, d=Math.hypot(dx,dz)||1;
    const py=(p.py||0);
    this._volleyT-=dt; this._swoopT-=dt; this._stingCd=Math.max(0,this._stingCd-dt);
    let wantY=this._riderOn?((this._rideRefY!=null?this._rideRefY:Math.max(30,this.y))+Math.sin(this.t*1.1)*8)
                           :((window._MANTA_CRUISE||88)+py+Math.sin(this.t*1.1)*8);   // ridden: HOLD the mount altitude (player-relative cruise is a feedback loop when the player is standing on you)"""
b="""  update(p,dt){ this.baseUpdate(); this.t+=dt; if(this.hitFlash>0)this.hitFlash--; else try{ this._rig.eyeMat.color.setHex(0x9d5cff); }catch(_){}
    const px=p.wx, pz=p.wz, dx=px-this.wx, dz=pz-this.wz, d=Math.hypot(dx,dz)||1;
    const py=(p.py||0);
    // ── PERCEPTION LAG ── the creature must not read your transform. Feeding p.wx/p.py straight into the steering target
    // is what made it feel bolted to your feet: jump and it rose with you on the SAME FRAME, landed with you on the same
    // frame — it knew what you were doing at the instant you did it. So it flies at where it BELIEVES you are instead:
    //   1. a short DEAD TIME (_MANTA_REACT) — it is still acting on what it saw a beat ago, so a jump gets no response
    //      at all until it has "noticed";
    //   2. then a first-order follow (_MANTA_LAG / _MANTA_LAG_Y) toward that stale reading.
    // The attenuation falls out for free and is the whole point: a fast hop barely moves the belief before you have
    // already come back down, while standing on a ledge for a few seconds still brings it all the way up. Altitude lags
    // hardest (_MANTA_LAG_Y) because that mirroring was the worst tell. Contact/damage tests below keep using the TRUE
    // position — only where it CHOOSES TO FLY is lagged. _MANTA_LAG=0 restores instant tracking.
    let bx=px, bz=pz, by=py;
    if(window._MANTA_LAG!==0){ try{
      const _H=(this._pHist||(this._pHist=[])), _tn=(this._pT=(this._pT||0)+dt);
      _H.push(_tn,px,py,pz); if(_H.length>480)_H.splice(0,4);
      const _rt=(window._MANTA_REACT!=null?window._MANTA_REACT:0.3);
      while(_H.length>8 && _tn-_H[0]>_rt) _H.splice(0,4);                       // drop everything older than the reaction window; _H[0..3] is now the oldest reading it has "seen"
      const _sx=_H[1], _sy=_H[2], _sz=_H[3];
      if(this._bx==null){ this._bx=px; this._bz=pz; this._by=py; }
      const _f=(t)=>1-Math.exp(-dt/Math.max(0.001,t));                          // frame-rate independent: the same lag at 30fps and 120fps
      const _LX=(window._MANTA_LAG!=null?window._MANTA_LAG:0.5), _LY=(window._MANTA_LAG_Y!=null?window._MANTA_LAG_Y:1.6);
      const _kx=_f(_LX), _ky=_f(_LY);
      this._bx+=(_sx-this._bx)*_kx; this._bz+=(_sz-this._bz)*_kx; this._by+=(_sy-this._by)*_ky;
      bx=this._bx; bz=this._bz; by=this._by;
    }catch(_){ bx=px; bz=pz; by=py; } }
    this._volleyT-=dt; this._swoopT-=dt; this._stingCd=Math.max(0,this._stingCd-dt);
    let wantY=this._riderOn?((this._rideRefY!=null?this._rideRefY:Math.max(30,this.y))+Math.sin(this.t*1.1)*8)
                           :((window._MANTA_CRUISE||88)+by+Math.sin(this.t*1.1)*8);   // ridden: HOLD the mount altitude (player-relative cruise is a feedback loop when the player is standing on you)"""
assert s.count(a)==1
s=s.replace(a,b)

# orbit ring centres on the BELIEF, not on you
a2="""      const oa=Math.atan2(this.wz-pz,this.wx-px)+this._orbitDir*dt*(this.spd/R);
      tx=px+Math.cos(oa)*R; tz=pz+Math.sin(oa)*R;
      }"""
b2="""      const oa=Math.atan2(this.wz-bz,this.wx-bx)+this._orbitDir*dt*(this.spd/R);
      tx=bx+Math.cos(oa)*R; tz=bz+Math.sin(oa)*R;   // the ring hangs off where it THINKS you are -> it drifts in after you move instead of translating with you
      }"""
assert s.count(a2)==1
s=s.replace(a2,b2)

# the swoop's climb-out reference should trail too (it was pinned to your live height mid-dive)
a3="""      tx=this._sx; tz=this._sz; sp=this.spd*(window._MANTA_SWOOP_K||2.1); if(!this._riderOn)wantY=py+16;"""
b3="""      tx=this._sx; tz=this._sz; sp=this.spd*(window._MANTA_SWOOP_K||2.1); if(!this._riderOn)wantY=by+16;   // by, not py: a dive that re-aimed at your live altitude every frame tracked a jump perfectly through the pass"""
assert s.count(a3)==1
s=s.replace(a3,b3)

assert s.count('BUILD &#8734;-CMB1494')==1 and s.count('∞-CMB1494')==1
s=s.replace('BUILD &#8734;-CMB1494','BUILD &#8734;-CMB1495').replace('∞-CMB1494','∞-CMB1495')

open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
