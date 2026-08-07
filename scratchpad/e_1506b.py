import os
p='/home/user/robits/index.html'
s=open(p,encoding='utf-8').read()

a="""      let bb=new THREE.Box3().setFromObject(d); let sz=bb.getSize(new THREE.Vector3());
      const raw=Math.max(sz.x,sz.y,sz.z)||1e-3;
      const gs=(this._rig.group.scale&&this._rig.group.scale.x)||1;
      d.scale.multiplyScalar((window._DRAGON_SPAN||150)/(raw*gs));
      d.updateMatrixWorld(true); bb.setFromObject(d); sz=bb.getSize(new THREE.Vector3());
      d.position.y-=(bb.min.y+bb.max.y)*0.5;                                    // centre it on the rig origin so the ride/hang offsets still line up"""
b = """      // Measure from the geometry ATTRIBUTES, not Box3.setFromObject. For a SKINNED mesh the object-level box is
      // derived from an unposed bind skeleton, and here it came back wrong by two orders of magnitude - the "fitted"
      // dragon rendered about one unit long. Bind-pose vertex extents times the mesh's own accumulated scale is
      // deterministic and cannot be surprised by skinning.
      const _span=(o3)=>{ let mnx=1e30,mny=1e30,mnz=1e30,mxx=-1e30,mxy=-1e30,mxz=-1e30;
        const _v=new THREE.Vector3(); o3.updateMatrixWorld(true);
        o3.traverse(o=>{ if(!(o.isMesh||o.isSkinnedMesh)||!o.geometry||o._isWireTwin)return;
          if(!o.geometry.boundingBox)o.geometry.computeBoundingBox(); const gb=o.geometry.boundingBox; if(!gb)return;
          for(const cx of [gb.min.x,gb.max.x])for(const cy of [gb.min.y,gb.max.y])for(const cz of [gb.min.z,gb.max.z]){
            _v.set(cx,cy,cz).applyMatrix4(o.matrixWorld);
            if(_v.x<mnx)mnx=_v.x; if(_v.x>mxx)mxx=_v.x; if(_v.y<mny)mny=_v.y; if(_v.y>mxy)mxy=_v.y; if(_v.z<mnz)mnz=_v.z; if(_v.z>mxz)mxz=_v.z; } });
        if(mxx<mnx)return null;
        return {x:mxx-mnx, y:mxy-mny, z:mxz-mnz, cy:(mny+mxy)*0.5}; };
      let sp0=_span(d); const raw=sp0?Math.max(sp0.x,sp0.y,sp0.z):1;
      const gs=(this._rig.group.scale&&this._rig.group.scale.x)||1;
      this._dragonRaw=raw;
      d.scale.multiplyScalar((window._DRAGON_SPAN||150)/((raw>1e-9?raw:1)*gs));
      const sp1=_span(d); const sz=new THREE.Vector3(sp1?sp1.x:0,sp1?sp1.y:0,sp1?sp1.z:0);
      if(sp1)d.position.y-=sp1.cy;                                              // centre it on the rig origin so the ride/hang offsets still line up"""
assert s.count(a)==1
s=s.replace(a,b)
open(p+'.tmp','w',encoding='utf-8').write(s); os.replace(p+'.tmp',p)
print('ok')
