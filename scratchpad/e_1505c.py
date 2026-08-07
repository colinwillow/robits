import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()

a="""        // A running jet holds its own weight. Feeding the ramp against the full sink meant the first ~0.12s of thrust
        // was still net-downward - press UP, sink first, which is the opposite of the intended ease-in. The sink is
        // therefore suppressed while lift is commanded, and _BIKE_FLY_LIFT is rebalanced so the terminal climb is
        // unchanged: with no sink to fight, 484/2.6 = 186/s up, exactly what (795-312)/2.6 used to give.
        if(_hHold||jetIn>0.06){
          // HOLD MEANS STOP, NOT COAST. Zeroing the sink alone left the climb to bleed off through flight drag - a 0.38s
          // time constant, so deflecting the stick to shoot still carried you ~27 units higher before it settled. Keep
          // your finger down and the bike PARKS at the height it is at, whatever you do with the stick after that.
          this._hbHopVy=(this._hbHopVy||0)*Math.max(0,1-(window._BIKE_HOLD_DAMP!=null?window._BIKE_HOLD_DAMP:14)*dt);
        } else {
          this._hbHopVy=(this._hbHopVy||0)-(window._BIKE_FLY_SINK!=null?window._BIKE_FLY_SINK:312)*dt;
          this._hbHopVy*=Math.max(0,1-(window._BIKE_FLY_DRAG!=null?window._BIKE_FLY_DRAG:2.6)*dt);   // drag -> a terminal speed both ways (climb ~185/s, settle ~120/s), so neither the climb nor the fall runs away and letting go bites almost immediately
        }"""
b = """        // THREE cases, not two - conflating the last two is what made the ramp fight gravity.
        if(_hHold){
          // HOLD MEANS STOP, NOT COAST. Zeroing the sink alone left the climb to bleed off through flight drag - a 0.38s
          // time constant, so deflecting the stick to shoot still carried you ~27 units higher before it settled. Keep
          // your finger down and the bike PARKS at the height it is at, whatever you do with the stick after that.
          this._hbHopVy=(this._hbHopVy||0)*Math.max(0,1-(window._BIKE_HOLD_DAMP!=null?window._BIKE_HOLD_DAMP:14)*dt);
        } else if(jetIn>0.06){
          // THRUSTING: a running jet holds its own weight, so no sink - only drag. Feeding the thrust ramp against the
          // full sink meant the first ~0.12s of a press was still net-DOWNWARD: press up, sink first, the exact
          // opposite of the intended ease-in (measured vy going negative through the whole ramp). _BIKE_FLY_LIFT is
          // rebalanced to match: with no sink to fight, 484/2.6 = 186/s terminal climb - what (795-312)/2.6 gave.
          this._hbHopVy*=Math.max(0,1-(window._BIKE_FLY_DRAG!=null?window._BIKE_FLY_DRAG:2.6)*dt);
        } else {
          this._hbHopVy=(this._hbHopVy||0)-(window._BIKE_FLY_SINK!=null?window._BIKE_FLY_SINK:312)*dt;
          this._hbHopVy*=Math.max(0,1-(window._BIKE_FLY_DRAG!=null?window._BIKE_FLY_DRAG:2.6)*dt);   // drag -> a terminal speed both ways (climb ~186/s, settle ~120/s), so neither the climb nor the fall runs away and letting go bites almost immediately
        }"""
assert s.count(a)==1
open(p+'.tmp','w',encoding='utf-8').write(s.replace(a,b)); os.replace(p+'.tmp',p)
print('ok')
