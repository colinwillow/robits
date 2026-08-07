import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── TURN: strong at a standstill, CALM at speed ──
a="""      // Third pass on the geometry. In a front-steer model the RATE is v/R, so tightening R lifts the whole curve -
      // but the bottom end is governed by the speed-INDEPENDENT pivot term, so both move together or it only gets
      // sharper where it was already sharpest. R ~161 -> ~132, and standstill authority 0.55 -> 0.85.
      const _dmax=(window._BIKE_STEER_MAX!=null?window._BIKE_STEER_MAX:0.72);       // full lock, radians
      const _wb=(window._BIKE_WHEELBASE!=null?window._BIKE_WHEELBASE:115);          // sets the carve radius: R = wheelbase / tan(lock)
      const _piv=(window._BIKE_PIVOT!=null?window._BIKE_PIVOT:0.85);                // low-speed nose authority, faded out as you pick up speed"""
b = """      // THE TWO ENDS ARE SEPARATE KNOBS, and I had been moving the wrong one. Rate = v/R + pivot*(1-speed):
      //   · the pivot term is what turns you at a STANDSTILL and fades out as you gain speed
      //   · the v/R term is what turns you AT SPEED and does nothing when parked
      // Asking for "more turn" and getting it at 287 deg/s flat out is what made it spin out: I kept tightening R,
      // which only ever helps where it was already sharpest. The pivot stays where it is (that end is right now);
      // R opens back up so speed calms it down instead of amplifying it.
      const _dmax=(window._BIKE_STEER_MAX!=null?window._BIKE_STEER_MAX:0.72);       // full lock, radians
      const _wb=(window._BIKE_WHEELBASE!=null?window._BIKE_WHEELBASE:235);          // sets the carve radius: R = wheelbase / tan(lock)
      const _piv=(window._BIKE_PIVOT!=null?window._BIKE_PIVOT:0.85);                // low-speed nose authority, faded out as you pick up speed"""
assert s.count(a)==1
s=s.replace(a,b)

# ── THE TWO STICKS ADDING TOGETHER ── strafe must not fight the carve at speed
a2="""    const _stTgt=-strafe*(window._HB_STRAFE||240);   // negated: right-stick right now strafes right"""
b2 = """    // Strafe and steer both push you sideways, so at speed the left stick and the right stick were adding into one
    // muddled lateral shove - "the two sticks kind of add together and it's a little hard to control". Strafe now
    // fades out as you gain speed: full authority for parking and lining up, mostly gone once you are travelling,
    // where the carve should be doing the work. _BIKE_STRAFE_FADE=0 restores the old always-on strafe.
    const _stF=1-(window._BIKE_STRAFE_FADE!=null?window._BIKE_STRAFE_FADE:0.78)*Math.min(1,Math.abs(this._skSpeed||0)/MAXV);
    const _stTgt=-strafe*(window._HB_STRAFE||240)*_stF;   // negated: right-stick right now strafes right"""
assert s.count(a2)==1
s=s.replace(a2,b2)

# ── SPINNING OUT ── I had loosened grip for "water feel"; at 287 deg/s that became uncontrollable
a3="""      const grip=(window._BIKE_GRIP!=null?window._BIKE_GRIP:3.1)*(1-(window._BIKE_SLIP_K!=null?window._BIKE_SLIP_K:0.72)*sk);"""
b3 = """      // Grip was loosened to 3.1/0.72 for the water feel, which was fine at the old turn rates and became a
      // genuine spin-out once the yaw rate nearly tripled. Pulled back part-way: it still washes out and carves,
      // it just catches itself again.
      const grip=(window._BIKE_GRIP!=null?window._BIKE_GRIP:4.0)*(1-(window._BIKE_SLIP_K!=null?window._BIKE_SLIP_K:0.55)*sk);"""
assert s.count(a3)==1
s=s.replace(a3,b3)

# ── DRAGON: still massive. Cut hard. ──
a4="""    const _k=(window._DRAGON_SPAN||68)/68;"""
b4 = """    const _k=(window._DRAGON_SPAN||24)/68;"""
assert s.count(a4)==1
s=s.replace(a4,b4)

a5="""      d.scale.multiplyScalar((window._DRAGON_SPAN||68)/((raw>1e-9?raw:1)*gs));"""
b5 = """      // Told twice that it is still enormous, so this is a decisive cut rather than another cautious halving:
      // 150 -> 68 -> 24, about a sixth of what first shipped. Small is a cheap mistake to correct; large is not.
      d.scale.multiplyScalar((window._DRAGON_SPAN||24)/((raw>1e-9?raw:1)*gs));"""
assert s.count(a5)==1
s=s.replace(a5,b5)

a6="""    if(!this._riderOn&&!this._hangOn){ const _my=(window._DRAGON_MAX_Y||95);"""
b6 = """    if(!this._riderOn&&!this._hangOn){ const _my=(window._DRAGON_MAX_Y||78);"""
assert s.count(a6)==1
s=s.replace(a6,b6)

a7="""    this.y=(window._DRAGON_CRUISE||88);   // the manta cruises at ~84 measured; match it rather than tower over the match"""
b7 = """    this.y=(window._DRAGON_CRUISE||74);   // under the manta's ~84 rather than over it"""
assert s.count(a7)==1
s=s.replace(a7,b7)

assert s.count('BUILD &#8734;-CMB1511')==1 and s.count('∞-CMB1511')==1
s=s.replace('BUILD &#8734;-CMB1511','BUILD &#8734;-CMB1512').replace('∞-CMB1511','∞-CMB1512')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
