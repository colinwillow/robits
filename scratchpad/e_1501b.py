import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
a="""        const _sink=_hHold?0:(window._BIKE_FLY_SINK!=null?window._BIKE_FLY_SINK:312);   // hover-hold = neutral buoyancy, it just hangs
        this._hbHopVy=(this._hbHopVy||0)-_sink*dt;
        this._hbHopVy*=Math.max(0,1-(window._BIKE_FLY_DRAG!=null?window._BIKE_FLY_DRAG:2.6)*dt);   // drag -> a terminal speed both ways (climb ~185/s, settle ~52/s), so neither the climb nor the fall runs away and letting go bites almost immediately"""
b="""        if(_hHold){
          // HOLD MEANS STOP, NOT COAST. Zeroing the sink alone left the climb to bleed off through flight drag - a 0.38s
          // time constant, so deflecting the stick to shoot still carried you ~27 units higher before it settled. Keep
          // your finger down and the bike PARKS at the height it is at, whatever you do with the stick after that.
          this._hbHopVy=(this._hbHopVy||0)*Math.max(0,1-(window._BIKE_HOLD_DAMP!=null?window._BIKE_HOLD_DAMP:14)*dt);
        } else {
          this._hbHopVy=(this._hbHopVy||0)-(window._BIKE_FLY_SINK!=null?window._BIKE_FLY_SINK:312)*dt;
          this._hbHopVy*=Math.max(0,1-(window._BIKE_FLY_DRAG!=null?window._BIKE_FLY_DRAG:2.6)*dt);   // drag -> a terminal speed both ways (climb ~185/s, settle ~120/s), so neither the climb nor the fall runs away and letting go bites almost immediately
        }"""
assert s.count(a)==1
open(p+'.tmp','w',encoding='utf-8').write(s.replace(a,b)); os.replace(p+'.tmp',p)
print('ok')
