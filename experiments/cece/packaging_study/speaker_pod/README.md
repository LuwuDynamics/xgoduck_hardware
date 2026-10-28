# Cece external rear head speaker pod — candidate

This candidate moves a nominal 28 mm diameter, 7 mm thick speaker to the **outside of the rear head wall**. It resolves the solid overlap found between a low internal speaker and the UBEC in the current packaging study. The speaker centre is **X = 0, Y = 44.7, Z = 17.0 mm** in Cece's assembled coordinates, with its axis along Y. The speaker dimensions are an allowance, not an exact model of the purchased item. Check the real speaker's rim, terminals and wires before printing a final assembly.

## Printable files

- `cece_head_with_speaker_mount_CANDIDATE.stl`: complete replacement for `Cece_Head_Centered_Antenna_DRAFT.stl`, with two rear mounting posts and a 4 mm wire passage. The old head file is untouched.
- `speaker_pod_tray.stl`: Ø34.5 mm outside speaker housing, X = ±31 mm including screw rails, Y = 37.2–50.2 mm.
- `speaker_retaining_grille.stl`: removable sound grille, rear face Y = 52.2 mm. Twenty-one Ø3.1 mm sound holes are provided.

`Cece_rear_speaker_pod_candidate.FCStd` is the FreeCAD model with the source head as reference, the candidate head mesh, editable pod/grille mounting solids and a 28 × 7 mm speaker envelope. Run `build_freecad.py` with the FreeCAD 1.1 Python runtime, then `validate_meshes.py` with the workspace Python and mesh dependencies to rebuild exports/checks. The replacement head STL is produced by `validate_meshes.py`; rerun `build_freecad.py` once after validation to refresh the candidate mesh in the FreeCAD project.

## Assembly and fasteners

The head has posts centred at X = ±23, Z = 17 mm, each with a blind Ø2.5 mm pilot. Two **M3 × 10 screws** enter from recessed access bores at the back of the open pod and fasten it to these posts. The printed grille sits at the back, retaining the speaker by its rim, and takes two **M2 × 5 screws** at X = ±28 into separate Ø1.8 mm pilot holes in the pod rails. Fastener lengths and printed pilot sizes are design assumptions; test them on a small printed sample. Install the pod screws before the grille. The grille can then be removed without taking the pod off the head.

Feed bare speaker wires through the aligned 4 mm passage in the modified head and pod front. The head's printed sleeve surrounds the wires across the 5 mm gap to the pod. A preattached plug has not been checked to pass through this opening. The speaker sits between printed front and rear rim supports with a **nominal 7 mm axial space**. A thinner speaker needs a compressible shim; a thicker speaker needs a revised seating depth. The Ø30.5 mm cavity gives 1.25 mm radial room around a Ø28 mm speaker.

## Geometry checks and limits

`mesh_validation.json` records exact mesh Boolean checks. The replacement head, pod and grille each export as one watertight solid. The pod has zero solid overlap with the replacement head, V3 body and charger cassette, rear `cece` name, faceplate, cleaned feet and an approximate assembled antenna location. The 28 × 7 mm speaker envelope has zero solid overlap with the pod or grille. Narrow probes pass through both mounting screw paths, grille screw paths and the wire passage without solid overlap. The original head and added posts have 502.77 mm³ intentional fusion overlap.

The speaker centre extends the robot rearward and upward; mass and dynamic balance must be recalculated with the actual speaker and printed infill. Screw holding strength, cable strain, actual terminals, electrical connector fit, heat and audio quality have not been tested. Do not infer speaker performance from the grille's hole area alone.
