# Cece battery, UBEC and USB-C charging construction draft

**Not a finished wiring schematic or charge-ready assembly.** This records the selected battery and UBEC, a candidate charger, the minimum connections, and the parts still needed. The [mechanical charging review](CHARGING_INTERFACE_REVIEW.md) separately identifies cassette connector-fit gaps.

## Confirmed order and candidate charger

| Item | Evidence | Electrical and physical facts |
| --- | --- | --- |
| **Ordered:** Dualsky `DSBXP05502ULT` | [Supercheap Hobbies product listing](https://www.supercheaphobbies.com.au/store/550mah-dualsky-lipo-battery-with-connector-p-51186.html) | 2S LiPo, 7.4 V nominal, 550 mAh, 52 × 31 × 12 mm, 35 g, 20 AWG main leads terminated in a connector called only `JST`; advertised maximum charge current 3 A. The exact main-connector series, mating gender, polarity, and presence/length of a balance lead must be checked on the delivered unit. |
| **Ordered:** Hobbywing `UBEC-5A-V2-Air` (`HW30607000`) | [Supercheap listing](https://www.supercheaphobbies.com.au/store/hobbywing-ubec-p-62554.html), [Hobbywing product specification](https://www.hobbywingdirect.com/products/ubec-5a-air), [Hobbywing manual](https://oss.hobbywing.com/pdf/pdfen/UBEC5A.pdf) | 2–8S LiPo input; selectable 5.0/6.0/7.4 V output; 5 A continuous, 15 A short peak; 50 × 17 × 10 mm, 21 g. The manual specifies **no jumper for 5.0 V**. This is a regulator, not a charger or per-cell low-voltage cutoff. Verify actual 5.0 V output with a meter before connecting Cece. |
| **Candidate, not ordered:** ISDT `UC2` | [ISDT product specification](https://www.isdt.co/uc2-2.html?lang=en), [port photograph](https://www.isdt.co/wp-content/uploads/2023/11/UC2-2.png) | USB-C input at 5 V/2 A; 1S/2S LiPo balance charging through XH 2.54 port at fixed 0.8 A; 39.6 × 19.8 × 9.5 mm, 6 g. The 0.8 A setting is below the pack seller's 3 A maximum, but the UC2 plug must match the real three-wire 2S balance connector and polarity. Charger mounting and external USB plug access remain candidate geometry only. |

A [same-model Dualsky listing](https://www.flashrc.com/fr/batteries-de-propulsion-avions-rc/23056-batterie-dualsky-ultra-lipo-2s-74v-550mah-50c-prise-jst-bec-6941047105294.html) explicitly calls the main discharge plug **JST-BEC** and the separate balance plug **JST-XH**. Its barcode `6941047105294` matches the [Australian Metro Hobbies listing for `DSBXP05502ULT`](https://www.metrohobbies.com.au/products/dualsky-dsbxp05502ult-550mah-2s-7-4v-50c-lipo-battery-with-jst-connector). However, the [actual Supercheap order page](https://www.supercheaphobbies.com.au/store/550mah-dualsky-lipo-battery-with-connector-p-51186.html) does not specify the balance plug or even the main `JST` series, so the delivered unit is still **unverified**. Do not buy the UC2 or a mating power harness solely on this other seller's description; inspect the battery first. JST's [XH drawing](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf) identifies a 3-position XHP-3 housing, nominally 9.8 mm overall width and 7.75 mm deep; the pack's actual connector and wire exit still need measuring.

## Minimum circuit, with robot OFF for charging

```text
BATTERY MAIN POSITIVE -- mating pack plug -- protection/fuse TBD --
    accessible DC-rated ON/OFF switch -- Hobbywing UBEC input positive
BATTERY MAIN NEGATIVE -- mating pack plug --------------- UBEC input negative

Hobbywing UBEC output: measured +5 V and GND -> Cece 5 V distribution;
    all powered modules share signal ground; exact ESP32/servo-driver
    power-entry and USB backfeed isolation remain separate checks.

BATTERY THREE-WIRE 2S BALANCE LEAD -> UC2 2S XH balance port
EXTERNAL 5 V / 2 A USB-C source -> UC2 USB-C port at rear of robot
```

The balance lead stays **upstream of the main switch**, directly on the pack. Set the main switch OFF before connecting USB-C for charging, and ensure no other USB cable or external 5 V feed can power the robot during this test. The UC2 documentation describes balance-port charging, not a load-sharing power path; it must not be treated as one. Do not wire USB 5 V straight to the 2S pack, the UBEC output, or the ESP32/PiicoDev USB socket as a charging shortcut. Hobbywing warns to disconnect its UBEC from the battery after use because leaving it connected can completely discharge the pack. For storage/service, unplug the main battery connector; a 2S low-voltage cutoff/protection approach during operation is still to be selected. [ISDT](https://www.isdt.co/uc2-2.html?lang=en); [Hobbywing manual](https://oss.hobbywing.com/pdf/pdfen/UBEC5A.pdf).

The proposed cassette assumes the battery's balance lead can remain plugged into the UC2 during robot use. The UC2's unpowered balance-port standby draw and suitability for permanent connection have **not** been established from the available specification. Measure that draw and check the charger's instructions with the actual pack. Until then, unplug the balance lead for storage, and do not treat the cassette as a sealed, maintenance-free charging system.

## Main-connector current is a conditional design blocker

If the delivered pack's `JST-BEC` plug is a genuine **JST RCY**, JST rates it at **3 A per circuit with AWG22**; the family is a free-hanging wire-to-wire connector, with a mated body about 23.3 mm long and 4.0 mm high. [JST RCY product profile](https://www.jst-mfg.com/product/index.php?lang=2&series=521); [JST RCY drawing](https://www.jst-mfg.com/product/pdf/eng/eRCY.pdf). The UBEC can deliver 5 A at 5 V (25 W). At 7.4 V nominal, that would require **at least 3.38 A at the battery even with impossible 100% efficiency**, or about 3.75 A at 90% efficiency. Therefore **the pack connector could be the limiting component**; the UBEC's 5 A label is not proof that the full robot can continuously draw 5 A through a 3 A RCY plug. The actual 4-servo peak and running currents have not been measured. Do not solve this by merely adding an RCY adapter or a higher-rated switch; the original contact remains in series. Identify the delivered connector and measure the operating/stall current before setting a permitted load or choosing a higher-current connector/battery solution.

## Items still to source or verify

| Quantity | Item / decision | Why it is still open |
| ---: | --- | --- |
| 1 | ISDT UC2 or another **specified 2S LiPo balance charger** | UC2 is only a candidate, not confirmed purchased. **Defer this purchase** until the delivered pack's 3-position balance lead, connector key/polarity and main switch/power connector plan are confirmed. |
| 1 | Mating **two-position pack discharge connector/harness** | Confirm JST series, gender and polarity on the delivered pack first. If it is RCY, confirm current budget against its 3 A rating before freezing this harness. Use pre-crimped matching leads or proper crimp tooling. |
| 1 | DC-rated, retained **main ON/OFF switch**, in pack-positive path | No selected switch or shell hole exists. A *candidate* robust, non-SMD option is Cole Hersee `5570`, SPST 10 A at 12 V DC, panel mount, two wire leads, Ø11.9 mm panel hole; the manufacturer allows panels up to 7.2 mm. This is **not** fit-checked in Cece and may be too bulky. [Littelfuse/Cole Hersee catalog](https://www.littelfuse.com/assetdocs/passenger-commercial-vehicle-aftermarket-products-catalog?assetguid=4b565fce-3f7e-4c34-95ce-d1f2a4f88d84); [DigiKey part](https://www.digikey.com.au/en/products/detail/littelfuse-commercial-vehicle-products/5570/6347384). |
| 1 | **2S low-voltage cutoff/protection and input fuse strategy**, sized after load measurements | UBEC protection is on its output and does not establish per-cell cutoff or safe pack wiring. Do not lock a fuse value or BMS before normal/inrush/stall current and pack connector are known. |
| 1 | USB-C **5 V/2 A source and cable** for the UC2 | Source specification is from ISDT. Molded plug dimensions must be modeled at the rear bezel before ordering a final panel arrangement. |
| As needed | Insulated wire joints, heat-shrink, strain relief, grommet/edge liner, and 5 V distribution on the through-hole/perfboard build | Routing, wire gauge and connector mating depend on delivered hardware and measured current. The 14 × 12 mm balance-lead duct is a CAD opening only. |

There is **no selected through-hole PCB switch**. A panel-mounted, wire-lead DC switch is mechanically easier to operate and replace in a perfboard prototype; its hole, rear body and lead-bend clearance must be included in CAD before purchase. The RCY discharge connection, if confirmed, is **wire-to-wire**, so a PCB footprint is not needed for that plug. [JST RCY profile](https://www.jst-mfg.com/product/index.php?lang=2&series=521).

## Required acceptance checks

1. Photograph/measure the delivered battery's main and balance plugs; confirm series, polarity and cells with a multimeter before mating anything. Confirm the pack permits the candidate UC2's 0.8 A charge rate from its label/vendor specification.
2. Measure the candidate switch, UC2, XH plug, USB-C cable grip and wire bends in the assembled body. The [current cassette](charger_cassette/README.md) has a rear-facing USB window and balance-lead duct but **no exact mating connector or strain-relief fit result**.
3. With battery absent, check switch continuity and polarity. With current-limited test power, verify UBEC 5.0 V setting and absence of backfeed to the pack/USB ports. Measure 5 V sag and battery current under the four servos' actual operation and brief controlled peak-load conditions before accepting connector, wire, switch or fuse ratings.
4. Charge only with the robot switched off and no other USB power connected; check cell voltages through the balance connector and verify the UC2 terminates correctly on the actual pack. This powered test is outstanding.

This is a construction **draft**. Electrical pinout, connector current capacity, low-voltage cutoff, physical fit and charging behavior must be verified before calling the system complete.
