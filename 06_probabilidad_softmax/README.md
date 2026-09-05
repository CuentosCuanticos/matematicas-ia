# 06_probabilidad_softmax

## Sesión 6 — Probabilidad, información y clasificación probabilística

Carpeta oficial del laboratorio de la sesión 6 del curso **Matemáticas de la Inteligencia Artificial** de Cuentos Cuánticos.

[![Abrir en Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CuentosCuanticos/matematicas-ia/blob/main/06_probabilidad_softmax/laboratorio.ipynb)

## Archivo

- `laboratorio.ipynb` — cuaderno de trabajo del alumno.

La solución completa, incluido el **problema final resuelto**, se mantiene exclusivamente en el repositorio privado `CuentosCuanticos/matematicas-ia-docente`.

## Entorno oficial

- Python
- NumPy
- Matplotlib
- Google Colab

Todavía no se utiliza PyTorch ni `autograd`. La sesión construye explícitamente probabilidades conjuntas, marginales y condicionadas; la regla de Bayes; Bernoulli y máxima verosimilitud; logit y sigmoide; distribución categórica; softmax estable; cross-entropy; divergencia KL; el gradiente `p-y`; y un clasificador probabilístico multiclase entrenado desde cero.

## Problema final

El alumno resuelve un problema integrado de tres clases en el que debe:

- estimar priors y probabilidades condicionadas a partir de frecuencias;
- aplicar Bayes y comprobar el posterior mediante conteos;
- construir un clasificador softmax lineal con NumPy;
- implementar cross-entropy y sus gradientes;
- entrenar los parámetros mediante descenso de gradiente;
- visualizar las regiones de decisión;
- inspeccionar distribuciones predichas en puntos ambiguos;
- distinguir probabilidad del modelo de certeza factual.

## Hito acumulativo

Al terminar la sesión queda construido el ciclo

\[
x\rightarrow z\rightarrow q_\theta(y\mid x)\rightarrow -\log q_\theta(y_{\rm observado}\mid x)\rightarrow \nabla_\theta L\rightarrow \text{actualización}.
\]

La sesión 7 introducirá optimización moderna, generalización, separación train/validation/test y la transición de los gradientes manuales a `autograd` en PyTorch.
