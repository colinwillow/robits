import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── CONTROLS BACK TO GHOST ──
a="""  window._HB_CTRL=(window._BIKE_CTRL||'skate');                                 // SKATE: left stick drives it like your own legs do, right stick keeps lift/guns/wheelie. 'ghost' = the old Halo-Ghost scheme (L throttle+strafe, R turn)"""
b = """  window._HB_CTRL=(window._BIKE_CTRL||'ghost');                                 // GHOST (the default, and the one that feels right): L throttle+strafe, R turn, R deep-up fires. The front-steer CARVE underneath it is unchanged - that dynamic was never the problem, the mapping was. window._BIKE_CTRL='skate' brings back the left-stick-drives experiment."""
assert s.count(a)==1
s=s.replace(a,b)

# ── STRONGER TURN ──
a2="""      const _dmax=(window._BIKE_STEER_MAX!=null?window._BIKE_STEER_MAX:0.72);       // full lock, radians
      const _wb=(window._BIKE_WHEELBASE!=null?window._BIKE_WHEELBASE:140);          // sets the carve radius: R = wheelbase / tan(lock)
      const _piv=(window._BIKE_PIVOT!=null?window._BIKE_PIVOT:0.55);                // low-speed nose authority, faded out as you pick up speed"""
b2 = """      // Third pass on the geometry. In a front-steer model the RATE is v/R, so tightening R lifts the whole curve -
      // but the bottom end is governed by the speed-INDEPENDENT pivot term, so both move together or it only gets
      // sharper where it was already sharpest. R ~161 -> ~132, and standstill authority 0.55 -> 0.85.
      const _dmax=(window._BIKE_STEER_MAX!=null?window._BIKE_STEER_MAX:0.72);       // full lock, radians
      const _wb=(window._BIKE_WHEELBASE!=null?window._BIKE_WHEELBASE:115);          // sets the carve radius: R = wheelbase / tan(lock)
      const _piv=(window._BIKE_PIVOT!=null?window._BIKE_PIVOT:0.85);                // low-speed nose authority, faded out as you pick up speed"""
assert s.count(a2)==1
s=s.replace(a2,b2)

assert s.count('BUILD &#8734;-CMB1510')==1 and s.count('∞-CMB1510')==1
s=s.replace('BUILD &#8734;-CMB1510','BUILD &#8734;-CMB1511').replace('∞-CMB1510','∞-CMB1511')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
