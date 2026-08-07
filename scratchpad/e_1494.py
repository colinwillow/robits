import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# 1) impactLocal: optional deform-radius override + shock scaling
a1="""  impactLocal(lu,lv,power,col){   // localized blast = ground's landing formula, toned to ~0.6x ground
    power*=(this._defMul!=null?this._defMul:1);   // per-sheet amplitude scale (platform disc dials it down)
    if(!this._cubeWall) power*=0.6;   // cube faces hit at FULL ground strength so the deform/shock reads
    this.shock(lu,lv,power,col);   // the expanding ripple carries the blast colour
    const rad=40+power*10;"""
b1="""  impactLocal(lu,lv,power,col,opt){   // localized blast = ground's landing formula, toned to ~0.6x ground
    power*=(this._defMul!=null?this._defMul:1);   // per-sheet amplitude scale (platform disc dials it down)
    if(!this._cubeWall) power*=0.6;   // cube faces hit at FULL ground strength so the deform/shock reads
    // opt.rad DECOUPLES the crater's WIDTH from its POWER. Without it rad grows with power (40+power*10), so the only
    // way to press deeper is to press wider — which is exactly how a travel wake turns into a field-wide smear.
    // opt.shockMul scales (or with 0, silences) the expanding ripple, which travels the WHOLE sheet regardless of power.
    const _sm=(opt&&opt.shockMul!=null)?opt.shockMul:1;
    if(_sm>0) this.shock(lu,lv,power*_sm,col);   // the expanding ripple carries the blast colour
    const rad=(opt&&opt.rad!=null)?opt.rad:(40+power*10);"""
assert s.count(a1)==1, s.count(a1)
s=s.replace(a1,b1)

# 2) gridSheetsBlast: thread opt through; tint honours the narrow radius; wake ticks skip the heavy asset/platform fan-out
a2="""function gridSheetsBlast(wx,wy,wz,power,radius,col,tintAmt){"""
b2="""function gridSheetsBlast(wx,wy,wz,power,radius,col,tintAmt,opt){"""
assert s.count(a2)==1
s=s.replace(a2,b2)

a3="""  if(window._DEFORM_UNIFY!==false && (power||1)>=(window._DEFORM_UNIFY_MIN!=null?window._DEFORM_UNIFY_MIN:2) && typeof window._arenaDeformShock==='function'"""
b3="""  if(!(opt&&opt.noAsset) && window._DEFORM_UNIFY!==false && (power||1)>=(window._DEFORM_UNIFY_MIN!=null?window._DEFORM_UNIFY_MIN:2) && typeof window._arenaDeformShock==='function'"""
assert s.count(a3)==1
s=s.replace(a3,b3)

a4="""      if(fo>0.02) sh.impactLocal(clamp(_gsV.x,-sh.hw,sh.hw), clamp(_gsV.z,-sh.hd,sh.hd), power*fo, col);   // pass the blast colour so the expanding ripple carries it"""
b4="""      if(fo>0.02) sh.impactLocal(clamp(_gsV.x,-sh.hw,sh.hw), clamp(_gsV.z,-sh.hd,sh.hd), power*fo, col, opt);   // pass the blast colour so the expanding ripple carries it"""
assert s.count(a4)==1
s=s.replace(a4,b4)

a5="""  if(col!=null && typeof gridSheetsTint==='function') gridSheetsTint(wx,wy,wz,radius,col,(tintAmt!=null?tintAmt:(window._GRID_TINT_BLAST||0.85)));   // paint the blast the projectile's colour"""
b5="""  if(col!=null && typeof gridSheetsTint==='function') gridSheetsTint(wx,wy,wz,((opt&&opt.rad!=null)?opt.rad:radius),col,(tintAmt!=null?tintAmt:(window._GRID_TINT_BLAST||0.85)));   // paint the blast the projectile's colour — a narrow crater paints a narrow stripe, not the whole slab"""
assert s.count(a5)==1
s=s.replace(a5,b5)

a6="""  if(window._ASSET_BLAST_REACT!==false && typeof _arenaDeformShock==='function'"""
b6="""  if(!(opt&&opt.noAsset) && window._ASSET_BLAST_REACT!==false && typeof _arenaDeformShock==='function'"""
assert s.count(a6)==1
s=s.replace(a6,b6)

a7="""  if(window._PLAT_DEFORM!==false && typeof window._platDeformShock==='function' && window._platDeform){"""
b7="""  if(!(opt&&opt.noAsset) && window._PLAT_DEFORM!==false && typeof window._platDeformShock==='function' && window._platDeform){"""
assert s.count(a7)==1
s=s.replace(a7,b7)

# 3) _gridBowl / _gridSpiral: optional vertical REACH + per-point opt (rad scales with each sub-blast's share)
a8="""window._gridBowl=function(x,y,z,R,pw,col,rings){ try{
  if(typeof gridSheetsBlast!=='function'||typeof GRID_SHEETS==='undefined'||!GRID_SHEETS.length)return;
  const N=Math.max(1,rings||(window._BOWL_RINGS||4));
  gridSheetsBlast(x,y,z,pw,R*0.4,col,0.8);                                    // the throat
  for(let i=1;i<=N;i++){ const f=i/N, rr=R*f, prof=Math.sqrt(Math.max(0,1-f*f));   // hemisphere falloff
    const n=4+i*3;
    for(let k=0;k<n;k++){ const a=(k/n)*Math.PI*2+i*0.7;
      gridSheetsBlast(x+Math.cos(a)*rr, y, z+Math.sin(a)*rr, pw*prof, R*0.34, col, 0.45); } }
}catch(_){} };"""
b8="""// yr (optional) overrides the VERTICAL reach used to gate/soften each sub-blast. It is normally tied to R, which couples
// "how far above the floor the source may be" to "how wide the crater is" — fine for an explosion, wrong for a narrow
// deep press from a ball flying at chest height. opt (optional) is forwarded to gridSheetsBlast; opt.rad is scaled per
// sub-blast so the ring points keep their relative footprint.
window._gridBowl=function(x,y,z,R,pw,col,rings,yr,opt){ try{
  if(typeof gridSheetsBlast!=='function'||typeof GRID_SHEETS==='undefined'||!GRID_SHEETS.length)return;
  const N=Math.max(1,rings||(window._BOWL_RINGS||4));
  const _o=(opt&&opt.rad!=null)?(k=>Object.assign({},opt,{rad:opt.rad*k})):(()=>opt||undefined);
  gridSheetsBlast(x,y,z,pw,(yr!=null?yr:R*0.4),col,0.8,_o(0.55));             // the throat
  for(let i=1;i<=N;i++){ const f=i/N, rr=R*f, prof=Math.sqrt(Math.max(0,1-f*f));   // hemisphere falloff
    const n=4+i*3;
    for(let k=0;k<n;k++){ const a=(k/n)*Math.PI*2+i*0.7;
      gridSheetsBlast(x+Math.cos(a)*rr, y, z+Math.sin(a)*rr, pw*prof, (yr!=null?yr:R*0.34), col, 0.45, _o(0.4)); } }
}catch(_){} };"""
assert s.count(a8)==1
s=s.replace(a8,b8)

a9="""window._gridSpiral=function(x,y,z,R,col,pw,t){ try{
  if(typeof gridSheetsBlast!=='function'||typeof GRID_SHEETS==='undefined'||!GRID_SHEETS.length)return;
  const ARM=(window._MSP_ARMS||3), SPIN=(window._MSP_SPIN||2.8), MARCH=(window._MSP_MARCH||0.9), TW=(window._MSP_TWIST||3.2);
  for(let a2=0;a2<ARM;a2++){ const frac=(((t*MARCH+a2/ARM)%1)+1)%1;
    const rr=R*(0.15+frac*0.85), th=t*SPIN+a2*(Math.PI*2/ARM)+frac*TW;   // the twist bends each arm into a spiral instead of a spoke
    gridSheetsBlast(x+Math.cos(th)*rr, y, z+Math.sin(th)*rr, pw*(1-frac*0.5), R*0.35, col, 0.5); }
  gridSheetsBlast(x,y,z,pw*0.7,R*0.5,col,0.55);   // and the throat keeps pulling
}catch(_){} };"""
b9="""window._gridSpiral=function(x,y,z,R,col,pw,t,yr,opt){ try{
  if(typeof gridSheetsBlast!=='function'||typeof GRID_SHEETS==='undefined'||!GRID_SHEETS.length)return;
  const ARM=(window._MSP_ARMS||3), SPIN=(window._MSP_SPIN||2.8), MARCH=(window._MSP_MARCH||0.9), TW=(window._MSP_TWIST||3.2);
  const _o=(opt&&opt.rad!=null)?(k=>Object.assign({},opt,{rad:opt.rad*k})):(()=>opt||undefined);
  for(let a2=0;a2<ARM;a2++){ const frac=(((t*MARCH+a2/ARM)%1)+1)%1;
    const rr=R*(0.15+frac*0.85), th=t*SPIN+a2*(Math.PI*2/ARM)+frac*TW;   // the twist bends each arm into a spiral instead of a spoke
    gridSheetsBlast(x+Math.cos(th)*rr, y, z+Math.sin(th)*rr, pw*(1-frac*0.5), (yr!=null?yr:R*0.35), col, 0.5, _o(0.4)); }
  gridSheetsBlast(x,y,z,pw*0.7,(yr!=null?yr:R*0.5),col,0.55,_o(0.55));   // and the throat keeps pulling
}catch(_){} };"""
assert s.count(a9)==1
s=s.replace(a9,b9)

# 4) THE WAKE ITSELF — width off the BALL, drama into Y
a10="""        try{ const _pw=(window._PORB_WAKE_PW0||3.2)+this.ch*(window._PORB_WAKE_PW1||4.5), _r=(window._PORB_WAKE_R0||85)+this.ch*(window._PORB_WAKE_R1||70);
          if(window._gridBowl)window._gridBowl(this.x,this.y,this.z,_r*(window._PORB_BOWL_R||2.3),_pw*(window._PORB_BOWL_PW||5.0),this._col,(window._PORB_BOWL_RINGS||3));   // THE TRAIL is the effect worth having — widened and driven much harder. Ring COUNT stays at 3 on purpose: each ring is a full sheet walk, so depth/width buy drama far cheaper than more rings.
          if(window._gridSpiral)window._gridSpiral(this.x,this.y,this.z,_r,this._col,_pw,this._sw*(window._PORB_SPIRAL_T||1));   // ...with the mini-singularity spiral turning inside it
          else gridSheetsBlast(this.x,this.y,this.z,_pw,_r,this._col); }catch(_){} } }"""
b10="""        try{ const _pw0=(window._PORB_WAKE_PW0||3.2)+this.ch*(window._PORB_WAKE_PW1||4.5);
          // WIDTH comes off the BALL, not off a fixed constant. It used to be (85 + ch*70) * 2.3 -> ~356 units at full
          // charge against an 18-unit ball: twenty ball-widths of grid churning. The drama belongs on Y instead, so the
          // footprint is ~2 ball radii and the POWER is multiplied up — decoupled via opt.rad, which is the only reason
          // pressing harder no longer means pressing wider. yr keeps the vertical REACH generous so a ball flying at
          // chest height still bites the floor. shockMul mutes the traveling ripple (it crosses the entire sheet no
          // matter how small the crater is, and at 20 wake ticks/second that alone read as "the whole grid going crazy").
          const _rw=this.R*(window._PORB_WAKE_K!=null?window._PORB_WAKE_K:2.2);
          const _pw=_pw0*(window._PORB_WAKE_DEEP!=null?window._PORB_WAKE_DEEP:9);
          const _yr=(window._PORB_WAKE_YR||110);
          const _o={rad:_rw, shockMul:(window._PORB_WAKE_SHOCK!=null?window._PORB_WAKE_SHOCK:0.1), noAsset:(window._PORB_WAKE_ASSET!==true)};
          if(window._gridBowl)window._gridBowl(this.x,this.y,this.z,_rw,_pw,this._col,(window._PORB_BOWL_RINGS||2),_yr,_o);   // a narrow deep punch that follows the ball
          if(window._gridSpiral)window._gridSpiral(this.x,this.y,this.z,_rw*(window._PORB_SPIRAL_R||0.85),this._col,_pw*(window._PORB_SPIRAL_PW||0.5),this._sw*(window._PORB_SPIRAL_T||1),_yr,_o);   // ...with the mini-singularity spiral turning inside it
          else gridSheetsBlast(this.x,this.y,this.z,_pw,_yr,this._col,null,_o); }catch(_){} } }"""
assert s.count(a10)==1
s=s.replace(a10,b10)

# badge
assert s.count('BUILD &#8734;-CMB1493')==1 and s.count('∞-CMB1493')==1
s=s.replace('BUILD &#8734;-CMB1493','BUILD &#8734;-CMB1494').replace('∞-CMB1493','∞-CMB1494')

open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
