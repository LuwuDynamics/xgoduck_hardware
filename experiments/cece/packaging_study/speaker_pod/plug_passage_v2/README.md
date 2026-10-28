# Cece speaker plug passage V2 — candidate only

This trial updates the **hooded speaker head** and matching pod tray. It leaves the old 4 mm bare-wire versions untouched. The selected [SparkFun COM-21311 speaker](https://www.sparkfun.com/thin-speaker-4-ohm-2-5w-28mm.html) has an approximately 180 mm lead ending in a two-wire JST connector. SparkFun does not identify the connector series or housing dimensions. For scale, a genuine [JST PHR-2 housing](https://www.jst.com/wp-content/uploads/2025/06/ePH.pdf) is 5.8 mm wide and 6.85 mm in the other housing dimension; the actual speaker plug must be measured.

## Files and geometry

- `Cece_head_hood_speaker_plug_passage_V2_CANDIDATE.stl`: replacement hooded head with the rear speaker mounts and enlarged plug passage.
- `speaker_pod_tray_plug_passage_V2_CANDIDATE.stl`: matching replacement rear speaker tray.
- The original `../speaker_retaining_grille.stl` is retained without change.
- `Cece_speaker_plug_passage_V2_CANDIDATE.FCStd`: FreeCAD inspection assembly. `build_and_check.py` regenerates the two STLs and `mesh_validation.json`; `make_freecad.py` regenerates the FCStd file.

The round passage is **Ø12 mm**, centered at X=0, Z=17 and along Y. A small asymmetric side relief makes the feed orientation visible; it is **not** a connector key. An **Ø18 mm outer sleeve** reinforces the passage between the head wall and pod front. The housing still uses two candidate M3×10 head screws and two candidate M2×5 grille screws. The speaker centre and original grille geometry are unchanged.

## Checks and limits

`mesh_validation.json` reimports the two printed STLs and confirms both are watertight, single-component meshes. A straight 8×7×16 mm trial plug envelope clears both printed pieces, with zero solid intersection. The new head and pod have zero solid intersection with each other, the V4 body, heart frame, faceplate, charger tray, original grille, and a Ø28×7 mm speaker envelope.

**The complete installed route is a no-go at the current provisional ESP position.** `module_route_probe.json` finds **224 mm³ overlap** between the straight 8×7×16 mm trial plug and the ESP32-C3 envelope centered at (0,24,10) mm. A straight Ø2 mm wire also intersects that envelope by 25.092 mm³. A right-side turn near the rear wall intersects the printed head. Thus a wider plastic hole alone does not make the speaker plug-and-play. The trial plug size is an assumption; actual plug shoulders, speaker terminals, cable bend, strain relief and the path to the amplifier remain unknown. Relocate the ESP or design a measured side/upper cable corridor, then repeat CAD and physical tests before choosing this head for a full print. A serviceable connector inside an accessible pod is another option after measuring the supplied speaker plug.

The source hooded head also has a separate provisional PiicoDev cable hood at its top; its connector and service route remain unverified. Neither candidate is a final Cece print release.
