{
	description = "Reproducible R environment with Nix flake";

	inputs = {
		nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
		flake-utils.url = "github:numtide/flake-utils";
	};

	outputs = { nixpkgs, flake-utils, ... }:
		flake-utils.lib.eachDefaultSystem (system:
		let
			pkgs = import nixpkgs { inherit system; };
			r-packages = with pkgs.rPackages; [
				caret
				ggplot2
				naniar
				quarto
				reticulate
				stopwords
				tidytext
				tidyverse
				wordcloud2
			];
			r-with-packages = pkgs.rWrapper.override { packages = r-packages; };
			python-with-packages = pkgs.python3.withPackages (ps: with ps; [
				matplotlib
				pandas
				rpy2
				scikit-learn
				seaborn
				statsmodels
			]);
			rstudio-with-packages = pkgs.rstudioWrapper.override { packages = r-packages; };
			render-cmd = pkgs.writeShellApplication {
				name = "render";
				runtimeInputs = [
					pkgs.pandoc
					pkgs.texliveFull
					python-with-packages
					r-with-packages
				];
				text = ''
					${r-with-packages}/bin/Rscript -e "quarto::quarto_render('Resolucion-PR2.qmd')"
				'';
			};
			rstudio-cmd = pkgs.writeShellApplication {
				name = "rstudio";
				runtimeInputs = [
					rstudio-with-packages
					python-with-packages
				];
				text = ''
					${rstudio-with-packages}/bin/rstudio ./Resolucion-PR2.qmd
				'';
			};
		in {
			devShells.default = pkgs.mkShell {
				packages = [
					r-with-packages
					rstudio-with-packages
					python-with-packages
				];

				shellHook = ''
					export RETICULATE_PYTHON=${python-with-packages}/bin/python3
					echo "RETICULATE_PYTHON set to $RETICULATE_PYTHON"
				'';
			};
			apps.rstudio = {
				type = "app";
				program = "${rstudio-cmd}/bin/rstudio";
			};
			apps.render = {
				type = "app";
				program = "${render-cmd}/bin/render";
			};
		});
}
