import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()

# While the jets are RUNNING they hold station; the ramp then shapes how fast you CLIMB. Without this the ramp spends
# its first 0.12s losing to the sink, so pressing UP sent the bike DOWN first - measured vy going negative.
a="""        if(_hHold){"""
b = """        // A running jet holds its own weight. Feeding the ramp against the full sink meant the first ~0.12s of thrust
        // was still net-downward - press UP, sink first, which is the opposite of the intended ease-in. The sink is
        // therefore suppressed while lift is commanded, and _BIKE_FLY_LIFT is rebalanced so the terminal climb is
        // unchanged: with no sink to fight, 484/2.6 = 186/s up, exactly what (795-312)/2.6 used to give.
        if(_hHold||jetIn>0.06){"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""(_flyLift?(window._BIKE_FLY_LIFT!=null?window._BIKE_FLY_LIFT:795):"""
b2 = """(_flyLift?(window._BIKE_FLY_LIFT!=null?window._BIKE_FLY_LIFT:484):"""
assert s.count(a2)==1
s=s.replace(a2,b2)
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
