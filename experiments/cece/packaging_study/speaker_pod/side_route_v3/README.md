# Cece right-side speaker route and screwed faceplate V3 — assembly candidate

These files derive from the **preferred V2 PiicoDev cable-hood head** at `../../servo_plug_check/Cece_head_vertical_driver_hood_V2_CANDIDATE.stl`. They combine a right-side speaker lead opening with two front faceplate screw bosses in **one head STL**. They do not replace the source hood or earlier speaker files.

## Files

- `Cece_head_V2_hood_side_speaker_face_boss_V3_CANDIDATE.stl` — combined head with V2 driver roof hood, rear speaker posts, side speaker passage and front faceplate screw bosses.
- `Cece_faceplate_M2_retained_V3_CANDIDATE.stl` — replacement flat faceplate with two screw holes and shallow recesses.
- `speaker_pod_side_wire_notch_V3_CANDIDATE.stl` — rear pod with an open upper-right bare-wire exit and reinforced two-hole cable-tie lug.
- Existing `../speaker_retaining_grille.stl` remains the grille.
- `Cece_Side_Speaker_Faceplate_V3_CANDIDATE.FCStd` displays these printed meshes and trial speaker/plug envelopes in FreeCAD. `build_and_check.py`, `mesh_validation.json`, `check_exact_driver.py` and `exact_driver_check.json` are the reproducible geometry checks.

## Mechanical scheme

The speaker's supplied lead has a preattached **unspecified two-wire JST plug**. The V3 side passage is Ø12 mm at **X=+28,Z=+26 mm**, through the rear head along Y. A fused Ø18 mm sleeve surrounds it. The minimum nominal web from this bore to the nearby M3 speaker-post pilot at X=+23,Z=+17 mm is **3.046 mm**. An assumed **8×7×16 mm** straight plug clears the printed head and pod. It clears the provisional ESP envelope at (0,24,10), unlike the rejected central-passage V2. With the source V2 hood, an Ø2 mm straight cable envelope from (28,24,26) to (28,6.5,26) has zero solid clash with the head, provisional ESP, gross driver box and amp box. This gets the lead close to the rear/right boundary of the amp envelope. The **actual connector location and bend into it remain unknown**.

Feed the speaker's plug through the side head opening **before fitting the pod**, place the speaker in the pod, then lay its bare lead through the pod's open upper-right notch. A small external lug on the right rail has two Ø2.4 mm vertical holes at X=31,Y=39.7/44.3 mm for one narrow cable tie. This is a candidate restraint; verify lead diameter, bend radius and that neither the tie nor the exposed loop snags. The existing pod-to-head M3×10 and grille M2×5 screw candidates remain. The side wire exit does not carry the plug through the pod, so assembly order matters.

The faceplate is retained by two **trial M2×6** screws at X=±25.5,Z=11 mm. The faceplate has Ø2.3 mm through holes and Ø4×1 mm **counterbores**; the combined head has fused Ø6 mm bosses with blind Ø1.8 mm pilots. The prior supposed ultrasonic eye locator rings were erased by their larger through-hole cut, so these new screws provide the first modeled positive faceplate attachment. Screw length, head size, pilot grip and pull-out must be tested in printed PLA. The HC-SR04 PCB and LEDs still need independent retainers.

## Check results and no-go items

The three V3 STLs reimport as watertight single solids. `mesh_validation.json` reports zero nominal solid overlap among the replacement printed parts, V4 body, V3 heart frame, antenna, charger tray, grille, 28×7 mm speaker cylinder and present provisional module boxes except a **6.511 mm³ gross PiicoDev bounding-box overlap**. That same bounding-box overlap exists in the source V2 hood; V3 does not create it. The detailed manufacturer partial PiicoDev STEP at its selected forward/vertical placement has **zero head overlap** in `exact_driver_check.json`; it omits its USB-C and JST-SH connector bodies, so the real connector route is unproven. The modeled speaker plug/straight wire, faceplate screw cores, speaker mount screw cores and tie-hole probes clear their printed passages. All results are static neutral-pose geometry.

**Do not call this plug-and-play or final print-ready.** SparkFun and Core identify the preattached speaker plug only as “JST”; its actual size and mating amplifier connector must be measured. A cable-tie lug is not proof of strain relief. The lead must route to the actual amplifier socket without a sharp bend or pinching after all other electronics are installed. The head-to-body snap, heart-frame/OLED mount, ultrasonic/LED mounting and hip/ankle physical joints remain open; see `../../ASSEMBLY_JOINT_AUDIT.md`.
