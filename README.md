A thing to format and print Pathfinder creatures and items on a receipt printer
to make them easy to hand out, reference, annotate, etc.

Assumptions
-----------

* Uses data files from [pf2e](https://github.com/foundryvtt/pf2e) and assumes
you have it checked out locally somewhere.
* Uses nix for dependencies, run `nix-shell` or use
[direnv](https://github.com/direnv/direnv).
* Prints to a network printer supported by
[python-escpos](https://github.com/python-escpos/python-escpos).

Usage
-----

Example usage:
```shell
# preview in console
./print-item --json ~/3src/pf2e/packs/pf2e/equipment/healing-potion-lesser.json
./print-creature --json ~/3src/pf2e/pathfinder-monster-core/mitflit.json --details

# preview what will be sent to printer
./print-creature --json .../thing.json --details --preview

# actually send to printer
./print-creature --json .../thing.json --details --printer 192.168.1.123
```

Written hastily and experimental.  Please don't judge code quality.
