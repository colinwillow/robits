import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── 1. THE RIDER PITCHES WITH THE BIKE ──
a="""    BIKE._pitchS=(BIKE._pitchS||0)+(_px-(BIKE._pitchS||0))*Math.min(1,dt*(window._BIKE_PITCH_EASE||4.5));   // progressive, like the bank
    g.rotation.x=BIKE._pitchS-_lp; }   // nose dips on throttle, lifts on the hop, LOOP pitches it around — and pulling back pops a WHEELIE"""
b = """    BIKE._pitchS=(BIKE._pitchS||0)+(_px-(BIKE._pitchS||0))*Math.min(1,dt*(window._BIKE_PITCH_EASE||4.5));   // progressive, like the bank
    g.rotation.x=BIKE._pitchS-_lp;   // nose dips on throttle, lifts on the hop, LOOP pitches it around - and pulling back pops a WHEELIE
    // ...and the RIDER pitches with it. CMB1497 coupled the roll and stopped there, so the bike could stand on its nose
    // while the rider stayed bolt upright - which is the "bike tilts one way, character the other" on a straight climb.
    // Same treatment: written here (the frame's last writer, after draw() has forced rotation.x back to 0) and scaled,
    // because a rider leans less than his machine on every axis.
    try{ if(player.model&&window._BIKE_RIDER_LOCK!==false)player.model.rotation.x=(BIKE._pitchS-_lp)*(window._BIKE_RIDER_PITCH!=null?window._BIKE_RIDER_PITCH:0.8); }catch(_){} }"""
assert s.count(a)==1
s=s.replace(a,b)

# the carve coefficient was tuned for hover velocities; flight saturates it at the clamp permanently
a2="""  const carve=THREE.MathUtils.clamp((player._hbHopVy||0)*0.0016,-0.3,0.3);"""
b2 = """  // 0.0016 was sized for hover-era vertical speeds. Flight terminal is ~186/s, which pins this at the +/-0.3 clamp for
  // the WHOLE climb and the whole fall - the nose is jammed at max deflection instead of reading the actual climb rate.
  const _cvK=(window._BIKE_CARVE_K!=null?window._BIKE_CARVE_K:((player._bikeMode&&window._BIKE_FLY!==false)?0.0009:0.0016));
  const carve=THREE.MathUtils.clamp((player._hbHopVy||0)*_cvK,-0.3,0.3);"""
assert s.count(a2)==1
s=s.replace(a2,b2)

# ── 2. THE BLAST PUNT WAS LEAVING THE FRAME ──
a3="""    player.knock(Math.cos(a),Math.sin(a),(window._BIKE_BOOM_KB||16),(window._BIKE_BOOM_LIFT||520),26,{blast:true}); } }catch(_){}"""
b3 = """    // 520 of lift threw him ~440 units up at ~500/s, which outruns the chase camera's own easing - he left the top of
    // the frame and came back a second later, which is what read as "he just disappears and then reappears".
    player.knock(Math.cos(a),Math.sin(a),(window._BIKE_BOOM_KB||16),(window._BIKE_BOOM_LIFT||285),26,{blast:true}); } }catch(_){}"""
assert s.count(a3)==1
s=s.replace(a3,b3)

# ── 3. A LAUNCH SHOULD TUMBLE, NOT LIE DOWN ──
a4="""      if(this.model.userData.isRobot){ // YAW first, THEN pitch about the body's own X axis -> the head ALWAYS leads the velocity, even after a wall bounce reverses the direction
        const _qy=this._kbQy||(this._kbQy=new THREE.Quaternion()), _qx=this._kbQx||(this._kbQx=new THREE.Quaternion());
        _qy.setFromAxisAngle(_KB_YAX, yaw); _qx.setFromAxisAngle(_KB_XAX, pitch); this.model.quaternion.copy(_qy).multiply(_qx);"""
b4 = """      // TUMBLE. The arc pose alone holds the body RIGID along the flight line, and a body held rigid and horizontal
      // reads as "lying down in mid-air", not as "thrown" - which is exactly what it looked like. Rolling it steadily
      // about its own flight axis is what sells the throw. Spins down as the launch decays so the landing still
      // resolves through the existing exit blend. window._KB_TUMBLE=false restores the rigid pose.
      const _tum=(window._KB_TUMBLE!==false);
      if(_tum && (this._launched||_flung)){ const _decay=Math.max(0.15,Math.min(1,Math.hypot(this._kbVx||0,this._kbVz||0)*0.5+Math.abs(this.pvy||0)/260));
        this._kbRoll=(this._kbRoll||0)+(window._KB_TUMBLE_SPIN!=null?window._KB_TUMBLE_SPIN:3.1)*0.016*_decay; }
      else this._kbRoll=0;
      if(this.model.userData.isRobot){ // YAW first, THEN pitch about the body's own X axis -> the head ALWAYS leads the velocity, even after a wall bounce reverses the direction
        const _qy=this._kbQy||(this._kbQy=new THREE.Quaternion()), _qx=this._kbQx||(this._kbQx=new THREE.Quaternion());
        _qy.setFromAxisAngle(_KB_YAX, yaw); _qx.setFromAxisAngle(_KB_XAX, pitch); this.model.quaternion.copy(_qy).multiply(_qx);
        if(_tum&&this._kbRoll){ const _qr=this._kbQr||(this._kbQr=new THREE.Quaternion()); _qr.setFromAxisAngle(_KB_ZAX, this._kbRoll); this.model.quaternion.multiply(_qr); }"""
assert s.count(a4)==1
s=s.replace(a4,b4)

# ── 4. A BIKE LEFT IN MID-AIR FLOATS DOWN ──
a5="""  if(BIKE.grp){ if(window._BIKE_REPARK!==false && player && !BIKE.dead){ _bikePark(player.wx+Math.sin(player._skHeading||0)*26, player.wz+Math.cos(player._skHeading||0)*26, player._skHeading||0, 0); }"""
b5 = """  // Park it at the height it was actually LEFT at, not on the floor. Stepping off at altitude used to teleport the bike
  // to ground level under you; it now keeps its height and settles down from there (see the parked branch in _bikeTick).
  if(BIKE.grp){ if(window._BIKE_REPARK!==false && player && !BIKE.dead){ _bikePark(player.wx+Math.sin(player._skHeading||0)*26, player.wz+Math.cos(player._skHeading||0)*26, player._skHeading||0, Math.max(0,(player.py||0)-(window._HB_HOVER_Y||16))); }"""
assert s.count(a5)==1
s=s.replace(a5,b5)

a6="""    const P=BIKE.park; BIKE.grp.position.set(P.x,(P.y||0)-14+Math.sin(performance.now()*0.0016)*1.6, P.z);"""
b6 = """    const P=BIKE.park;
    if((P.y||0)>0.5) P.y=Math.max(0,(P.y||0)-(window._BIKE_PARK_SINK||110)*dt);   // an abandoned bike sinks at its own flight rate rather than dropping - it is anti-grav, it does not fall
    BIKE.grp.position.set(P.x,(P.y||0)-14+Math.sin(performance.now()*0.0016)*1.6, P.z);"""
assert s.count(a6)==1
s=s.replace(a6,b6)

assert s.count('BUILD &#8734;-CMB1503')==1 and s.count('∞-CMB1503')==1
s=s.replace('BUILD &#8734;-CMB1503','BUILD &#8734;-CMB1504').replace('∞-CMB1503','∞-CMB1504')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
