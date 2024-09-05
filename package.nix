{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python310.withPackages (ps: with ps; [
    tkinter
    pygame
    # List any other dependencies you need here
  ]);

in pkgs.stdenv.mkDerivation {
  pname = "timer-app";
  version = "1.0";

  src = ./.;

  nativeBuildInputs = [ pkgs.python3 ];

  buildInputs = [
    pythonEnv
    pkgs.clang
    pkgs.llvmPackages.libcxx
    pkgs.ffmpeg
    pkgs.git
    pkgs.tcl
    pkgs.tk
  ];

  # Define the environment for the build phase
  shellHook = ''
    export VENV_DIR="$PWD/.venv"
    if [ ! -d "$VENV_DIR" ]; then
      ${pythonEnv}/bin/python -m venv $VENV_DIR
      source $VENV_DIR/bin/activate
      pip install --upgrade pip setuptools wheel
    else
      source $VENV_DIR/bin/activate
    fi

    export PYTHONPATH="${pythonEnv}/lib/python3.10/site-packages:$PYTHONPATH"
    export TCL_LIBRARY="${pkgs.tcl}/lib/tcl${pkgs.tcl.version}"
    export TK_LIBRARY="${pkgs.tk}/lib/tk${pkgs.tk.version}"

    if [ -f requirements.txt ]; then
      pip install -r requirements.txt --upgrade
    fi

    python --version
  '';

  buildPhase = ''
    mkdir -p $out/bin
    cp -r ./assets $out/bin
    cp -r ./timer $out/bin
    cp main.py $out/bin/timer-app
  '';

  installPhase = ''
    chmod +x $out/bin/timer-app
  '';

  meta = with pkgs.lib; {
    description = "Python GUI Timer System";
    license = licenses.mit;
    maintainers = with maintainers; [ your-name ];
    platforms = platforms.linux;
  };
}
