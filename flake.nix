{
  description = "HostCaps provider-neutral capability discovery baseline";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in {
      packages = forAllSystems (system:
        let pkgs = import nixpkgs { inherit system; };
        in {
          default = pkgs.python3Packages.buildPythonApplication {
            pname = "hostcaps";
            version = "0.1.0";
            pyproject = true;
            src = ./.;
            nativeBuildInputs = [ pkgs.python3Packages.setuptools ];
          };
        });

      checks = forAllSystems (system:
        let pkgs = import nixpkgs { inherit system; };
        in {
          tests = pkgs.runCommand "hostcaps-tests" {
            nativeBuildInputs = [ self.packages.${system}.default ];
          } ''
            export HOME=$TMPDIR
            export PYTHONPATH=${self}/src
            cd ${self}
            ${pkgs.python3}/bin/python -m unittest discover -s tests -v
            touch $out
          '';
        });

      nixosModules.default = import ./nix/module.nix;
    };
}
