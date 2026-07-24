# Privacy and selective disclosure

A useful capability document does not need to reveal a machine's exact hardware serial number, internal hostname, rack position, private addresses or operator contact details.

HostCaps therefore distinguishes:

- an internal manifest containing detailed facts and evidence;
- one or more generated disclosure views;
- a public compatibility surface containing only the fields needed by external consumers.

The v0.1 policy removes explicitly listed paths. The funded implementation will add schema-aware classification, allow-list modes, disclosure linting and tests that fail when prohibited fields enter public fixtures.
