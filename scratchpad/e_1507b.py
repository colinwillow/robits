import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()

# per-creature spawn distance: a dragon that bursts up off the deck should do it where you can SEE it
a="""      const a=Math.random()*TAU, r=(window._MANTA_SPAWN_R||760)+Math.random()*260;"""
b = """      const a=Math.random()*TAU, r=(W.r?W.r():(window._MANTA_SPAWN_R||760))+Math.random()*260;"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""  { key:'dragon', at:()=>(window._DRAGON_AMBIENT_T||80), label:'\\u26a0 MECH LIGHTNING DRAGON', col:'#66e0ff', hz:90,"""
b2 = """  { key:'dragon', at:()=>(window._DRAGON_AMBIENT_T||80), label:'\\u26a0 MECH LIGHTNING DRAGON', col:'#66e0ff', hz:90,
    r:()=>(window._DRAGON_SPAWN_R||430),   // nearer than the manta on purpose: its arrival is a burst up off the deck, and an entrance you cannot see is not an entrance"""
assert s.count(a2)==1
s=s.replace(a2,b2)

# ── ALTITUDE CEILING ── it was settling around 196, well above the top of the frame
a3="""  update(p,dt){
    super.update(p,dt);
    if(this._mx){ try{"""
b3 = """  update(p,dt){
    super.update(p,dt);
    // ── STAY IN FRAME ── the inherited cruise is prey-relative (_MANTA_CRUISE + believed prey height), which for this
    // creature settled around y=196 - more than twice the manta's ~88, i.e. above the top of a phone screen, so it
    // could arrive perfectly and still never be seen. A CEILING rather than a servo: dives and swoops still take it
    // lower, it just cannot drift up out of view. _DRAGON_MAX_Y raises it if you want a genuinely high-altitude beast.
    if(!this._riderOn&&!this._hangOn){ const _my=(window._DRAGON_MAX_Y||132);
      if(this.y>_my)this.y+=(_my-this.y)*Math.min(1,dt*(window._DRAGON_Y_EASE||1.6)); }
    if(this._mx){ try{"""
assert s.count(a3)==1
s=s.replace(a3,b3)

a4="""    this.y=(window._DRAGON_CRUISE||118);"""
b4 = """    this.y=(window._DRAGON_CRUISE||100);"""
assert s.count(a4)==1
s=s.replace(a4,b4)
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
