# Timer App
A simple Python GUI application that allows multiple timers to run simultaneously.

This project was created with the goal of **learning** how to package a Python application using Nix. It demonstrates (in a weird way) how to build, package, and use the application within the Nix ecosystem.

## Features
- Run multiple independent timers at once
- Pause, reset, and manage each timer individually
- Customizable timer names via pop-up windows

## Requirements
- Nix package manager (with flake support enabled)
- a `x86_64-linux` system at the moment.

## Installation
To add the `timer-app` as an input to your `flake.nix`, include the following configuration:

```nix
{
  inputs.timer-app = {
    url = "github:neocrz/timer-app";
    inputs.nixpkgs.follows = "nixpkgs";
  };
}
```

## Usage

After adding the timer-app as an input, you can use it as a package in your configuration by referencing it as follows:

```nix
{
  inputs.timer-app.packages.${system}.timer-app
}
```

Where `${system}` refers to your system architecture (at moment, support for `x86_64-linux` only).

You can also add `timer-app` to your `home.nix` under `home.packages` for easier access:

```nix

{
  home.packages = [
    inputs.timer-app.packages.${system}.timer-app
  ];
}
```

## Running the App

Once the `timer-app` is available as a package, run the app with the following command:

```bash
timer-app
```
