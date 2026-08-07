import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

a="""          const vmesh=new THREE.LineSegments(vgeo,vmat); vmesh.frustumCulled=false; vmesh.renderOrder=2;"""
b = """          // BORN HIDDEN. This lattice is authored at ROOM scale (outer radius ~2580 units, bbox +/-4721) and is only
          // brought down to lens size by the per-frame fit in _stagePortalTick. Until that fit has run even once it is
          // a ~4700-unit white grid, and because it is frustumCulled=false + renderOrder 2 + additive it paints over
          // the entire screen from anywhere in the world - which is exactly what you see laid over the ground while
          // you drop in. Nothing may draw it before it has been sized; the tick turns it on.
          const vmesh=new THREE.LineSegments(vgeo,vmat); vmesh.frustumCulled=false; vmesh.renderOrder=2; vmesh.visible=false;"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""      const bs=baseS*V.bK;
      V.grp.scale.set(bs,bs,bs*Math.max(0.2,V.dK));"""
b2 = """      const bs=baseS*V.bK;
      V.grp.scale.set(bs,bs,bs*Math.max(0.2,V.dK));
      // safe to draw now: it has been fitted to the lens this frame. And never during the drop - you have left the
      // stage, and a screen-wide additive lattice over the arena you are falling into is not a portal effect.
      if(V.mesh)V.mesh.visible=(bs>0 && !window._DROPSEQ && window._STAGE_PORTAL_VIZ!==false);"""
assert s.count(a2)==1
s=s.replace(a2,b2)

assert s.count('BUILD &#8734;-CMB1512')==1 and s.count('∞-CMB1512')==1
s=s.replace('BUILD &#8734;-CMB1512','BUILD &#8734;-CMB1513').replace('∞-CMB1512','∞-CMB1513')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
