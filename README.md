# PR2 - Tipología y Ciclo de Vida de los Datos (Máster de Ciencia de Datos - UOC)

Este repositorio contiene la resolución de la Práctica 2 (PR2) de la asignatura Tipología y Ciclo de Vida de los Datos, perteneciente al Máster Universitario en Ciencia de Datos de la Universitat Oberta de Catalunya (UOC).

El objetivo de la práctica es el análisis y modelado de un conjunto de datos del portal inmobiliario Idealista, con el fin de construir un sistema capaz de estimar el valor de los inmuebles en función de sus características.

Estructura del repositorio

.
├── data/
│ └── [Archivos de datos utilizados en el análisis]
├── sources/
│ └── [Funciones y scripts auxiliares en R]
├── Resolucion-PR2.qmd # Documento Quarto con el análisis
├── Resolucion-PR2.html # Versión renderizada del informe
├── flake.nix # Entorno reproducible con Nix
├── flake.lock # Lockfile del entorno Nix
├── .envrc # Configuración para direnv
└── .gitignore # Archivos ignorados por Git

# Requisitos previos

La manera más sencilla de ejecutar correctamente el proyecto requiere lo siguiente:

- Tener instalado [Nix](https://nixos.org/download.html) con soporte para Nix Flakes.
- Tener instalado [direnv](https://direnv.net/docs/installation.html).
- Tener instalado [Quarto](https://quarto.org/docs/get-started/).

# Instrucciones de ejecución

1. Clonar el repositorio

```bash
git clone https://github.com/acpuchades/uoc-tcvd-pr2.git
cd uoc-tcvd-pr2
```

2. Permitir la carga del entorno con direnv

```bash
direnv allow
```

Esto activará automáticamente el entorno definido en .envrc y flake.nix.

3. Renderizar el informe

```bash
nix run .#render
```

Esto generará el archivo Resolucion-PR2.html con el informe completo de análisis y resultados.

4. (opcional) Ejecutar el notebook de manera interactiva

```bash
nix run .#rstudio
```

# Notas

- El análisis se ha realizado parcialmente con R y Python de manera integrada en el archivo `Resolucion-PR2.qmd`.
- La gestión del entorno con Nix garantiza la reproducibilidad del entorno de ejecución.
- Para cumplir con los requerimientos, se ha extraído el código necesario para ejecutar la mayor parte del análisis de manera independiente. Los archivos de código fuente se encuentran en el directorio `sources`.
