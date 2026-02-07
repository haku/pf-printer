{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = with pkgs; [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      markdownify
      python-escpos
      requests
      rich
      stransi
    ]))
  ];
}
