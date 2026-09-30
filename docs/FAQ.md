# Maker FAQ

[Project](../readme.md) · [Build guide](BUILD_GUIDE.md) · [Origins](../UPSTREAM.md)

## What is XGO-Duck?

A Microduck-based biped project adapted by Luwu Dynamics for Arduino Uno Q, a custom expansion board and Feetech 1910 servos. It publishes hardware resources, a training environment and an onboard runtime in separate repositories.

## Do I need to train a model before building?

No. The Arduino runtime contains walk, get-up and pick ONNX files. You still need the matching hardware, servo setup and calibration. Start with the bundled set before experimenting with new policies.

## Can I explore without a robot?

Yes. Inspect the build and control code, or use the XGO-Duck training repository on a suitable CUDA machine. No XGO-Duck browser simulator has been validated or published in this package. The [Microduck simulator](https://huggingface.co/spaces/pollen-robotics/microduck-simulator) is an upstream learning reference, not a simulation of the Uno Q variant.

## Is this a ready-to-use product or a kit?

These repositories describe a maker build. A purchasable kit, inventory, retail price and delivery schedule have not been supplied. Contact hello@xgorobot.com for availability questions. The approximately US$400 figure is a build estimate, not a purchase offer.

## How long does assembly take?

There is no validated assembly-time estimate yet. Printing, sourcing, PCB preparation and calibration depend on your equipment and experience. A first independent build should record both working time and blockers.

## Can I use Microduck software or policies unchanged?

Do not assume so. Use the [XGO-Duck runtime contract](https://github.com/LuwuDynamics/xgoduck_runtime_arduino) and the [policy handoff guide](https://github.com/LuwuDynamics/xgoduck_rl). Matching dimensions do not prove matching dynamics or command semantics.

## What does it do today?

The runtime contains walking, get-up and pick control paths. Other training tasks are experiments until they have a matching runtime integration and repeatable hardware evidence. Camera-based behavior, voice, skating and additional upstream behaviors are not established XGO-Duck capabilities in this release.

## Can I change the shell or actuator?

Treat mechanical changes as control changes when they alter mass, inertia, joint limits or foot contact. Recheck fit and calibration; compare the simulation model and evaluate whether retraining is required. A visually similar servo is not necessarily a compatible actuator.

## How can I contribute before owning one?

Check instructions, improve diagrams, identify missing information, review source provenance or reproduce a simulation result. See [Community](../COMMUNITY.md) for concrete contributions and how to report evidence.

## Can I sell a build or use it commercially?

Read [Licensing](../LICENSING.md) for the specific material. Existing Apache-2.0 code rights remain in place; design and model terms require separate review. Contact the team for material needing additional authorization.
