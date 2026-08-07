import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

# ── 1. CONTROLS: back to the TANK ──
a="""    if(this._bikeMode && window._RIDE_FRONT_STEER!==false){"""
b = """    // FRONT-STEER IS OFF BY DEFAULT. It is a faithful vehicle model and it is the wrong one here: yaw rate is
    // (speed/wheelbase)*tan(lock), so reversing INVERTS the steering - hold the left stick back while turning right
    // and the two genuinely cancel, which is the "I can't make sharp turns" and the muddled two-stick feel. The
    // jet-ski quality wanted from this was never the physics; it is the visual spring further down. _RIDE_FRONT_STEER
    // =true brings the carve model back.
    if(this._bikeMode && window._RIDE_FRONT_STEER===true){"""
assert s.count(a)==1
s=s.replace(a,b)

# strafe fade + grip were part of taming the carve; with the tank back they are just drift from the original feel
a2="""    const _stF=1-(window._BIKE_STRAFE_FADE!=null?window._BIKE_STRAFE_FADE:0.78)*Math.min(1,Math.abs(this._skSpeed||0)/MAXV);"""
b2 = """    const _stF=1-(window._BIKE_STRAFE_FADE!=null?window._BIKE_STRAFE_FADE:0)*Math.min(1,Math.abs(this._skSpeed||0)/MAXV);   // introduced to stop strafe fighting the carve; with the tank back it is just drift from the feel that worked"""
assert s.count(a2)==1
s=s.replace(a2,b2)

a3="""      const grip=(window._BIKE_GRIP!=null?window._BIKE_GRIP:4.0)*(1-(window._BIKE_SLIP_K!=null?window._BIKE_SLIP_K:0.55)*sk);"""
b3 = """      const grip=(window._BIKE_GRIP!=null?window._BIKE_GRIP:4.4)*(1-(window._BIKE_SLIP_K!=null?window._BIKE_SLIP_K:0.62)*sk);   // back to the original grip/slip"""
assert s.count(a3)==1
s=s.replace(a3,b3)

# ── 2. THE VISUAL SPRING ── cosmetic only
a4="""  const g=BIKE.grp, nth=player._skHeading||0, F=(window._BIKE_FWD!=null?window._BIKE_FWD:7);
  g.position.set(player.wx+Math.sin(nth)*F, (player.py||0)-14, player.wz+Math.cos(nth)*F);   // bike sits a touch AHEAD so the seat (rear of centre) lands under the straddle
  g.rotation.y=nth;"""
b4 = """  const g=BIKE.grp, nth=player._skHeading||0, F=(window._BIKE_FWD!=null?window._BIKE_FWD:7);
  // ══ VISUAL SPRING ══ purely cosmetic, and deliberately so. The vehicle's LOGICAL heading, position, hitbox, guns
  // and every control read the raw values below - none of this touches them. Only the DRAWN model is spring-loaded to
  // where the vehicle actually is, so it leans late into a turn, overshoots coming out of one, and rebounds like an
  // elastic band when you stop a hard strafe. That is the jet-ski quality; it was never meant to be in the physics.
  // window._BIKE_VSPRING=false draws the model rigidly on the logical pose.
  const _vs=(window._BIKE_VSPRING!==false), _vdt=Math.min(dt,0.05);
  let _vYaw=nth;
  if(_vs){
    if(BIKE._vYaw==null){ BIKE._vYaw=nth; BIKE._vYawV=0; }
    let _e=nth-BIKE._vYaw; _e=Math.atan2(Math.sin(_e),Math.cos(_e));
    BIKE._vYawV=(BIKE._vYawV||0)+(_e*(window._BIKE_VS_YAW_K||64)-(BIKE._vYawV||0)*(window._BIKE_VS_YAW_D||8.4))*_vdt;   // zeta ~0.52: it overshoots the heading and settles back
    BIKE._vYaw+=BIKE._vYawV*_vdt;
    _vYaw=BIKE._vYaw;
    // LATERAL REBOUND — the body is thrown by CHANGES in sideways velocity (starting or stopping a strafe, snapping
    // out of a turn) and springs back to centre. This is the elastic-band flick.
    const _lat=(player._strafeV||0);
    const _dl=(_lat-(BIKE._latPrev||0)); BIKE._latPrev=_lat;
    BIKE._vLatV=((BIKE._vLatV||0)+(-(BIKE._vLat||0)*(window._BIKE_VS_LAT_K||58)-(BIKE._vLatV||0)*(window._BIKE_VS_LAT_D||7.6))*_vdt) - _dl*(window._BIKE_VS_LAT_KICK||0.035);
    BIKE._vLat=Math.max(-14,Math.min(14,(BIKE._vLat||0)+BIKE._vLatV*_vdt));
  } else { BIKE._vYaw=null; BIKE._vLat=0; BIKE._vLatV=0; }
  const _rgx=Math.cos(nth), _rgz=-Math.sin(nth);                                  // bike-local RIGHT, for the lateral throw
  const _bob=_vs?Math.sin(performance.now()*0.0021)*(window._BIKE_VS_BOB||1.5):0;   // idles with a slight bob within its own space
  g.position.set(player.wx+Math.sin(nth)*F+_rgx*(BIKE._vLat||0), (player.py||0)-14+_bob, player.wz+Math.cos(nth)*F+_rgz*(BIKE._vLat||0));   // bike sits a touch AHEAD so the seat (rear of centre) lands under the straddle
  g.rotation.y=_vYaw;"""
assert s.count(a4)==1
s=s.replace(a4,b4)

# bank gets the same treatment: a spring ON TOP of the existing ease, so exiting a lean rebounds
a5="""  BIKE._bankS=(BIKE._bankS||0)+((lean*(window._BIKE_BANK!=null?window._BIKE_BANK:1.0))-(BIKE._bankS||0))*Math.min(1,dt*(window._BIKE_BANK_EASE||4.5));
  g.rotation.z=BIKE._bankS;"""
b5 = """  BIKE._bankS=(BIKE._bankS||0)+((lean*(window._BIKE_BANK!=null?window._BIKE_BANK:1.0))-(BIKE._bankS||0))*Math.min(1,dt*(window._BIKE_BANK_EASE||4.5));
  // ...and the DRAWN lean springs around that eased target, so coming out of a hard carve it over-corrects, corrects
  // and settles instead of just decaying to level. Same rule: cosmetic only - _bankS stays the authority everything
  // else (the rider's coupling, the seat arc) reads.
  if(_vs){ if(BIKE._vBank==null){ BIKE._vBank=BIKE._bankS; BIKE._vBankV=0; }
    BIKE._vBankV=(BIKE._vBankV||0)+(((BIKE._bankS||0)-BIKE._vBank)*(window._BIKE_VS_BANK_K||70)-(BIKE._vBankV||0)*(window._BIKE_VS_BANK_D||8.6))*_vdt;
    BIKE._vBank+=BIKE._vBankV*_vdt;
  } else BIKE._vBank=BIKE._bankS;
  g.rotation.z=(_vs?BIKE._vBank:BIKE._bankS);"""
assert s.count(a5)==1
s=s.replace(a5,b5)

# the rider rides the VISUAL pose, or he detaches from the bike he is sitting on
a6="""  try{ if(player.model&&window._BIKE_RIDER_LOCK!==false)player.model.rotation.z=BIKE._bankS*(window._BIKE_RIDER_BANK!=null?window._BIKE_RIDER_BANK:0.55); }catch(_){}
  if(window._BIKE_AIM_LOCK!==false){ player.aim=Math.PI/2-g.rotation.y; player._visAim=player.aim; }   // the right stick must not swivel the CHARACTER — he faces where the bike points"""
b6 = """  // The rider follows the DRAWN bike, not the logical one - otherwise the spring visibly detaches him from the machine
  // he is sitting on. His aim, though, stays on the LOGICAL heading: the wobble is a look, never an aiming error.
  try{ if(player.model&&window._BIKE_RIDER_LOCK!==false){
    player.model.rotation.z=(_vs?BIKE._vBank:BIKE._bankS)*(window._BIKE_RIDER_BANK!=null?window._BIKE_RIDER_BANK:0.55);
    player.model.rotation.y=_vYaw; } }catch(_){}
  if(window._BIKE_AIM_LOCK!==false){ player.aim=Math.PI/2-nth; player._visAim=player.aim; }   // the right stick must not swivel the CHARACTER — he faces where the bike points"""
assert s.count(a6)==1
s=s.replace(a6,b6)

# and he shares the lateral throw + bob so the pair move as one object
a7="""      const _B0=window.BIKE, _bk=(_B0&&_B0._bankS!=null)?_B0._bankS:"""
b7 = """      const _B0=window.BIKE, _bk=(_B0&&_B0._vBank!=null)?_B0._vBank:(_B0&&_B0._bankS!=null)?_B0._bankS:"""
assert s.count(a7)==1
s=s.replace(a7,b7)

# ── 3. DRAGON: half again ──
a8="""    const _k=(window._DRAGON_SPAN||24)/68;"""
b8 = """    const _k=(window._DRAGON_SPAN||12)/68;"""
assert s.count(a8)==1
s=s.replace(a8,b8)
a9="""      d.scale.multiplyScalar((window._DRAGON_SPAN||24)/((raw>1e-9?raw:1)*gs));"""
b9 = """      d.scale.multiplyScalar((window._DRAGON_SPAN||12)/((raw>1e-9?raw:1)*gs));"""
assert s.count(a9)==1
s=s.replace(a9,b9)

assert s.count('BUILD &#8734;-CMB1513')==1 and s.count('∞-CMB1513')==1
s=s.replace('BUILD &#8734;-CMB1513','BUILD &#8734;-CMB1514').replace('∞-CMB1513','∞-CMB1514')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
