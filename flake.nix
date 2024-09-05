{
  description = "Python GUI Timer System";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
      };
    in {
      devShells.${system}.default = import ./shell.nix { inherit pkgs; };

      packages.${system} = {
        # Set `timer-app` as the default package
        default = import ./package.nix { inherit pkgs; };
        timer-app = import ./package.nix { inherit pkgs; };
      };
    };
}
