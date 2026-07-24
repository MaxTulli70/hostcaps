# HostCaps v0.1 reproducible demo

This demo exercises the public pre-grant baseline: manifest validation, service-profile validation, deterministic compatibility matching, fingerprints, privacy redaction and automated tests.

## Requirements

- Python 3.11 or later; or
- Nix with flakes enabled.

## Python path

```bash
git clone https://github.com/MaxTulli70/hostcaps.git
cd hostcaps
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .

hostcaps validate host examples/host-public.json
hostcaps validate profile profiles/forgejo.json
hostcaps match examples/host-public.json profiles/forgejo.json
hostcaps fingerprint examples/host-public.json
hostcaps redact examples/host-private.json examples/public-view-policy.json \
  --output /tmp/hostcaps-public.json
python -m unittest discover -s tests -v
```

Expected baseline behaviour:

- both documents validate;
- the Forgejo example produces a deterministic compatibility report;
- fingerprints remain stable across JSON key ordering;
- the public view removes configured private fields;
- the automated test suite passes;
- missing required capabilities produce `unknown` rather than a silent pass;
- failed required constraints produce `incompatible`.

## Nix path

```bash
git clone https://github.com/MaxTulli70/hostcaps.git
cd hostcaps
nix flake check
```

The repository also includes a baseline NixOS module in `nix/module.nix` and a sample configuration in `nix/example-configuration.nix`.

## What this demo proves

The v0.1 baseline already demonstrates:

- two separate machine-readable document types;
- dependency-free structural validation;
- deterministic rule-level matching;
- explicit pass, fail and unknown handling;
- evidence-age checks;
- public/private disclosure redaction;
- canonical SHA-256 document fingerprints;
- four service requirement profiles;
- Python and Nix CI paths.

It does not yet prove production-grade host collectors, signed evidence, a stable discovery registration, complete typed units or integration with external control planes. Those are funded v1.0 targets and have separate acceptance criteria in `MILESTONES.md`.

## Reporting a result

When opening an issue, include:

- operating system and architecture;
- Python or Nix version;
- exact command;
- complete error output;
- tested commit SHA;
- a sanitised fixture that contains no internal addresses, credentials or unique infrastructure identifiers.
