# Cece balance study: actual sole geometry, incomplete full payload

For the later provisional calculation that includes the purchased battery,
UBEC and four SG90 masses at candidate positions, see `INTERIM_STATIC.md` and
run `interim_static.py`. That scenario has a **known battery/hip-servo collision**
and is not a physically verified robot layout.

`INTERIM_STATIC.md` also records a rotated battery/UBEC alternative and a
third V3 body plus rear charger-cassette scenario with widened feet. The third
scenario includes an *unpurchased* 6 g charger input and remains an
incomplete static calculation, not a fitted or walking robot.

For the latest V4 OLED-header-route body, current rear charger cassette,
speaker pod, servo-driver service hood and wider feet, run `latest_balance.py` and read
`LATEST_BALANCE.md`. It compares solid PLA geometry with a stated nominal 20%
infill skin model, and separates unknown speaker/board masses from confirmed
part masses. These are neutral static support checks, not walking validation.

Run `python experiments/cece/balance_study/balance_study.py` from the repository root. It uses only Python 3 standard library and writes `balance_results.json`. The script reads the current Adafruit concept body/head/decorative STL files, the new ankle V2 feet/legs/washers, and the assembly translations in `design/analyze_geometry.py`. It calculates STL tetrahedron volume and centroid and uses the *bottom vertices* of both printed feet to form the actual theoretical contact polygons.

## Results that do not depend on guessing electronic parts

The right flat sole covers x = 15..57 mm, y = -32..32 mm with 5 mm corner chamfers. The left sole is its mirror x = -57..-15 mm. Both feet together have a 31.69 mm minimum edge distance for the **shell-only** nominal centre of mass. The same shell-only centre of mass is **outside** either individual planted foot by roughly 15 mm. A quasi-static step therefore needs a lateral centre-of-mass shift of at least 15 mm just to reach the inner edge, and about 20 mm for the explicitly chosen 5 mm reserve.

At an assumed 1.24 g/cm³ and **100%-solid** geometric volume, the assembled printed shell is 129.75 g, with centre at (0.219, -0.311, -36.228) mm in CAD coordinates and height 52.79 mm above the sole plane. These are not sliced filament mass or measured weights. Shifting the whole shell's projected centre sideways by 20 mm solely through rigid tilt would take about 21° at that height; the actual jointed robot may shift its centre differently. With a 5 mm one-foot margin and this height, an outward lateral acceleration of about 0.93 m/s² would consume the margin in the simplified zero-angular-momentum model. The real hardware may move the centre height and change this value.

The four purchased SG90s have a published 9 g mass each (36 g total), but the selected four motor centres, battery, charger, UBEC, electronics, wiring, screws and actual print masses are not all established. `measured_inputs.json` records missing values as `null`. Accordingly `balance_results.json` explicitly marks the **full robot unverified** rather than producing a false final mass, full centre of mass or payload limit. Adding a battery in the middle may lower the centre height, but it does not by itself move a symmetric robot's centre above a single planted foot. Mass alone does not change a static support polygon; motor torque, shaft/print strength, dynamic acceleration and floor friction determine tolerable moving weight.

## What completes the calculation

Fill `printed_part_masses_g` with weighed printed parts. For every hardware entry, provide a real mass and a mounted centre in the FreeCAD model's XYZ millimetres. Include the exact battery and charger, not a generic box. Re-run the script. It then reports static margins and a simple acceleration bound for the one fixed neutral pose. Each printed part's centre is still approximated by the STL solid-volume centroid; actual perimeter and infill distribution may move it. For a walking sign-off, repeat the calculation over the **actual gait poses** with transformed part centres and active foot contacts, then check ground reaction forces, friction, SG90 running torque/current, servo voltage sag and foot slip under a physical load test. The previous MuJoCo GIF uses proxy contacts and assumed masses and cannot establish those facts.

The sole convex hull represents a perfectly flat floor and ideal contact across the printed foot. Actual print warp or floor unevenness can reduce the support area. The 5 mm reserve is a declared design criterion for comparison, not a measured safety factor.

Sources: Rapid Robotics SG90 product page https://rapidroboticsaustralia.com.au/products/sg90-micro-servo ; assembled part transforms in `../design/analyze_geometry.py` ; STL shapes in `../parts_adafruit_draft/` and `../ankle_v2/`.
