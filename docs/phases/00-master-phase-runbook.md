# Industrial Edge AI Platform — Master Phase-by-Phase Implementation Runbook

## Non-negotiable phase rule

Every phase follows exactly this lifecycle:

1. Create/change only the files and resources belonging to the phase.
2. Test locally on the Mac.
3. Validate the target system (Azure Portal / CLI / Databricks / Kubernetes).
4. Capture evidence in `docs/evidence/PHASE-XX.md`.
5. Run `git diff --check` and phase-specific tests.
6. Commit on a feature branch.
7. Push the feature branch to GitHub.
8. Open a Pull Request.
9. GitHub CI/plan must pass.
10. Review and merge.
11. For infrastructure, run the controlled apply workflow and validate again.
12. Tag/record the phase as complete before starting the next phase.

**Never start the next phase because files merely exist. A phase is complete only when its acceptance criteria pass.**

## Environments

- `dev`: build and integration proving ground.
- `stage`: production-like validation; created after dev is stable.
- `prod`: controlled promotion; no experiments.

## Jetson-free testing strategy

You do not need an NVIDIA Jetson to complete most of this project.

1. Mac + CSV sensor simulator tests the sensor contract and FastAPI service.
2. Docker Desktop tests the exact container boundary used at the edge.
3. IoT Hub simulator tests device-to-cloud telemetry.
4. An Azure Ubuntu VM acts as a **virtual IoT Edge device** and runs the IoT Edge runtime/modules.
5. AKS tests the cloud inference deployment.
6. ONNX Runtime CPU validates the portable model artifact.
7. A physical Jetson is an optional final hardware-validation phase; it changes execution provider/performance constraints, not the core application contract.

Microsoft's IoT Edge quickstart explicitly uses an Azure Linux VM as a virtual IoT Edge device, and IoT Edge supports Linux x64 and ARM64 modules. This makes the VM path a legitimate pre-hardware integration environment.

## Phase map

| Phase | Scope | Main outcome | Gate before moving on |
|---|---|---|---|
| 01 | Repo baseline | Reproducible local project | CI green on first PR |
| 02 | Terraform bootstrap | Azure Blob remote state | remote state + `plan` no-change |
| 03 | GitHub OIDC | Secretless Azure CI identity | PR OIDC login succeeds |
| 04 | Azure foundation | RG/VNet/KV/Logs/ACR | Terraform no-change + portal check |
| 05 | IoT/data | ADLS + IoT Hub + Event Hubs | simulated device event reaches Event Hubs |
| 06 | FastAPI simulator | local inference service | tests + CSV replay pass |
| 07 | Container/ACR | immutable application artifact | pushed SHA image runs successfully |
| 08 | Databricks | UC + streaming + governed layers | telemetry visible in validated Delta table |
| 09 | ML/ONNX | model lifecycle | approved ONNX artifact runs in FastAPI |
| 10 | AKS | cloud inference runtime | rollout + health + metrics pass |
| 11 | Virtual IoT Edge | edge deployment without Jetson | module healthy on Azure Linux VM |
| 12 | Observability/SRE | SLIs/SLOs/alerts | alert and dashboard validation |
| 13 | Security hardening | private/least privilege | security checklist passes |
| 14 | Stage/prod | promotion lifecycle | stage soak + approved prod release |

Read the individual phase guides in numerical order.
