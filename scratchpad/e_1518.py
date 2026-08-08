import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

a="""    J=window._stageJack={ grp, mach, heart, tubes, H, HU, mx, mz, my, gy, fx, fz, rvx, rvz, col:_col, padX:player.wx, padZ:player.wz, attached:true, _detStamp:0 };"""
b = """    J=window._stageJack={ grp, mach, heart, tubes, H, HU, mx, mz, my, gy, fx, fz, rvx, rvz, col:_col, padX:player.wx, padZ:player.wz, attached:true, _detStamp:0 };
    // ── HAND OVER, DO NOT LEAVE A HOLE ── the forge's unit is retired HERE, the exact statement its replacement comes
    // into being, so the machine is on screen continuously across the deploy. It used to be cleared on a fixed 120ms
    // timer after the press while this one is not built until zone -32 is up - hundreds of milliseconds later - so the
    // machine popped out of existence and a new one popped back in. (The 120ms timer was itself a fix for the opposite
    // bug: both machines visible at once at different scales. A timer cannot solve that; only sequencing can, because
    // the thing it has to be sequenced against is a zone build of unknown duration.)
    try{ if(window._dressJack&&window._dressJackClear)window._dressJackClear(); }catch(_){}"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""  if(window._DEPLOY_JACK_CLEAR!==false){
    setTimeout(()=>{ try{ if(window._dressJack&&window._dressJackClear)window._dressJackClear(); }catch(_){} },
               (window._DEPLOY_JACK_CLEAR_MS!=null?window._DEPLOY_JACK_CLEAR_MS:120));
  }"""
b2 = """  // NOW A BACKSTOP ONLY. The handover happens where the stage unit is BUILT (see _stageJack), so the forge unit lives
  // right up until its replacement exists - no gap, and no two-machines-at-once either. This timer only covers a route
  // that never reaches the deploy room at all, so it is long rather than immediate.
  if(window._DEPLOY_JACK_CLEAR!==false){
    setTimeout(()=>{ try{ if(window._dressJack&&window._dressJackClear)window._dressJackClear(); }catch(_){} },
               (window._DEPLOY_JACK_CLEAR_MS!=null?window._DEPLOY_JACK_CLEAR_MS:4200));
  }"""
assert s.count(a2)==1
s=s.replace(a2,b2)

assert s.count('BUILD &#8734;-CMB1517')==1 and s.count('∞-CMB1517')==1
s=s.replace('BUILD &#8734;-CMB1517','BUILD &#8734;-CMB1518').replace('∞-CMB1517','∞-CMB1518')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
