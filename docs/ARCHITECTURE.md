# Architecture

HostCaps separates five responsibilities:

1. **Capability collection** - read-only probes and explicit NixOS configuration produce candidate facts.
2. **Evidence and disclosure** - each claim can identify its source, collection method and age; a disclosure policy creates public and private views.
3. **Publication** - a compact JSON document is served locally or through a proposed well-known HTTP location.
4. **Requirements** - service authors publish independent profiles containing required and preferred constraints.
5. **Matching** - a deterministic engine evaluates a host against a profile and emits a machine-readable report.

```text
NixOS configuration + read-only probes
                |
                v
     Host Capability Manifest
                |
     disclosure / evidence policy
                |
                v
       public discovery document  <---  Service Requirements Profile
                |                                  |
                +--------------- matcher ----------+
                                   |
                                   v
                         Compatibility Evidence
```

The architecture intentionally excludes deployment, scheduling and continuous monitoring. Consumers may use the compatibility report as an input to those systems.
