import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── extract the stage's mast into a SHARED builder so both instances are the same object by construction ──
a="""    try{ if(window._STAGE_JACK_POST!==false && gy>6){
      const _pc=(typeof _cc!=='undefined'&&_cc&&_cc.clone)?_cc.clone():new THREE.Color(0x9d7bff);
      const _lp=grp.worldToLocal(new THREE.Vector3(mx,0,mz));
      const _pm=new THREE.MeshStandardMaterial({color:0x131a2c,metalness:0.8,roughness:0.35,emissive:_pc.clone().multiplyScalar(0.22),toneMapped:false});
      const _gm=new THREE.MeshBasicMaterial({color:_pc,transparent:true,opacity:0.75,blending:THREE.AdditiveBlending,depthWrite:false,toneMapped:false});
      const _rP=HU*0.16;
      { const base=new THREE.Mesh(new THREE.CylinderGeometry(_rP*2.6,_rP*3.1,HU*0.10,16),_pm); base.position.set(_lp.x,_lp.y+HU*0.05,_lp.z); grp.add(base); }
      { const ring=new THREE.Mesh(new THREE.TorusGeometry(_rP*2.9,_rP*0.16,8,24),_gm); ring.rotation.x=Math.PI/2; ring.position.set(_lp.x,_lp.y+HU*0.11,_lp.z); grp.add(ring); }
      { const col3=new THREE.Mesh(new THREE.CylinderGeometry(_rP,_rP*1.25,gy+HU*0.12,14),_pm); col3.position.set(_lp.x,_lp.y+(gy+HU*0.12)*0.5,_lp.z); grp.add(col3); }
      for(let r2=0;r2<4;r2++){ const rb=new THREE.Mesh(new THREE.TorusGeometry(_rP*1.14,_rP*0.13,6,18),_pm);
        rb.rotation.x=Math.PI/2; rb.position.set(_lp.x,_lp.y+gy*(0.2+r2*0.2),_lp.z); grp.add(rb); }"""
b = """    try{ if(window._STAGE_JACK_POST!==false && gy>6){
      const _lp=grp.worldToLocal(new THREE.Vector3(mx,0,mz));
      window._quantumPost(grp,_lp.x,_lp.y,_lp.z,HU,gy,(typeof _cc!=='undefined'&&_cc&&_cc.clone)?_cc.clone():new THREE.Color(0x9d7bff));"""
assert s.count(a)==1
s=s.replace(a,b)

# define the shared builder just before _buildQuantumUnit
a2="""function _buildQuantumUnit(H,colHex){"""
b2 = """// ── THE UNIT'S MAST ── plinth, glow ring, ribbed column. Pulled out of the stage build so BOTH quantum units are the
// same object by construction rather than by two sets of numbers kept in step by hand. The customise-screen unit stood
// flat on the floor while the deploy-room one arrived on a mast, so the machine visibly changed shape across the
// handoff - the two are meant to read as ONE machine you never left. Same code, same proportions, one knob for height.
window._quantumPost=function(grp,lx,ly,lz,HU,gy,pcol){ try{
  const _pc=pcol||new THREE.Color(0x9d7bff);
  const _pm=new THREE.MeshStandardMaterial({color:0x131a2c,metalness:0.8,roughness:0.35,emissive:_pc.clone().multiplyScalar(0.22),toneMapped:false});
  const _gm=new THREE.MeshBasicMaterial({color:_pc,transparent:true,opacity:0.75,blending:THREE.AdditiveBlending,depthWrite:false,toneMapped:false});
  const _rP=HU*0.16;
  { const base=new THREE.Mesh(new THREE.CylinderGeometry(_rP*2.6,_rP*3.1,HU*0.10,16),_pm); base.position.set(lx,ly+HU*0.05,lz); grp.add(base); }
  { const ring=new THREE.Mesh(new THREE.TorusGeometry(_rP*2.9,_rP*0.16,8,24),_gm); ring.rotation.x=Math.PI/2; ring.position.set(lx,ly+HU*0.11,lz); grp.add(ring); }
  { const col3=new THREE.Mesh(new THREE.CylinderGeometry(_rP,_rP*1.25,gy+HU*0.12,14),_pm); col3.position.set(lx,ly+(gy+HU*0.12)*0.5,lz); grp.add(col3); }
  for(let r2=0;r2<4;r2++){ const rb=new THREE.Mesh(new THREE.TorusGeometry(_rP*1.14,_rP*0.13,6,18),_pm);
    rb.rotation.x=Math.PI/2; rb.position.set(lx,ly+gy*(0.2+r2*0.2),lz); grp.add(rb); }
}catch(_){} };
function _buildQuantumUnit(H,colHex){"""
assert s.count(a2)==1
s=s.replace(a2,b2)

# ── the customise-screen unit gets the SAME mast, at the same proportion of its own height ──
a3="""  const mach=_buildQuantumUnit(H*(window._DRESS_JACK_SCALE!=null?window._DRESS_JACK_SCALE:0.58),col); grp.add(mach);"""
b3 = """  const _machH=H*(window._DRESS_JACK_SCALE!=null?window._DRESS_JACK_SCALE:0.58);
  const mach=_buildQuantumUnit(_machH,col); grp.add(mach);
  // Stand it on the same mast the deploy-room unit arrives on. The stage lifts its unit by the pilot's foot plane,
  // which measures ~0.18 of the unit's own height; matching that ratio here makes the two silhouettes identical
  // instead of "the one with a base and the one without". _DRESS_JACK_POST=0 puts it back flat on the floor.
  try{ const _pg=(window._DRESS_JACK_POST!=null?window._DRESS_JACK_POST:0.18)*_machH;
    if(_pg>0.001 && window._quantumPost){ mach.position.y+=_pg; window._quantumPost(grp,mach.position.x,0,mach.position.z,_machH,_pg,new THREE.Color(col)); } }catch(_){}"""
assert s.count(a3)==1
s=s.replace(a3,b3)

assert s.count('BUILD &#8734;-CMB1515')==1 and s.count('∞-CMB1515')==1
s=s.replace('BUILD &#8734;-CMB1515','BUILD &#8734;-CMB1516').replace('∞-CMB1515','∞-CMB1516')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
