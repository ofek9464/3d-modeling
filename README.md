# 3D modeling and printing

Printable models, editable Blender projects, build scripts, and the skills and MCP setup used to make them.

| Model | Download | Status |
| --- | --- | --- |
| [PEQ-15 cosmetic miniature](models/peq15/) | [Colorable 3MF](models/peq15/3mf/PEQ15_colorable_7p4mm.3mf) · [STL](models/peq15/stl/peq15_channel_7p4mm.stl) · [Blender](models/peq15/blender/peq15_v4.blend) | Revision 4; 21 color parts; rail fit untested |
| [Book and stethoscope QR keychain](models/logo-keychain/) | [Complete STL](models/logo-keychain/stl/keychain_complete.stl) · [Front half](models/logo-keychain/stl/keychain_front_glue_half.stl) · [QR half](models/logo-keychain/stl/keychain_qr_glue_half.stl) | Latest enlarged-QR revision; digital QR check passed; physical scan untested |
| [Paw can opener](models/paw-can-opener/) | Original creator link and investigation notes | Model files excluded because the creator prohibits re-uploading |

<img src="models/peq15/previews/color-preview.png" alt="PEQ-15 miniature with suggested colors" width="430">
<img src="models/logo-keychain/previews/preview.png" alt="Book-shaped keychain, front and QR back" width="650">

## Print a model

Download the file through GitHub's **Download raw file** button, or clone this repository. Open it in your slicer at 100% scale with millimeter units. The intended printer is a Bambu Lab X2D; the files here contain geometry, not a verified X2D print profile or G-code.

- **3MF** stores the PEQ assembly and named color regions. Keep the parts assembled and assign filaments in the slicer's Objects list. Suggested display colors may need to be mapped to your actual filaments.
- **STL** stores geometry. The keychain previews show suggested paint colors, which are not encoded in its STLs.
- **BLEND** opens the editable mesh project in Blender.

Read each model's print notes. For the PEQ, print a [rail-fit sample](models/peq15/fit-tests/) before the full miniature. For the keychain, scan the finished QR after printing and painting.

## Modeling tools

- [Blender skill bundle](skills/): the installed `create-3d-model` skill, including its reference-modeling, rendering, and export modules.
- [BlenderMCP setup](mcp/): the tested server version and a portable Codex configuration example.
- [Rebuild instructions](docs/REBUILD.md): Python dependencies and commands for the model generators.
- [Source and licensing notes](THIRD_PARTY_NOTICES.md): provenance for the skill, software, and model references.

The generated meshes were checked for closed geometry. These checks do not establish physical fit, strength, or successful printing. See the per-model validation files for what was measured.
