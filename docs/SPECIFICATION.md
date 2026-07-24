# HostCaps v0.1 specification notes

## Design principles

- small core vocabulary with namespaced extensions;
- explicit distinction between declared, configured, observed and third-party evidence;
- deterministic matching with no hidden scoring model;
- required and preferred constraints;
- `unknown` is distinct from `fail`;
- public disclosure is a generated view, not the raw internal inventory;
- no central registry is required for basic use;
- no new cryptographic primitive.

## Capability categories

The baseline uses compute, storage, network, runtime, databases, security, federation and operations. Additional keys are permitted so experiments do not require a new release. The funded v1.0 work will define extension and namespace rules.

## Requirement operators

The baseline implements equality, inequality, numeric bounds, containment, existence and minimum-version matching. The production specification will define version semantics, units, typed values and conformance fixtures more rigorously.

## Status model

- `compatible`: every required and preferred rule passes;
- `compatible_with_warnings`: required rules pass, but a preferred rule fails or is unknown;
- `incompatible`: at least one required rule fails;
- `unknown`: no required rule fails, but at least one required rule cannot be evaluated from current evidence.
