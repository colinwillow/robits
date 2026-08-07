import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

a="""    this._skHeading -= this._skSteer*turn*dt*(0.55+0.45*clamp(Math.abs(this._skSpeed)/MAXV,0,1));   // pivots even slow, sharper with speed"""
b = """    // ── FRONT-STEER (single-track / "bicycle") MODEL ──
    // The old line rotated the whole vehicle in place at a rate the stick set directly: that is a TANK, and it is why
    // it could never carve - there is no front and no back, only yaw. A front-steered vehicle (jet ski, snowboard,
    // skateboard) turns because the FRONT is angled and the body is dragged around it:
    //        yawRate = (speed / wheelbase) * tan(steerAngle)
    // Everything you asked for falls out of that one line. Turn RADIUS is set by how far you push the stick and is
    // independent of speed, while turn RATE scales with speed - so you carve an arc instead of pivoting, the tail
    // follows the nose through it, and rocking the stick left-right swings the back end like a pendulum. Reversing
    // steers the opposite way for free, because speed goes negative. A little pivot authority is kept at low speed so
    // you can still creep the nose around at a standstill (a real jet ski cannot; that is annoying in a game).
    // _RIDE_FRONT_STEER=false restores the tank model.
    if(this._bikeMode && window._RIDE_FRONT_STEER!==false){
      const _dmax=(window._BIKE_STEER_MAX!=null?window._BIKE_STEER_MAX:0.62);       // full lock, radians
      const _wb=(window._BIKE_WHEELBASE!=null?window._BIKE_WHEELBASE:210);          // sets the carve radius: R = wheelbase / tan(lock)
      const _piv=(window._BIKE_PIVOT!=null?window._BIKE_PIVOT:0.34);                // low-speed nose authority, faded out as you pick up speed
      const _sf=Math.min(1,Math.abs(this._skSpeed)/MAXV);
      this._yawRate=(this._skSpeed/_wb)*Math.tan(this._skSteer*_dmax) + this._skSteer*_piv*(1-_sf);
      this._skHeading-=this._yawRate*dt;
    } else {
      this._yawRate=this._skSteer*turn*(0.55+0.45*clamp(Math.abs(this._skSpeed)/MAXV,0,1));
      this._skHeading-=this._yawRate*dt;   // pivots even slow, sharper with speed
    }"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""    const targetLean=clamp(this._skSteer*0.6 + strafe*_strafeLean + (this._slipA||0)*(window._BIKE_SLIP_LEAN!=null?window._BIKE_SLIP_LEAN:1.1), -0.85, 0.85);   // sliding banks the bike harder into the drift"""
b2 = """    // Bank off the yaw rate it is ACTUALLY turning at, not off raw stick. Full lock while barely moving is not a turn,
    // so it should not look like one; the same lock at speed is a hard carve and now banks like one. That coupling is
    // most of what sells the pendulum when you rock the stick across.
    const _yrN=clamp((this._yawRate||0)/(window._BIKE_YAW_REF||1.9),-1,1);
    const targetLean=clamp(_yrN*(window._BIKE_LEAN_K!=null?window._BIKE_LEAN_K:0.62) + strafe*_strafeLean + (this._slipA||0)*(window._BIKE_SLIP_LEAN!=null?window._BIKE_SLIP_LEAN:1.1), -0.85, 0.85);   // sliding banks the bike harder into the drift"""
assert s.count(a2)==1
s=s.replace(a2,b2)

assert s.count('BUILD &#8734;-CMB1507')==1 and s.count('∞-CMB1507')==1
s=s.replace('BUILD &#8734;-CMB1507','BUILD &#8734;-CMB1508').replace('∞-CMB1507','∞-CMB1508')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
