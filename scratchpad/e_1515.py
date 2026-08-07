import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

a="""    const _sprung=(window._RIDE_SPRING!==false)&&this._bikeMode, _dtc=Math.min(dt,0.05);
    if(_sprung){"""
b = """    const _sprung=(window._RIDE_SPRING!==false)&&this._bikeMode, _dtc=Math.min(dt,0.05);
    // REVERSE IS NOT A SECOND FORWARD GEAR. The throttle ran straight into the speed target, so pulling back reached
    // the same top speed as driving - the bike went backwards as fast as it went forwards. Negative throttle is
    // scaled down; _BIKE_REVERSE=1 restores the symmetric behaviour.
    const _thr=(throttle<0)?throttle*(window._BIKE_REVERSE!=null?window._BIKE_REVERSE:0.42):throttle;
    if(_sprung){"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""      this._skAcc=(this._skAcc||0)+(((throttle*MAXV)-(this._skSpeed||0))*_K-(this._skAcc||0)*_D)*_dtc;"""
b2 = """      this._skAcc=(this._skAcc||0)+(((_thr*MAXV)-(this._skSpeed||0))*_K-(this._skAcc||0)*_D)*_dtc;"""
assert s.count(a2)==1
s=s.replace(a2,b2)

a3="""    } else { this._skSpeed=lerp(this._skSpeed, throttle*MAXV, clamp(accel*dt,0,1)); this._skAcc=0; }   // throttle = cruise target (anti-grav glide, no pedal)"""
b3 = """    } else { this._skSpeed=lerp(this._skSpeed, _thr*MAXV, clamp(accel*dt,0,1)); this._skAcc=0; }   // throttle = cruise target (anti-grav glide, no pedal)"""
assert s.count(a3)==1
s=s.replace(a3,b3)

# dragon: half again
a4="""    const _k=(window._DRAGON_SPAN||12)/68;"""
b4 = """    const _k=(window._DRAGON_SPAN||6)/68;"""
assert s.count(a4)==1
s=s.replace(a4,b4)
a5="""      d.scale.multiplyScalar((window._DRAGON_SPAN||12)/((raw>1e-9?raw:1)*gs));"""
b5 = """      d.scale.multiplyScalar((window._DRAGON_SPAN||6)/((raw>1e-9?raw:1)*gs));"""
assert s.count(a5)==1
s=s.replace(a5,b5)

assert s.count('BUILD &#8734;-CMB1514')==1 and s.count('∞-CMB1514')==1
s=s.replace('BUILD &#8734;-CMB1514','BUILD &#8734;-CMB1515').replace('∞-CMB1514','∞-CMB1515')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
