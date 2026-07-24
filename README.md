# HostCaps

**Open Hosting Capability Discovery and Compatibility Matching for NixOS Services**

HostCaps is a small, provider-neutral discovery and verification layer for hosting environments. It lets an operator publish a machine-readable description of what an existing host can actually provide, while service authors publish a separate requirements profile. A deterministic matcher then answers a pre-deployment question:

> Is this host compatible with this service, which requirements passed or failed, and what evidence supports the decision?

HostCaps does not deploy, migrate, schedule or monitor services. It provides reusable capability facts and compatibility evidence that other tools can consume.

## Why this matters

NixOS makes software and configuration reproducible, but portability still fails when the target environment lacks a required database version, storage property, network feature, security control or federation capability. Today these facts are commonly hidden in provider documentation, custom APIs or operator knowledge. HostCaps turns them into a compact open interface.

The v0.1 baseline includes:

- Host Capability Manifest and Service Requirements Profile schemas;
- CLI validation, canonical fingerprinting, privacy redaction and deterministic matching;
- explicit `pass`, `fail`, `warning` and `unknown` outcomes;
- evidence freshness checks and declared/observed provenance;
- example host manifests and four service profiles;
- NixOS module baseline for publishing a public manifest;
- automated tests, CI, security and privacy documentation.

## Quick start

```bash
python -m pip install -e .
hostcaps validate host examples/host-public.json
hostcaps validate profile profiles/forgejo.json
hostcaps match examples/host-public.json profiles/forgejo.json
hostcaps fingerprint examples/host-public.json
hostcaps redact examples/host-private.json examples/public-view-policy.json
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Core concepts

### Host Capability Manifest

A versioned JSON document describing capabilities in categories such as compute, storage, network, runtime, databases, security, federation and operations. Claims can carry evidence metadata including collection method and freshness.

### Service Requirements Profile

A separate JSON document containing required and preferred constraints. This decouples service requirements from any single provider, control plane or marketplace.

### Compatibility report

The matcher returns a deterministic machine-readable report. A required failed rule produces `incompatible`; missing or stale required evidence produces `unknown`; preferred-rule issues produce `compatible_with_warnings`.

### Public and private views

HostCaps supports policy-driven redaction so operators can publish enough information for useful discovery without exposing sensitive host identifiers or topology details.

## Planned discovery endpoint

The reference NixOS module publishes a public manifest at a configurable endpoint. The proposed interoperable path is:

```text
/.well-known/hostcaps
```

Use of the well-known location is a standards-track objective, not a claim that an IANA registration already exists.

## Scope boundaries

HostCaps is not:

- a hosting platform or provider marketplace;
- a deployment or fleet-management control plane;
- a scheduler or migration engine;
- a continuous monitoring product;
- a replacement for TOSCA, NetBox, Kubernetes or NixOS modules.

It is designed as a thin discovery and compatibility layer that those systems can call.

## Licence

Apache License 2.0. Documentation is intended for CC BY 4.0 publication in the funded release.
