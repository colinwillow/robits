import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

a="""    const _k=(window._DRAGON_SPAN||150)/110;
    this.size=52*_k; this._hitR=(window._DRAGON_HITR||78*_k); this._tall=150*_k; this._barY=64*_k;
    this.spd=(window._DRAGON_SPD||135);
    this.y=(window._DRAGON_CRUISE||100);"""
b = """    // SIZE. Set by eye against the manta, not by measurement: every indirect way of measuring a SKINNED mesh
    // disagreed with the others (the same code reported the player robot as ~1850 units, and the bone cloud as
    // 11446), so the harness could not tell me what is actually on screen. _DRAGON_SPAN is a straight linear scale
    // on the model - if it still reads wrong, it is one number.
    // The HITBOX is deliberately NOT derived from the visual span alone: it is anchored to the manta's own figures so
    // the thing stays fair to shoot at whatever the art ends up scaled to, and only tracks span proportionally.
    const _k=(window._DRAGON_SPAN||68)/68;
    this.size=57*_k; this._hitR=(window._DRAGON_HITR||84*_k); this._tall=170*_k; this._barY=70*_k;
    this.spd=(window._DRAGON_SPD||135);
    this.y=(window._DRAGON_CRUISE||88);   // the manta cruises at ~84 measured; match it rather than tower over the match"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""      d.scale.multiplyScalar((window._DRAGON_SPAN||150)/((raw>1e-9?raw:1)*gs));"""
b2 = """      d.scale.multiplyScalar((window._DRAGON_SPAN||68)/((raw>1e-9?raw:1)*gs));"""
assert s.count(a2)==1
s=s.replace(a2,b2)

a3="""    if(!this._riderOn&&!this._hangOn){ const _my=(window._DRAGON_MAX_Y||132);"""
b3 = """    if(!this._riderOn&&!this._hangOn){ const _my=(window._DRAGON_MAX_Y||95);"""
assert s.count(a3)==1
s=s.replace(a3,b3)

# it is the LIGHTNING DRAGON
a4="""label:'\\u26a0 MECH LIGHTNING DRAGON', col:'#66e0ff', hz:90,"""
b4 = """label:'\\u26a0 LIGHTNING DRAGON', col:'#66e0ff', hz:90,"""
assert s.count(a4)==1
s=s.replace(a4,b4)

a5="""  if(typeof announce==='function')announce('MECH LIGHTNING DRAGON','#66e0ff');"""
b5 = """  if(typeof announce==='function')announce('LIGHTNING DRAGON','#66e0ff');"""
assert s.count(a5)==1
s=s.replace(a5,b5)

a6="""//  MECH LIGHTNING DRAGON — the manta's BRAIN with a different body."""
b6 = """//  LIGHTNING DRAGON — the manta's BRAIN with a different body."""
assert s.count(a6)==1
s=s.replace(a6,b6)

assert s.count('BUILD &#8734;-CMB1509')==1 and s.count('∞-CMB1509')==1
s=s.replace('BUILD &#8734;-CMB1509','BUILD &#8734;-CMB1510').replace('∞-CMB1509','∞-CMB1510')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
