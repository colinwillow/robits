import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── A. FALL FASTER — the settle was 28% of the climb; target ~65% ──
a="""        const _sink=_hHold?0:(window._BIKE_FLY_SINK!=null?window._BIKE_FLY_SINK:135);   // hover-hold = neutral buoyancy, it just hangs"""
b="""        // SINK vs LIFT set the two terminal speeds, and they are coupled: climb=(LIFT-SINK)/DRAG, fall=SINK/DRAG.
        // The first pass (135/620/2.6) gave 186 up but only 52 down — a 28% ratio, which is the "falls way too slow".
        // Raising SINK alone would just have eaten the climb, so both move: 312/795/2.6 -> 186 up, 120 down = 65%.
        const _sink=_hHold?0:(window._BIKE_FLY_SINK!=null?window._BIKE_FLY_SINK:312);   // hover-hold = neutral buoyancy, it just hangs"""
assert s.count(a)==1
s=s.replace(a,b)

a2="""(_flyLift?(window._BIKE_FLY_LIFT!=null?window._BIKE_FLY_LIFT:620):"""
b2="""(_flyLift?(window._BIKE_FLY_LIFT!=null?window._BIKE_FLY_LIFT:795):"""
assert s.count(a2)==1
s=s.replace(a2,b2)

# ── B. HEAVY ROUNDS: a vehicle gun must hit like one ──
# knock: the bullet path hard-coded forceMul 0.1, so damage alone could never shove anything
a3="""        kt+=0.015; const pts=e.hit(b.dmg, b.wx, b.wz, b.y); e.knock(b.vx,b.vz,b.dmg,0.1); if(b.pierce>0){b.pierce--;b.hitSet.add(e);}else b.life=0;"""
b3="""        // forceMul was pinned at 0.1 for EVERY round, so a heavier bullet could only ever do more damage - never shove
        // harder. force = 0.85*dmg*vuln*forceMul, so a vehicle cannon at 0.1 lands the same nudge as a pistol round.
        // _kbMul/_kbLift let a round carry its own weight; unset, every existing bullet keeps the exact old 0.1 nudge.
        kt+=0.015; const pts=e.hit(b.dmg, b.wx, b.wz, b.y); e.knock(b.vx,b.vz,b.dmg,(b._kbMul!=null?b._kbMul:0.1),(b._kbLift||0)); if(b.pierce>0){b.pierce--;b.hitSet.add(e);}else b.life=0;"""
assert s.count(a3)==1
s=s.replace(a3,b3)

# spiders get a FIXED shove regardless of what hit them -> scale it by the round's weight
a4="""if(e._isCrawler && e.alive){ const _kl=Math.hypot(b.vx||0,b.vz||0)||1; e._shoveVx=(b.vx/_kl)*(window._SPIDER_SHOVE||95); e._shoveVz=(b.vz/_kl)*(window._SPIDER_SHOVE||95);"""
b4="""if(e._isCrawler && e.alive){ const _kl=Math.hypot(b.vx||0,b.vz||0)||1, _hv=(b._heavy||1); e._shoveVx=(b.vx/_kl)*(window._SPIDER_SHOVE||95)*_hv; e._shoveVz=(b.vz/_kl)*(window._SPIDER_SHOVE||95)*_hv;"""
assert s.count(a4)==1
s=s.replace(a4,b4)

# grid: a heavy round leaves a crater, not a dent — and its travel wake is proportionally deeper
a5="""      if(_h){ _h.sheet.impactLocal(_h.lu,_h.lv,this._shotgun?(window._SHOT_IMPACT||4.2):(this.kind==='laser'?2.6:1.6)); if(typeof gridSheetsTint==='function')try{ gridSheetsTint(this.wx,this.y,this.wz,(this._shotgun?(window._SHOT_TINT_R||34):(window._BULLET_TINT_R||24)),_btc,(window._BULLET_TINT||0.6)); }catch(_){}"""
b5="""      if(_h){ const _hv=(this._heavy||1);
        _h.sheet.impactLocal(_h.lu,_h.lv,(this._shotgun?(window._SHOT_IMPACT||4.2):(this.kind==='laser'?2.6:1.6))*_hv);
        // A HEAVY round punches a real crater. Narrow on purpose (opt.rad ~ one grid cell): the plasma-orb lesson is
        // that width is what turns a hit into a field-wide smear, so the weight goes into DEPTH instead.
        if(_hv>1.5 && typeof gridSheetsBlast==='function')try{ gridSheetsBlast(this.wx,this.y,this.wz,(window._HEAVY_BLAST_PW||4)*_hv,(window._HEAVY_BLAST_YR||70),_btc,0.7,{rad:(window._HEAVY_BLAST_RAD||56),shockMul:(window._HEAVY_BLAST_SHOCK!=null?window._HEAVY_BLAST_SHOCK:0.3)}); }catch(_){}
        if(typeof gridSheetsTint==='function')try{ gridSheetsTint(this.wx,this.y,this.wz,(this._shotgun?(window._SHOT_TINT_R||34):(window._BULLET_TINT_R||24))*Math.min(2,_hv),_btc,(window._BULLET_TINT||0.6)); }catch(_){}"""
assert s.count(a5)==1
s=s.replace(a5,b5)

a6="""      else { gridSheetWake(this.wx,this.y,this.wz,(this._shotgun?(window._SHOT_WAKE||7):(window._BULLET_WAKE||2.6)));"""
b6="""      else { gridSheetWake(this.wx,this.y,this.wz,(this._shotgun?(window._SHOT_WAKE||7):(window._BULLET_WAKE||2.6))*(this._heavy||1));"""
assert s.count(a6)==1
s=s.replace(a6,b6)

# ── the bike's own guns declare themselves heavy ──
a7="""        b.dmg=(window._BIKE_SHOT_DMG!=null?window._BIKE_SHOT_DMG:2.5); b.pierce=1;"""
b7="""        // A VEHICLE GUN MUST OUT-HIT THE RIFLE YOU ARRIVED ON. At 2.5 it barely beat a plain laser round (2), and the
        // knock was the universal 0.1 nudge, so riding up to a spider and firing was strictly worse than dismounting.
        b.dmg=(window._BIKE_SHOT_DMG!=null?window._BIKE_SHOT_DMG:8); b.pierce=1;
        b._kbMul=(window._BIKE_SHOT_KB!=null?window._BIKE_SHOT_KB:0.5);      // blasts them BACK, not a nudge
        b._kbLift=(window._BIKE_SHOT_LIFT!=null?window._BIKE_SHOT_LIFT:90);  // ...and off their feet
        b._heavy=(window._BIKE_SHOT_HEAVY!=null?window._BIKE_SHOT_HEAVY:3);  // craters the grid, drags a deeper wake
        b._gridCol=(window._BIKE_SHOT_COL!=null?window._BIKE_SHOT_COL:0xaef4ff);"""
assert s.count(a7)==1
s=s.replace(a7,b7)

assert s.count('BUILD &#8734;-CMB1499')==1 and s.count('∞-CMB1499')==1
s=s.replace('BUILD &#8734;-CMB1499','BUILD &#8734;-CMB1500').replace('∞-CMB1499','∞-CMB1500')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
