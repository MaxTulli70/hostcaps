{ config, lib, pkgs, ... }:

let
  cfg = config.services.hostcaps;
  manifestFile = pkgs.writeText "hostcaps-public.json" (builtins.toJSON cfg.publicManifest);
in
{
  options.services.hostcaps = {
    enable = lib.mkEnableOption "HostCaps public capability publication";

    domain = lib.mkOption {
      type = lib.types.str;
      example = "host.example.org";
      description = "Virtual host that publishes the HostCaps manifest.";
    };

    publicManifest = lib.mkOption {
      type = lib.types.attrs;
      default = { };
      description = "Public Host Capability Manifest. Do not include secrets or private topology identifiers.";
    };
  };

  config = lib.mkIf cfg.enable {
    services.nginx.enable = lib.mkDefault true;
    services.nginx.virtualHosts.${cfg.domain}.locations."= /.well-known/hostcaps" = {
      alias = manifestFile;
      extraConfig = ''
        default_type application/json;
        add_header Cache-Control "public, max-age=300";
        add_header X-Content-Type-Options "nosniff";
      '';
    };
  };
}
