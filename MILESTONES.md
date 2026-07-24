# HostCaps delivery milestones and acceptance criteria

This document separates the public v0.1 baseline from the proposed funded v1.0 work. Pre-existing code and proposal preparation are not charged to the grant.

## Baseline B0 — public pre-grant evidence

Status: implemented.

Acceptance evidence:

- public repository and Apache-2.0 licence;
- Host Capability Manifest and Service Requirements Profile drafts;
- installable Python CLI and library;
- deterministic matching with explicit `compatible`, `compatible_with_warnings`, `incompatible` and `unknown` outcomes;
- evidence-freshness handling;
- policy-based public/private redaction;
- canonical fingerprints;
- Forgejo, Nextcloud, Matrix Synapse and Mastodon profiles;
- automated tests, Nix flake, NixOS module baseline and CI;
- reproducible demo instructions.

## M1 — Core specifications and public review

Target: months 1–2.

Outputs:

- Host Capability Manifest draft;
- Service Requirements Profile draft;
- typed core vocabulary, units and version rules;
- extension and namespace policy;
- public RFC round and disposition log.

Acceptance criteria:

- every core field has defined semantics, type, disclosure classification and example;
- required/preferred constraints and every supported operator have conformance fixtures;
- missing and stale evidence semantics are normative;
- specification and reference implementation agree on the conformance corpus;
- external review comments and dispositions are public.

## M2 — Safe NixOS collectors and evidence model

Target: months 2–4.

Outputs:

- reviewed read-only collector framework;
- collectors for core compute, storage, network, runtime and database capabilities;
- evidence provenance and freshness model;
- collector permission and failure policy.

Acceptance criteria:

- collectors run without arbitrary shell hooks in the core profile;
- every emitted observed fact identifies collector, timestamp and source class;
- collection failures produce explicit unknown facts or diagnostics, never fabricated defaults;
- test fixtures cover unavailable commands, denied permissions, malformed output and stale evidence;
- collectors disclose no credentials, private addresses or unique hardware identifiers in public mode.

## M3 — Public/private disclosure compiler

Target: months 3–5.

Outputs:

- schema-aware allow-list and deny-list disclosure policies;
- disclosure linting;
- internal and public manifest generation;
- privacy regression fixtures.

Acceptance criteria:

- public views are generated rather than manually edited;
- prohibited-field fixtures fail CI;
- removed fields and policy version are recorded in disclosure metadata;
- equivalent input and policy produce deterministic public output;
- internal topology and operator contact data are absent from public conformance fixtures.

## M4 — Production matcher, CLI and library

Target: months 4–6.

Outputs:

- typed matcher library;
- stable CLI;
- units, version ranges and namespaced extensions;
- deterministic machine-readable compatibility reports.

Acceptance criteria:

- all required constraints pass before `compatible` is emitted;
- missing or stale required facts result in `unknown`, not `compatible`;
- failed required constraints result in `incompatible`;
- preferred issues result in `compatible_with_warnings`;
- reports provide rule-level actual, expected, evidence and reason fields;
- equivalent inputs produce reports without volatile ordering noise.

## M5 — Discovery profile and conformance suite

Target: months 5–7.

Outputs:

- HTTP discovery and caching profile;
- media-type proposal or documented fallback;
- NixOS publication module;
- independent conformance suite;
- integration examples for a scheduler, deployment tool or hosting catalogue.

Acceptance criteria:

- a clean NixOS deployment publishes a valid public document at the configured discovery location;
- cache and expiry semantics are testable;
- the conformance suite runs without ONMAKE infrastructure;
- at least one external-style consumer example parses and uses a report through the public interface;
- standards-track identifiers are described as proposals until formally registered.

## M6 — Maintained service profiles

Target: months 6–7.

Outputs:

- Forgejo profile;
- Nextcloud profile;
- Matrix Synapse profile;
- Mastodon profile;
- profile authoring guide.

Acceptance criteria:

- every profile identifies supported application version or range;
- every requirement is linked to a documented operational need;
- fixtures include compatible, incompatible and unknown host cases;
- profile changes are versioned and covered by tests;
- no profile embeds provider-specific commercial assumptions.

## M7 — Security review, mappings, documentation and v1.0 release

Target: month 8.

Outputs:

- independent security review and remediation log;
- documented mapping to relevant TOSCA concepts;
- integration and operator documentation;
- accessibility-reviewed HTML documentation;
- tagged v1.0 release and post-grant roadmap.

Acceptance criteria:

- no unresolved critical or high-severity review finding at release;
- medium findings have remediation or documented disposition;
- all Python and Nix checks pass in CI;
- documentation enables a new contributor to publish a sanitised host manifest and evaluate all four service profiles from a clean checkout;
- the v1.0 release has no proprietary dependency or required central registry.

## Cross-project independence

HostCaps does not depend on ReproRestore, LINKALL, xTdC or other proprietary ONMAKE systems. No funded hour or output may be charged to another proposal. Optional future integrations must preserve independent operation and the Apache-2.0 licence.
