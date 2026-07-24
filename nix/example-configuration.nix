{ ... }:
{
  imports = [ ./module.nix ];

  services.hostcaps = {
    enable = true;
    domain = "host.example.org";
    publicManifest = builtins.fromJSON (builtins.readFile ../examples/host-public.json);
  };
}
