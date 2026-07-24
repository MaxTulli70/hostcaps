# RFC-0001: Host Capability Manifest and Compatibility Matching

Status: public review draft  
Date: 24 July 2026  
Project: HostCaps  
Licence: Apache-2.0

## Summary

HostCaps proposes a provider-neutral way for an existing host to publish machine-readable capabilities and for a service to publish independent requirements. A deterministic matcher then produces a rule-level compatibility report before deployment or migration.

HostCaps does not deploy, schedule, migrate or continuously monitor services. It provides a small discovery and verification layer that other tools can consume.

## Problem

Hosting compatibility is commonly hidden in provider documentation, private APIs, control-plane models or operator knowledge. A service may require a specific database version, persistent-storage property, network feature, runtime, security control or federation capability, but there is no compact, evidence-aware and provider-neutral interface for comparing those needs with the actual host.

The result is late failure: incompatibility is often discovered only during deployment or migration.

## Proposed documents

### Host Capability Manifest

A versioned document describing current host-side facts in categories such as:

- compute;
- storage;
- network and DNS;
- runtime and NixOS;
- databases;
- security and isolation;
- federation support;
- operational capabilities.

Claims may include evidence metadata:

- collection method: observed, configured, operator-declared or third-party;
- collection time and expiry;
- source or probe identity;
- public/private disclosure classification;
- optional integrity reference.

### Service Requirements Profile

A separate versioned document containing required and preferred constraints. It should remain independent of any provider or marketplace and support typed values, units, version semantics and namespaced extensions.

## Matching semantics

The baseline uses rule-level results and four report states:

- `compatible`: all required and preferred constraints pass;
- `compatible_with_warnings`: required constraints pass while one or more preferred constraints fail or remain unknown;
- `incompatible`: at least one required constraint fails;
- `unknown`: no required constraint is known to fail, but at least one required fact cannot be established from current evidence.

HostCaps must not silently convert missing or stale evidence into a pass.

## Discovery

The reference NixOS module currently demonstrates publication at:

```text
/.well-known/hostcaps
```

This is a proposed interoperability target, not a claim that an IANA well-known URI registration already exists. Community review should determine the final discovery and media-type path.

## Privacy and selective disclosure

A public document should expose the minimum facts necessary for matching. Internal hostnames, private addresses, rack identifiers, exact topology, credentials and unique hardware identifiers are not needed for most compatibility decisions.

The production design should compile public views from an internal manifest through schema-aware allow-list or deny-list policy, lint prohibited fields and test public fixtures for disclosure regressions.

## Trust boundaries

A signed claim is not automatically a true claim. HostCaps should distinguish authenticity, provenance and verification method:

- a signature can identify the publisher and protect integrity;
- evidence metadata explains how the fact was obtained;
- the matcher evaluates declared facts and evidence freshness;
- independent verification remains a separate policy decision.

No new cryptographic primitive is proposed.

## Interoperability boundaries

HostCaps is not a replacement for TOSCA, NetBox, Kubernetes, NixOS modules, Nix Fleet, NixEdgeOpt, cMonk, SelfPrivacy or hosting control planes. It is intended to provide a smaller host-side discovery and compatibility surface that those systems may publish or consume.

HostCaps is independent of ReproRestore. HostCaps evaluates pre-deployment host compatibility; ReproRestore verifies post-restore application reconstruction in a clean environment.

## Initial v1.0 scope

- reviewed Host Capability Manifest;
- reviewed Service Requirements Profile;
- typed core vocabulary and extension rules;
- evidence method and freshness semantics;
- safe NixOS collectors;
- public/private disclosure compiler;
- deterministic CLI and library;
- conformance suite;
- Forgejo, Nextcloud, Matrix Synapse and Mastodon profiles;
- documented TOSCA mapping;
- independent security review.

## Questions for reviewers

1. Which capability categories are essential for real placement or migration decisions?
2. Which facts should be observed rather than operator-declared?
3. How should units and version ranges be represented without creating an oversized ontology?
4. Is the four-state result model sufficient for schedulers and CI pipelines?
5. Which public fields create unnecessary security or privacy risk?
6. Should the discovery document expose evidence directly or by reference?
7. Which TOSCA, NetBox, NixOS or control-plane concepts require explicit mappings?
8. Which service profile would best demonstrate interoperability beyond the four initial examples?

## Review process

Feedback is requested through the repository RFC issue. Proposed changes should include a concrete use case, example manifest or requirement rule, expected ecosystem benefit and any disclosure or security implications.
