{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = with pkgs; [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      flask
      gunicorn
      markdownify
      pillow
      python-escpos
      requests
      rich
      stransi
    ]))
  ];
}
