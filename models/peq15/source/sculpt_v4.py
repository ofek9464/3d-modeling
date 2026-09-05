"""Exterior-only miniature sculpt using the collected multi-view photographs.

All dimensions here describe the small cosmetic print. Recesses are blind.
The simplified mounting interface is defined separately in build_model.py.
"""
import math
import numpy as np
import manifold3d as md
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties


def build_body(api):
    M=md.Manifold
    box=api['box']; cyl=api['cylinder']; rounded=api['rounded_box']
    union=api['union_all']; subtract=api['subtract_all']; chamfer=api['chamfer_box']

    def cone(r0,r1,h,xyz,axis='z'):
        obj=M.cylinder(h,r0,r1,64,center=True)
        if axis=='y': obj=obj.rotate((90,0,0))
        if axis=='x': obj=obj.rotate((0,90,0))
        return obj.translate(xyz)

    def engraving(text,height,xyz,angle=0):
        path=TextPath((0,0),text,size=height,
            prop=FontProperties(family='DejaVu Sans',weight='normal'))
        polygons=path.to_polygons()
        return md.CrossSection(polygons,md.FillRule.EvenOdd).extrude(.32).rotate((0,0,angle)).translate(xyz)

    # Primary shell: wide across the front, narrowed and sculpted at the rear.
    # Two intersecting rounded volumes soften the top/side transitions.
    shell=rounded((22.6,29.7,9.2),(0,0,8.0),1.45)
    # The molded top drops toward the battery-side wall, with a diagonal
    # shoulder interrupted by the forward adjustment boss.
    wedge=md.CrossSection([[(8.8,12.65),(12.5,10.4),(15,10.4),(15,17),(8.8,17)]]).extrude(29.0).rotate((90,0,0)).translate((0,15.0,0))
    shell-=wedge
    # Lower edge sweeps upward at the rear; retain the center mounting roof.
    for sign in (-1,1):
        scoop=rounded((5.8,9.2,3.1),(sign*9.4,8.3,3.6),1.0)
        shell-=scoop
    # Rear selector corner is rounded into the housing, not a square lid corner.
    rear_cut=box((4.8,5.0,15),(-11.6,15.3,9))
    rear_cut-=cyl(3.2,20,(-8.0,11.7,9))
    shell-=rear_cut
    # Rear relief between the selector lobe and battery shoulder.
    shell-=rounded((4.9,4.6,4.2),(.2,15.7,12.2),1.0)
    # Raised, gently sloping rear-right battery shoulder.
    shoulder=cone(4.08,3.68,13.8,(7.0,7.4,8.1),'y')
    shell+=shoulder
    # Cut shallow underside relief. Roof remains attached to the miniature mount.
    shell-=rounded((8.8,25,3.0),(0,0,2.45),.55)
    # Rear lower edge rises around the center of the housing.
    relief=rounded((25,10.6,4.3),(0,11.6,2.2),1.2)
    relief-=box((12,13,8),(0,10,3))
    shell-=relief

    # Large circular fire-button recess. The floor itself represents the button.
    fx,fy=0.0,3.0
    shell-=cyl(3.48,1.5,(fx,fy,12.85))
    shell-=cone(3.48,3.85,.50,(fx,fy,12.40))
    # Engraved outer boundary of the thin surrounding ring.
    ring=cyl(4.48,.27,(fx,fy,12.58))-cyl(4.31,.8,(fx,fy,12.58))
    shell-=ring

    # Deep selector pocket with a molded knob and radial protective walls.
    sx,sy=-6.0,10.0
    shell-=cyl(3.82,3.3,(sx,sy,12.25))
    shell-=cone(3.82,4.16,.65,(sx,sy,12.35))
    # Shell joint is cut before straps and screw heads are added.
    seam=box((25,.27,14),(0,-10.35,8))-rounded((22.0,20,8.6),(0,-10.35,8),1.3)
    shell-=seam
    shell-=box((20.2,.24,.25),(0,-10.35,12.57))
    parts=[shell,
           cone(2.0,1.82,2.20,(sx,sy,11.65)),
           cone(1.82,1.46,.48,(sx,sy,12.99))]
    # Selector pointer extends out of the knob, with a shallow split grip line.
    pointer=chamfer((1.25,2.35,1.0),(sx,sy-1.45,12.28),.25)
    pointer-=box((.25,1.65,.45),(sx,sy-1.8,12.72))
    parts.append(pointer)
    for a in [0,80,170,260]:
        ar=math.radians(a)
        guard=chamfer((1.05,1.5,2.0),(0,0,0),.22)
        guard=guard.rotate((0,0,a-90)).translate((sx+3.55*math.cos(ar),sy+3.55*math.sin(ar),11.8))
        parts.append(guard)
    # Small screw beside the selector. The bore is shallow and cosmetic.
    blue=cyl(.62,1.85,(sx-2.5,sy-1.15,11.47))
    blue-=cyl(.29,.6,(sx-2.5,sy-1.15,12.45))
    parts.append(blue)

    # Paired top adjustment screws, on either side ahead of the main button.
    for x in (-7.1,7.1):
        y=-2.0
        base=cone(2.42,2.05,.55,(x,y,12.40))
        base+=cyl(1.88,.18,(x,y,12.71))
        # Thin annular separation and six notches distinguish surround and screw.
        base-=cyl(1.42,.45,(x,y,12.74))-cyl(1.25,.8,(x,y,12.74))
        base-=box((2.70,.48,.8),(x,y,12.90))
        for a in range(0,360,60):
            ar=math.radians(a)
            base-=cyl(.23,.55,(x+1.7*math.cos(ar),y+1.7*math.sin(ar),13.15),segments=12)
        parts.append(base)

    # Dual-aperture cover, shorter than the adjacent ribbed cylindrical cover.
    lx,lz=-6.85,7.45
    parts += [cone(3.45,3.1,2.5,(lx,-14.9,lz),'y'),
              cyl(3.12,2.15,(lx,-16.5,lz),'y'),
              cyl(3.42,.45,(lx,-17.68,lz),'y')]
    front_left=cyl(3.57,.85,(lx,-18.30,lz),'y')
    front_left-=cyl(.92,1.0,(lx+1.30,-18.73,lz+.2),'y')
    front_left-=cyl(.80,1.0,(lx-1.24,-18.73,lz-.2),'y')
    front_left-=cyl(.20,.45,(lx,-18.80,lz-.05),'y',16)
    parts.append(front_left)

    # Molded cover strap, anchored on the top and folded over the front cover.
    strap=rounded((1.85,3.8,.62),(lx,-11.95,12.62),.25)
    # A continuous diagonal strap follows the photo's folded silhouette.
    strap+=M.hull_points([(lx+dx,y,z) for dx in (-.925,.925)
        for y,z in [(-13.5,12.3),(-13.5,12.92),(-18.1,10.45),(-18.1,11.07)]])
    strap+=rounded((1.85,1.0,.62),(lx,-18.05,10.73),.25)
    # Lower the nose end to follow the round cover, keeping all details fused.
    parts += [strap,cone(1.55,1.30,.62,(lx,-10.45,12.82))]
    # The tiny center is a paint recess, not a through-hole.
    parts[-1]-=cyl(.51,.4,(lx,-10.45,13.11))

    # Longer front cylinder with twelve rounded flutes and a cover-retention strap.
    rx,rz=6.8,7.35
    parts += [cone(3.95,3.48,1.8,(rx,-14.6,rz),'y'),
              cyl(3.27,1.1,(rx,-15.75,rz),'y')]
    ribbed=cyl(3.40,4.4,(rx,-17.75,rz),'y')
    for a in np.linspace(0,2*math.pi,12,endpoint=False):
        cutter=rounded((.78,3.20,.78),
            (rx+3.43*math.cos(a),-17.78,rz+3.43*math.sin(a)),.36)
        ribbed-=cutter
    parts += [ribbed,cyl(3.47,.50,(rx,-20.10,rz),'y')]
    right_lid=cyl(3.47,.85,(rx,-20.78,rz),'y')
    right_lid-=cyl(.98,1.0,(rx,-21.22,rz),'y')
    parts.append(right_lid)
    parts += [rounded((1.85,6.1,.66),(rx,-18.02,10.60),.26),
              rounded((1.85,.76,1.02),(rx,-20.76,10.28),.28)]

    # Rear battery cap with a narrow collar and fine grip ribs.
    bx,bz=7.0,8.0
    parts += [cyl(3.25,2.7,(bx,14.5,bz),'y'),cyl(3.54,.44,(bx,15.65,bz),'y')]
    cap=cyl(3.48,2.35,(bx,17.0,bz),'y')
    for a in np.linspace(0,2*math.pi,36,endpoint=False):
        cap-=cyl(.15,2.6,(bx+3.48*math.cos(a),17.0,bz+3.48*math.sin(a)),'y',12)
    parts += [cap,cyl(3.28,.40,(bx,18.17,bz),'y'),cyl(.75,.5,(bx,18.48,bz),'y')]
    # Small rear lanyard tab as a thick, fused decorative loop.
    loop=cyl(1.45,.75,(bx,18.45,6.55),'y')-cyl(.78,1.2,(bx,18.45,6.55),'y')
    parts.append(loop)

    # Shallow side surrounds follow the housing, with low slotted centers.
    for sign in (-1,1):
        x=sign*11.1; y=.15; z=6.85
        side=cone(2.65,2.18,.55,(0,0,0),'x')
        if sign<0: side=side.rotate((0,0,180))
        side=side.translate((x,y,z))
        side+=cyl(2.08,.40,(sign*11.52,y,z),'x')
        side-=cyl(1.14,.7,(sign*11.75,y,z),'x')-cyl(.98,1.1,(sign*11.75,y,z),'x')
        side-=box((.8,1.7,.4),(sign*11.72,y,z))
        for a in range(0,360,60):
            ar=math.radians(a)
            side-=cyl(.20,.65,(sign*11.8,y+1.82*math.cos(ar),z+1.82*math.sin(ar)),'x',12)
        parts.append(side)

    for i,p in enumerate(parts):
        assert p.status()==md.Error.NoError,('part',i,p.status())
    solid=union(parts)
    assert solid.status()==md.Error.NoError,('union',solid.status())
    cuts=[]
    # Broad shallow label seat on the front lid, printable without a texture.
    cuts.append(rounded((12.7,6.3,.28),(0,-6.55,12.58),.13))
    # Recessed figure-eight side connector, visible in the rear photograph.
    cuts += [cyl(.83,1.45,(-11.20,10.85,9.70),'x'),
             cyl(.83,1.45,(-11.20,12.0,9.70),'x')]
    # Front molded corner recesses and rear connector impressions.
    for x in (-9.6,9.6):
        cuts.append(cyl(.56,1.5,(x,-14.76,9.62),'y'))
    cuts += [cyl(.93,1.3,(-8.3,14.9,6.1),'y'),
             cyl(.65,1.3,(-.3,14.9,5.4),'y'),
             rounded((1.2,2.4,1.0),(-11.3,10.6,10.3),.45)]
    # Small top markings are shallow engravings; labels are not printed stickers.
    cuts += [engraving('FIRE',.82,(-1.03,-2.18,12.40)),
             engraving('U',.85,(-9.0,-.62,12.40)),
             engraving('U',.85,(8.1,-.62,12.40)),
             engraving('D',.85,(-9.0,-4.55,12.40)),
             engraving('D',.85,(8.1,-4.55,12.40))]
    # Markings around the selector, outside the pocket rather than on raised knobs.
    for text,x,y in [('VIS',-.8,10.4),('IR',-.8,11.7),('AL',-3.6,5.9),('DL',-7.6,5.1)]:
        cuts.append(engraving(text,.68,(x,y,12.40)))
    for i,p in enumerate(cuts):
        assert p.status()==md.Error.NoError,('cut',i,p.status())
    return subtract(solid,cuts)
