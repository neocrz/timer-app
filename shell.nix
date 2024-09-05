{ pkgs ? import <nixpkgs> {} }:

let
  pythonWithTk = pkgs.python310.buildEnv.override {
    extraLibs = with pkgs.python310Packages; [
      tkinter
      pip
      virtualenv
      pygame
      pyinstaller
    ];
    ignoreCollisions = true;
  };
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    pythonWithTk
    clang
    llvmPackages.libcxx
    cmake
    pkg-config
    ffmpeg
    git
    tcl
    tk
  ];

  shellHook = ''
    export VENV_DIR="$PWD/.venv"
    if [ ! -d "$VENV_DIR" ]; then
      ${pythonWithTk}/bin/python -m venv $VENV_DIR
      source $VENV_DIR/bin/activate
      pip install --upgrade pip setuptools wheel
    else
      source $VENV_DIR/bin/activate
    fi

    export PYTHONPATH="${pythonWithTk}/lib/python3.10/site-packages:$PYTHONPATH"
    export TCL_LIBRARY="${pkgs.tcl}/lib/tcl${pkgs.tcl.version}"
    export TK_LIBRARY="${pkgs.tk}/lib/tk${pkgs.tk.version}"

    pip install --upgrade "onnxruntime-silicon==1.13.1"

    if [ -f requirements.txt ]; then
      pip install -r requirements.txt --upgrade
    fi

    python --version
  '';
}
