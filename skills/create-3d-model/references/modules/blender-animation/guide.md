# Blender animation

Choose object transforms, shape keys, actions, drivers, or material changes from the requested motion and playback target. Preserve unrelated animation and the agreed timing, frame rate, and coordinate convention.

Use interpolation suited to the movement: constant velocity, eased movement, or stepped states. Match endpoints for loops and inspect intermediate frames for flips, clipping, and deformation. Bake or adapt mechanisms unsupported by the destination; a Blender Python handler alone does not establish portable playback.

Read [animation recipes](recipes.md) for keyframe, action, driver, NLA, or shape-key examples; check the installed Blender API before applying them. Read [advanced animation](references/overview.md) for curve control, reusable actions or facial animation.

Use [animation validation](../animation-quality-gate/guide.md) for changed motion. Completion requires the requested motion, inspected representative frames, and verified target playback or an explicit limitation.
