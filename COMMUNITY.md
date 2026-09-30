# Build, document and contribute

[Project](readme.md) · [Contributing](CONTRIBUTING.md) · [Roadmap](ROADMAP.md)

A useful contribution helps another person reproduce a result. You do not need a complete robot to start.

## Choose a first contribution

| What you can offer | A useful contribution | Where to send it |
| --- | --- | --- |
| A fresh reader's perspective | Identify the exact step that assumes missing knowledge | [Documentation issue](https://github.com/LuwuDynamics/xgoduck_hardware/issues/new?template=documentation.md) |
| A printer and measuring tools | Record fit, material and orientation for one named part | [Build report](https://github.com/LuwuDynamics/xgoduck_hardware/issues/new?template=build_report.md) |
| An assembled robot | Reproduce setup with revisions, calibration procedure and status capture | [Runtime issue](https://github.com/LuwuDynamics/xgoduck_runtime_arduino/issues) |
| A CUDA workstation | Reproduce one task and record checkpoint/export results | [Training issue](https://github.com/LuwuDynamics/xgoduck_rl/issues) |
| Experience with model transfer | Share an ONNX artifact, model card and bounded evaluation | [Policy report](https://github.com/LuwuDynamics/xgoduck_rl/issues/new?template=policy_report.md) |

Templates in this documentation package become available after the corresponding repository changes are merged. Use a regular issue if a template has not reached the live repository yet.

## Share a build people can repeat

Include one clear photo, the hardware/runtime revisions, servo identity, battery specification, print settings, calibration method and a short account of the first successful test. Include failures and fixes. An edited highlight clip can illustrate the result, but a continuous real-time clip with the test conditions is better evidence.

## Share a policy people can evaluate

Provide a model card, source and artifact hashes, exact task, observation/action semantics and hardware compatibility. Separate simulation-only results from real-robot results. Publish only material you have rights to redistribute. A submission is not an official compatibility endorsement.

## Help maintain useful issues

Search existing reports, keep each report focused and include the smallest reproduction. Redact credentials and personal information. Maintainers can ask for missing evidence, link duplicates and summarize verified fixes back into the documentation.

There is no dedicated XGO-Duck community-server link in this release. GitHub issues are the public entry point; hello@xgorobot.com handles private and commercial enquiries. Do not direct XGO-Duck support requests to upstream maintainers unless the issue has been isolated to their project.
