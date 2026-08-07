import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
a="""      window._DROPSEQ={ phase:'fall', t:0, vy:0, az:az, dist:dist, h:hh, hx:tx, hz:tz, yaw0:_y0,"""
b = """      // The portal's mandala must go dark the instant the drop begins. Gating it inside _stagePortalTick is not enough:
      // the ZONE UPDATE IS PAUSED for the whole fall (only the ship's own visuals are ticked), so that tick never runs
      // again and whatever `visible` it last wrote just persists - which is how a screen-wide additive lattice ends up
      // painted over the arena you are dropping into. Switched off from the drop side, where code is actually running.
      try{ const _P=window._stagePortal; if(_P&&_P.mem&&_P.mem.viz&&_P.mem.viz.mesh)_P.mem.viz.mesh.visible=false; }catch(_){}
      window._DROPSEQ={ phase:'fall', t:0, vy:0, az:az, dist:dist, h:hh, hx:tx, hz:tz, yaw0:_y0,"""
assert s.count(a)==1
open(p+'.tmp','w',encoding='utf-8').write(s.replace(a,b)); os.replace(p+'.tmp',p)
print('ok')
