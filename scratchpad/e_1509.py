import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── 1. IT TURNS TOO SLOWLY ── tighten the carve radius
a="""      const _dmax=(window._BIKE_STEER_MAX!=null?window._BIKE_STEER_MAX:0.62);       // full lock, radians
      const _wb=(window._BIKE_WHEELBASE!=null?window._BIKE_WHEELBASE:210);          // sets the carve radius: R = wheelbase / tan(lock)
      const _piv=(window._BIKE_PIVOT!=null?window._BIKE_PIVOT:0.34);                // low-speed nose authority, faded out as you pick up speed"""
b = """      // Radius R = wheelbase / tan(lock). The first pass sat at R~296, which reads as a barge: fine at top speed but
      // sluggish everywhere below it, because in this model rate falls with speed. Radius roughly halved (R~161) and
      // the standstill authority raised, so it comes round hard at speed AND still answers when you are crawling.
      const _dmax=(window._BIKE_STEER_MAX!=null?window._BIKE_STEER_MAX:0.72);       // full lock, radians
      const _wb=(window._BIKE_WHEELBASE!=null?window._BIKE_WHEELBASE:140);          // sets the carve radius: R = wheelbase / tan(lock)
      const _piv=(window._BIKE_PIVOT!=null?window._BIKE_PIVOT:0.55);                // low-speed nose authority, faded out as you pick up speed"""
assert s.count(a)==1
s=s.replace(a,b)

# ── 2. SKATE: the LEFT stick is the vehicle ──
a2="""    else if(_ctrl==='ghost'){ steerIn=rx; throttle=-ly; strafe=lx;"""
b2 = """    else if(_ctrl==='skate'){
      // ── LEFT STICK IS THE VEHICLE ── the character's own locomotion scheme applied to something that cannot pivot.
      // You push a world direction (camera-relative, exactly like on foot) and the bike goes there - but it has to
      // CARVE its way round to it through the front-steer model rather than snapping, which is the whole difference
      // between steering a body and steering a board. Heading error becomes steering lock; the bicycle model does the
      // rest, so a hard reversal swings the tail through instead of spinning on the spot. Stick MAGNITUDE is throttle,
      // so easing the stick out is easing off. Right stick is untouched from the ghost scheme below (centre-hold =
      // lift, up = guns, down = wheelie). window._BIKE_CTRL='ghost' puts the old scheme back.
      const _mv=(typeof rotInput==='function')?rotInput(lx,ly):{x:lx,z:ly};
      const _mag=Math.min(1,Math.hypot(_mv.x||0,_mv.z||0));
      if(_mag>(window._SKATE_DEAD||0.16)){
        const _want=Math.atan2(_mv.x,_mv.z);                                   // same convention as _skHeading
        let _e=_want-this._skHeading; _e=Math.atan2(Math.sin(_e),Math.cos(_e));
        steerIn=-clamp(_e*(window._SKATE_STEER_K||2.2),-1,1);                  // heading error -> lock. negative: heading DECREASES with positive steer
        throttle=_mag;
      } else { steerIn=0; throttle=0; }
      strafe=0;
      const _rTouch=!!(window._jR&&window._jR.id!==null), _rMag=Math.hypot(rx,ry);
      const _center=_rTouch&&_rMag<(window._BIKE_LIFT_DEAD!=null?window._BIKE_LIFT_DEAD:0.42);
      if(_center)this._bikeHoverLatch=true; if(!_rTouch)this._bikeHoverLatch=false;
      this._hbJetInput=_center?1:0;
      this._bikeHoverHold=(this._bikeHoverLatch&&_rTouch&&!_center)?1:0;
      this._hbDescInput=0;
      this._bikeFireIn=Math.max(0,-ry);
      this._bikeWheelie=Math.max(0,ry);
    }
    else if(_ctrl==='ghost'){ steerIn=rx; throttle=-ly; strafe=lx;"""
assert s.count(a2)==1
s=s.replace(a2,b2)

a3="""  window._HB_CTRL=(window._BIKE_CTRL||'ghost');                                 // Halo-Ghost scheme on the bike: L throttle+strafe, R turn, R deep-up fires"""
b3 = """  window._HB_CTRL=(window._BIKE_CTRL||'skate');                                 // SKATE: left stick drives it like your own legs do, right stick keeps lift/guns/wheelie. 'ghost' = the old Halo-Ghost scheme (L throttle+strafe, R turn)"""
assert s.count(a3)==1
s=s.replace(a3,b3)

assert s.count('BUILD &#8734;-CMB1508')==1 and s.count('∞-CMB1508')==1
s=s.replace('BUILD &#8734;-CMB1508','BUILD &#8734;-CMB1509').replace('∞-CMB1508','∞-CMB1509')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
