# Rebuild the models

The prebuilt files in `models/*/stl` and `models/peq15/3mf` are the download artifacts. Rebuilding writes to ignored `generated` directories so it does not overwrite them.

From the repository root, create an environment and install [requirements.txt](../requirements.txt):

```sh
python -m venv .venv
```

On Windows, activate it with `.venv\Scripts\Activate.ps1`; on macOS or Linux use `source .venv/bin/activate`. Then run:

```sh
python -m pip install -r requirements.txt
```

## PEQ miniature

```sh
python models/peq15/source/build_v4.py
blender --background --factory-startup --python models/peq15/source/blender_v4.py
python models/peq15/source/make_color_3mf.py --input models/peq15/generated/blender
```

Use your Blender executable's full path if it is not on PATH. The scripts produce the solid model, export and render it in Blender, then split the exported geometry into color regions. The generators check mesh structure and reconstruction volumes. Rendering still requires visual inspection.

To regenerate only the colorable models from the published STLs:

```sh
python models/peq15/source/make_color_3mf.py
```

## Logo keychain

```sh
python models/logo-keychain/source/build_maxqr.py
blender --background --factory-startup --python models/logo-keychain/source/render_maxqr.py
```

The builder uses the supplied logo and QR images under `models/logo-keychain/inputs`, reconstructs the meshes, and checks a QR projection from the exported back half. The renderer creates a preview and Blender mesh project with suggested paint colors.

## Verify published downloads

```sh
python scripts/verify_models.py
```

This checks the shipped STL geometry, reads every color-part mesh from the 3MF archives, compares their combined volume with the corresponding PEQ STL, and checks the saved keychain QR projection. It does not operate a printer or certify physical fit or scanning.
