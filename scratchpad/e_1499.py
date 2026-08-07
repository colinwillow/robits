import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()
assert len(s)>5_000_000

a="""        if(m.map){ m.emissiveMap=m.map; m.emissive=new THREE.Color(0xffffff); m.emissiveIntensity=(window._BIKE_GLB_GLOW!=null?window._BIKE_GLB_GLOW:2.4); }   // baked texture self-lit — hotter (1.5 read dim next to the neon world)"""
b="""        // AN AUTHORED EMISSIVE MAP OUTRANKS THE FALLBACK. Rev 01 shipped diffuse only, so the only way to make the bike
        // read in a neon world was to promote the diffuse to emissive wholesale — every pixel self-lit. Rev 02 ships a
        // real emissiveTexture (emissiveFactor [1,1,1]) that says WHICH parts glow, and blindly assigning m.map over it
        // throws that authoring away and floods the whole body at 2.4x. So: honour the map when there is one, and only
        // fall back to lighting the diffuse when there isn't. _BIKE_GLB_EGLOW tunes the authored case (the export's own
        // KHR emissive_strength is used when it declares one, as the 'white' material does at 2).
        if(m.emissiveMap){ m.emissive=new THREE.Color(0xffffff);
          if(window._BIKE_GLB_EGLOW!=null)m.emissiveIntensity=window._BIKE_GLB_EGLOW;
          else if(!(m.emissiveIntensity>1))m.emissiveIntensity=(window._BIKE_GLB_EGLOW_DEF||2.0); }
        else if(m.map){ m.emissiveMap=m.map; m.emissive=new THREE.Color(0xffffff); m.emissiveIntensity=(window._BIKE_GLB_GLOW!=null?window._BIKE_GLB_GLOW:2.4); }   // no authored glow map: baked texture self-lit — hotter (1.5 read dim next to the neon world)"""
assert s.count(a)==1
s=s.replace(a,b)
assert s.count('BUILD &#8734;-CMB1498')==1 and s.count('∞-CMB1498')==1
s=s.replace('BUILD &#8734;-CMB1498','BUILD &#8734;-CMB1499').replace('∞-CMB1498','∞-CMB1499')
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
