import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
a="""  if(trigger){ self._agroT=AGRO; self._prey=trigger; }
  if(self._agroT<=0){ self._prey=null; return {prey:null, engaged:false, near, nearD:nd}; }
  const pr=self._prey;
  if(!pr || pr.alive===false || Math.hypot((pr.wx||0)-self.wx,(pr.wz||0)-self.wz)>FORGET) self._prey=near;   // lost it: fall back to whoever is closest"""
b = """  // AN ACTIVE PROVOCATION WINS OUTRIGHT. This used to fall through to the forget check below, which then measured the
  // freshly-acquired target against FORGET and swapped it for whoever was nearest - so retaliating against a shooter
  // standing further away than the forget radius silently retargeted onto a bystander on the very same tick. If
  // something is provoking it right now, that thing IS the prey; the forget rule only decides when to give up.
  if(trigger){ self._agroT=AGRO; self._prey=trigger; }
  else {
    if(self._agroT<=0){ self._prey=null; return {prey:null, engaged:false, near, nearD:nd}; }
    const pr=self._prey;
    if(!pr || pr.alive===false || Math.hypot((pr.wx||0)-self.wx,(pr.wz||0)-self.wz)>FORGET) self._prey=near;   // lost it: fall back to whoever is closest
  }"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""  const FORGET=(o.forget!=null?o.forget:(window._WILD_FORGET_R||760));"""
b2 = """  const FORGET=Math.max((o.forget!=null?o.forget:(window._WILD_FORGET_R||760)),(window._WILD_RETALIATE_R||1400));   // never smaller than the range it can be provoked FROM, or it drops a shooter the instant it acquires one"""
assert s.count(a2)==1
s=s.replace(a2,b2)
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
