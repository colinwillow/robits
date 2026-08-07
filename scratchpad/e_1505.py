import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── THROTTLE: second-order, so it BUILDS instead of decaying ──
a="""    this._skSpeed=lerp(this._skSpeed, throttle*MAXV, clamp(accel*dt,0,1));            // throttle = cruise target (anti-grav glide, no pedal)"""
b = """    // ── WATER FEEL ── every axis becomes a second-order response instead of a first-order one.
    // lerp(speed, target, accel*dt) moves FASTEST on the very first frame and decays from there - which is precisely
    // backwards from "it starts off slow and then it builds fast". A damped spring builds: acceleration ramps in,
    // carries through the middle, and because it is deliberately UNDER-damped it overshoots and settles back when you
    // let go. The strafe (below) was worse than first-order - it was instantaneous, a hard step sideways. The vertical
    // jet gets the same ramp. So forward/back, side to side and up all share one weight.
    // _RIDE_SPRING=false restores the old response on every axis.
    const _sprung=(window._RIDE_SPRING!==false)&&this._bikeMode, _dtc=Math.min(dt,0.05);
    if(_sprung){
      const _K=(window._RIDE_ACC_K!=null?window._RIDE_ACC_K:14), _D=(window._RIDE_ACC_D!=null?window._RIDE_ACC_D:3.6);   // zeta ~0.48 -> ~19% overshoot
      this._skAcc=(this._skAcc||0)+(((throttle*MAXV)-(this._skSpeed||0))*_K-(this._skAcc||0)*_D)*_dtc;
      this._skSpeed=(this._skSpeed||0)+this._skAcc*_dtc;
    } else { this._skSpeed=lerp(this._skSpeed, throttle*MAXV, clamp(accel*dt,0,1)); this._skAcc=0; }   // throttle = cruise target (anti-grav glide, no pedal)"""
assert s.count(a)==1
s=s.replace(a,b)

# ── STRAFE: was an instantaneous step; give it the same weight ──
a2="""    const nth=this._skHeading, v=this._skSpeed, strafeV=-strafe*(window._HB_STRAFE||240);   // negated: right-stick right now strafes right"""
b2 = """    const _stTgt=-strafe*(window._HB_STRAFE||240);   // negated: right-stick right now strafes right
    if(_sprung){
      const _SK=(window._RIDE_STR_K!=null?window._RIDE_STR_K:16), _SD=(window._RIDE_STR_D!=null?window._RIDE_STR_D:4.2);
      this._stAcc=(this._stAcc||0)+((_stTgt-(this._strafeV||0))*_SK-(this._stAcc||0)*_SD)*_dtc;
      this._strafeV=(this._strafeV||0)+this._stAcc*_dtc;
    } else { this._strafeV=_stTgt; this._stAcc=0; }
    const nth=this._skHeading, v=this._skSpeed, strafeV=this._strafeV||0;"""
assert s.count(a2)==1
s=s.replace(a2,b2)

# ── TURN: more slide, less rail. A jet ski does not turn on grip, it turns and washes out. ──
a3="""      const grip=(window._BIKE_GRIP!=null?window._BIKE_GRIP:4.4)*(1-(window._BIKE_SLIP_K!=null?window._BIKE_SLIP_K:0.62)*sk);"""
b3 = """      // Lower grip = the velocity heading lags the nose further = a visible slip angle you carve through, which is
        // what reads as water rather than rails. It already scaled down with speed; both ends are looser now.
      const grip=(window._BIKE_GRIP!=null?window._BIKE_GRIP:3.1)*(1-(window._BIKE_SLIP_K!=null?window._BIKE_SLIP_K:0.72)*sk);"""
assert s.count(a3)==1
s=s.replace(a3,b3)

# ── VERTICAL JET: thrust ramps in and tails out, so the climb eases up to speed ──
a4="""      const jetIn=clamp(this._hbJetInput||0,0,1), descIn=clamp(this._hbDescInput||0,0,1);   // right-stick UP = jet boost up, DOWN = sink/brake"""
b4 = """      // The jet was full thrust on frame one and zero on release - a step input on the one axis you hold the longest.
      // Easing the THRUST (asymmetric: builds slower than it lets go) turns the climb into a ramp, and because the
      // velocity is the integral of that ramp you get the slow-then-fast build for free, with a coast at the top.
      const _jRaw=clamp(this._hbJetInput||0,0,1);
      if(window._RIDE_SPRING!==false&&this._bikeMode){
        const _jr=(_jRaw>(this._jetE||0))?(window._RIDE_JET_IN!=null?window._RIDE_JET_IN:4.2):(window._RIDE_JET_OUT!=null?window._RIDE_JET_OUT:9);
        this._jetE=(this._jetE||0)+(_jRaw-(this._jetE||0))*Math.min(1,_jr*dt);
      } else this._jetE=_jRaw;
      const jetIn=this._jetE, descIn=clamp(this._hbDescInput||0,0,1);   // right-stick UP = jet boost up, DOWN = sink/brake"""
assert s.count(a4)==1
s=s.replace(a4,b4)

assert s.count('BUILD &#8734;-CMB1504')==1 and s.count('∞-CMB1504')==1
s=s.replace('BUILD &#8734;-CMB1504','BUILD &#8734;-CMB1505').replace('∞-CMB1504','∞-CMB1505')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
