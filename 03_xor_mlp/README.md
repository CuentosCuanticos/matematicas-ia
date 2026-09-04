# 03_xor_mlp

## Sesión 3 — XOR y el nacimiento de las redes neuronales

Carpeta oficial del laboratorio de la sesión 3 del curso **Matemáticas de la Inteligencia Artificial** de Cuentos Cuánticos.

[![Abrir en Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CuentosCuanticos/matematicas-ia/blob/main/03_xor_mlp/laboratorio.ipynb)

## Archivos

- `laboratorio.ipynb` — cuaderno de trabajo del alumno.

La solución completa, incluido el **problema final resuelto**, se mantiene exclusivamente en el repositorio privado `CuentosCuanticos/matematicas-ia-docente`.

## Entorno oficial

- Python
- NumPy
- Matplotlib
- Google Colab

Todavía no se utiliza PyTorch ni `autograd`. El laboratorio hace visible el paso del perceptrón a una red multicapa: XOR, no separabilidad lineal, activaciones no lineales, capa oculta, cambio de representación, anchura, profundidad y expresividad.

## Problema final

El alumno resuelve un **XOR simétrico** en cinco etapas: geometría, fracaso del perceptrón, diseño de una capa oculta ReLU, construcción de la capa de salida e interpretación del cambio de representación. La solución completa solo aparece en el cuaderno docente.

## Hito acumulativo

El alumno construye su primera red multicapa y comprende la cadena

\[
\text{XOR}\rightarrow\text{no separabilidad lineal}\rightarrow\text{no linealidad}\rightarrow\text{capa oculta}\rightarrow\text{nueva representación}\rightarrow\text{separación lineal}.
\]

La sesión termina dejando abierto el siguiente problema: sabemos que existen pesos adecuados, pero todavía no sabemos cómo encontrarlos automáticamente.
