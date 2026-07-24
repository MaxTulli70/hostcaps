# Threat model baseline

HostCaps publishes operational facts, so its main risks are false claims, stale claims, unnecessary disclosure and unsafe collection.

## Threats

- a compromised host publishes fabricated capabilities;
- an operator accidentally exposes topology or contact information;
- stale evidence is treated as current;
- a collector executes an unsafe probe or leaks command output;
- a consumer treats a self-declared claim as independently verified;
- a public endpoint becomes a high-value inventory source for attackers;
- a matcher silently coerces units or versions and reports a false pass.

## Baseline controls

- evidence method and collection time are explicit;
- stale required evidence produces `unknown`, not `pass`;
- public/private views are generated through a deny-capable redaction policy;
- the v0.1 collector is not implemented as arbitrary shell execution;
- matching is deterministic and rule-level results are visible;
- signatures, when added, will use established external tools;
- capability granularity should be the minimum needed for matching.

The funded review will analyse trust anchors, replay, endpoint enumeration, extension safety and signature profiles.
