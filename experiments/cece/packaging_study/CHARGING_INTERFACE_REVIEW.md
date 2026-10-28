# Cece 2S charging interface: connector audit

**Status: the rear UC2 cassette is a size and mounting study, not a validated charging port.** A first sideways layout blocked both ports. The current candidate rotates the charger's long axis rearward so its XH end faces the body duct and its USB-C end faces a rear window. This corrects the port *direction*, but the exact connector mouths, mating plugs, cable bends and electrical isolation have not been modeled or tested. Do not treat `charger_cassette/*.stl` as charge-ready.

## What must connect

```text
Dualsky 2S pack MAIN 2-wire JST discharge lead
    -> mating connector, correctly polarized
    -> accessible power switch in the pack-positive lead
    -> suitably rated protection / low-voltage strategy (not designed yet)
    -> Hobbywing UBEC input -> regulated 5 V robot rail

Dualsky 2S pack 3-wire balance lead (likely JST-XH; verify delivered pack)
    -> ISDT UC2 2S XH balance socket
USB-C 5 V supply -> UC2 USB-C input
```

The UC2 is a balance-port charger: ISDT specifies USB-C **5 V / 2 A input**, XH 2.54 battery connection, **0.8 A charge current**, and a 39.6 × 19.8 × 9.5 mm, 6 g body. It does not document a robot power-path or an automatic load-isolation function. Thus switch the robot **off** and isolate the main discharge load while charging; do not feed USB into the ESP32 or PiicoDev USB port as a substitute for a 2S LiPo charger. [ISDT UC2 product specification](https://www.isdt.co/uc2-2.html?lang=en).

The ordered Supercheap battery is model **DSBXP05502ULT**, 2S 550 mAh, 52 × 31 × 12 mm, 35 g, with a two-wire `JST` discharge lead. That seller does **not** identify the separate balance connector. A listing for the same Dualsky pack identifies a JST-BEC main connector and 2S XH balance lead; use this as an expectation, then check the delivered battery's three-wire plug and polarity before buying or cutting mating connectors. [Supercheap pack listing](https://www.supercheaphobbies.com.au/store/550mah-dualsky-lipo-battery-with-connector-p-51186.html); [same-model FlashRC listing](https://www.flashrc.com/fr/batteries-de-propulsion-avions-rc/23056-batterie-dualsky-ultra-lipo-2s-74v-550mah-50c-prise-jst-bec-6941047105294.html).

The UBEC itself has output overcurrent, short-circuit and overheat protections; these do **not** establish per-cell LiPo discharge cutoff. Hobbywing explicitly warns that leaving its battery connected after use can completely discharge it. A pack-positive switch and a deliberate low-voltage/disconnect strategy are still needed. [Hobbywing UBEC 5A manual](https://oss.hobbywing.com/pdf/pdfen/UBEC5A.pdf).

## Present CAD geometry and remaining connector risks

| Feature | Current candidate geometry | Consequence |
| --- | --- | --- |
| Charger envelope | X −9.9…+9.9, Y 43.5…83.1, Z −28.75…−19.25 mm | Long axis is now Y. Manufacturer photos show USB-C and XH ports on the two **opposite ends of that axis**; the candidate assumes XH faces the body and USB-C faces rear. [ISDT product image](https://www.isdt.co/wp-content/uploads/2023/11/UC2-2.png). |
| Tray cavity | X −11.9…+11.9, Y 41.5…85.1, Z −30.75…−17.25 mm | Nominally 2 mm about the rectangular charger envelope. The cavity alone does not prove room for either mating connector. |
| Body and tray lead passage | X −7…+7, Z −30…−18 mm, through the body and cassette front wall | The 14 × 12 mm duct points directly toward the assumed XH end. Boolean checks pass a 13 × 11 × 11.9 mm probe with zero solid overlap, but actual XH socket offset, plug insertion depth, installed bend and strain relief remain unknown. The charger front is at Y 43.5, 2 mm behind the tray front cavity edge. |
| USB-C rear access | 16 × 7.5 mm bezel opening at Y 85.1…87.1; charger rear at Y 83.1 | CAD confirms an unobstructed rectangular probe through the rear opening. It does **not** confirm the UC2 USB-C receptacle location or clearance for the chosen molded cable plug. This window must be aligned to the measured unit. |
| Power switch | No switch opening, retained switch, connector adapter, fuse or low-voltage device in this CAD | Robot-off charging is not yet physically or electrically provided. |

Geometry comes from [`charger_cassette/build_freecad.py`](charger_cassette/build_freecad.py), [`charger_cassette/validate_meshes.py`](charger_cassette/validate_meshes.py), and [`charger_cassette/mesh_validation.json`](charger_cassette/mesh_validation.json) at this review. JST's XH drawing gives a 7.75 mm nominal housing depth for the XH plug family, considerably more than the 2 mm axial gap at the charger's front face. The new duct can potentially accommodate its straight insertion, but only if the UC2 socket center lies inside that opening and the actual lead reaches without a damaging bend. [JST XH drawing](https://cdn-shop.adafruit.com/product-files/4876/JST%20XH%20ds.pdf). The actual UC2 socket offsets, plug insertion length and cable bend envelope are not published as a dimensioned UC2 drawing, so **no minimum safe mating clearance can yet be certified**. The former X-axis tray, with solid walls just 2 mm from both ports, remains a documented no-go and must not be printed from old STL copies.

## Required design changes before a charging prototype

1. Obtain and measure the UC2 and delivered Dualsky pack. Confirm the UC2 2S socket side, main JST mating type, XH polarity, protruding plugs, cable length and minimum bend with plugs fully seated. Do not infer pin order from wire color alone.
2. Validate the corrected Y-axis cassette against the real UC2: position the 3D envelopes of the **mated XH plug and USB-C cable plug** and their strain reliefs, align the 14 × 12 mm front duct and 16 × 7.5 mm rear opening to the actual socket centers, then enlarge/relocate openings if needed. Check that the XH plug can be inserted or disconnected during service without removing/straining the soft pack. The longer rear pod changes center of mass; re-run balance with it and the actual cables.
3. Add an accessible, retained switch in the battery main-positive path ahead of the UBEC and a matching pack connector/harness. Verify switch and wire current ratings against the complete robot, and specify a 2S low-voltage cutoff during use plus a battery disconnect for storage/service. Firmware warning or servo shutdown alone does not disconnect the UBEC. Keep balance charging wiring separate from the switched 5 V rail.
4. Add edge protection and strain relief at the 14 × 12 mm body duct and cassette entry; route leads away from servo motion and screws. Check that the lid can open for battery/charger disconnection and that no soft-pack cell is compressed by fasteners.
5. Re-run full CAD connector mating and clearance, then perform a physical unpowered plug/fit check and a supervised charging test with the robot off before accepting the assembly.

The published UC2 envelope, oriented cassette and open probe paths prove **candidate packaging geometry only**. They do not prove connector mating, electrical safety, thermal behavior, serviceability or balance.
