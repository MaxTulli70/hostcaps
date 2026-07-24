# HostCaps v0.1.0

Initial public pre-grant baseline for provider-neutral hosting capability discovery and compatibility matching for NixOS services.

## Included

- draft Host Capability Manifest schema;
- draft Service Requirements Profile schema;
- installable Python library and CLI;
- structural validation and deterministic JSON fingerprints;
- policy-based public/private redaction;
- deterministic compatibility matching;
- explicit `compatible`, `compatible_with_warnings`, `incompatible` and `unknown` outcomes;
- evidence methods and freshness checks;
- public and private host examples;
- Forgejo, Nextcloud, Matrix Synapse and Mastodon profiles;
- NixOS publication module baseline for `/.well-known/hostcaps`;
- automated tests, GitHub Actions CI and Nix flake checks;
- public RFC, threat model, privacy model, milestones and acceptance criteria.

## Scope

This release proves the pre-existing technical baseline. It does not yet include the reviewed v1.0 specifications, production collectors, typed units and version ranges, disclosure compiler, conformance suite, integration adapters or independent security review proposed for the funded work.

## Verification

```bash
python -m pip install -e .
hostcaps validate host examples/host-public.json
hostcaps validate profile profiles/forgejo.json
hostcaps match examples/host-public.json profiles/forgejo.json
hostcaps fingerprint examples/host-public.json
hostcaps redact examples/host-private.json examples/public-view-policy.json
python -m unittest discover -s tests -v
nix flake check
```

## Licence

Apache License 2.0.
