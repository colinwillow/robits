import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()

a="""  // ── THE REAL BIKE ── models/hoverbike.glb (the _BIKE_GLB hook, now real): the procedural torpedo below still"""
b="""  // ── THE REAL BIKE ── models/hoverbike_02.glb (the _BIKE_GLB hook, now real): the procedural torpedo below still"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""    _gl.load((typeof window._BIKE_GLB==='string'?window._BIKE_GLB:'models/hoverbike.glb'), (gltf)=>{ try{"""
b2="""    _gl.load((typeof window._BIKE_GLB==='string'?window._BIKE_GLB:(window._BIKE_GLB_FILE||'models/hoverbike_02.glb')), (gltf)=>{ try{   // rev 02: cleaner rig (12 nodes), symmetric turn poses, hands renamed. Point _BIKE_GLB at the old file to A/B them."""
assert s.count(a2)==1
s=s.replace(a2,b2)

a3="""      // A STEERING POSE MAY ONLY ROTATE. Measured in models/hoverbike.glb: the 'right' clip translates handle_bars by"""
b3="""      // A STEERING POSE MAY ONLY ROTATE. Measured in the rev-01 export: the 'right' clip translates handle_bars by"""
assert s.count(a3)==1
s=s.replace(a3,b3)
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
