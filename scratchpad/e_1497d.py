import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()

# fly mode gets its OWN, much gentler lift — the hover value was tuned to fight a spring that no longer exists
a="""      if(jetIn>0.06 && (this.boostFuel>0||this._bikeMode)){ this._hbHopVy=(this._hbHopVy||0)+(this._bikeMode?(window._BIKE_JET_FORCE!=null?window._BIKE_JET_FORCE:1250):(window._HB_JET_FORCE||760))*jetIn*dt;"""
b="""      // The hover lift (1250) was sized to overpower a spring pulling you back down. With the spring gone it just
      // launches you, and the momentum you bank on the way up coasts you hundreds of units past the moment you let go.
      // Flight uses its own, much gentler figure so the climb is a CLIMB you steer, not a cannon shot.
      const _flyLift=this._bikeMode&&window._BIKE_FLY!==false;
      if(jetIn>0.06 && (this.boostFuel>0||this._bikeMode)){ this._hbHopVy=(this._hbHopVy||0)+(this._bikeMode?(_flyLift?(window._BIKE_FLY_LIFT!=null?window._BIKE_FLY_LIFT:620):(window._BIKE_JET_FORCE!=null?window._BIKE_JET_FORCE:1250)):(window._HB_JET_FORCE||760))*jetIn*dt;"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""        this._hbHopVy*=Math.max(0,1-(window._BIKE_FLY_DRAG!=null?window._BIKE_FLY_DRAG:1.8)*dt);   // drag -> a terminal speed both ways, so neither the climb nor the fall runs away"""
b2="""        this._hbHopVy*=Math.max(0,1-(window._BIKE_FLY_DRAG!=null?window._BIKE_FLY_DRAG:2.6)*dt);   // drag -> a terminal speed both ways (climb ~185/s, settle ~52/s), so neither the climb nor the fall runs away and letting go bites almost immediately"""
assert s.count(a2)==1
s=s.replace(a2,b2)
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
