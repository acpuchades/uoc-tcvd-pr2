# PR2 - Tipología y Ciclo de Vida de los Datos (Máster de Ciencia de Datos - UOC)

Este repositorio contiene la resolución de la Práctica 2 (PR2) de la asignatura Tipología y Ciclo de Vida de los Datos, perteneciente al Máster Universitario en Ciencia de Datos de la Universitat Oberta de Catalunya (UOC).

El objetivo de la práctica es el análisis y modelado de un conjunto de datos del portal inmobiliario Idealista, con el fin de construir un sistema capaz de estimar el valor de los inmuebles en función de sus características.

El tratamiento de los datos se ha realizado de manera integrada por parte de ambos integrantes del equipo:

- Alejandro Caravaca Puchades
- Andrea Vigo Ruíz

# Estructura del repositorio

```
.
├── data/
│ └── idealista-sale-properties-spain.csv
├── output/
│ └── idealista-sale-properties-spain_processed.csv
├── sources/
│ ├── data_pipeline.py # Pipeline Scikit-Learn con preprocesamiento adicional
│ ├── idealista-data.r # Preprocesamiento de los datos en R
│ ├── idealista_data.py # Carga de los datos tras la imputación
│ ├── stat_tests.py # Pruebas estadísticas de los datos en Python
│ ├── supervised_models.py # Modelos supervisados de Scikit-Learn
│ └── unsupervised_models.py # Modelos no supervisados de Scikit-Learn
├── Resolucion-PR2.qmd # Documento Quarto con el análisis
├── Resolucion-PR2.html # Versión renderizada del informe
├── flake.nix # Entorno reproducible con Nix
├── flake.lock # Lockfile del entorno Nix
├── .envrc # Configuración para direnv
└── .gitignore # Archivos ignorados por Git
```

# Requisitos previos

La manera más sencilla de ejecutar correctamente el proyecto requiere lo siguiente:

- Tener instalado [Nix](https://nixos.org/download.html) con soporte para Nix Flakes.
- Tener instalado [direnv](https://direnv.net/docs/installation.html).
- Tener instalado [Quarto](https://quarto.org/docs/get-started/).

Alternativamente, se requiere tener instalados los siguientes paquetes:

**Código en R**:

- caret
- ggplot2
- missRanger
- naniar
- quarto
- reticulate
- stopwords
- tidytext
- tidyverse
- wordcloud2

**Código en Python**:

- matplotlib
- pandas
- rpy2
- scikit-learn
- seaborn
- statsmodels

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
