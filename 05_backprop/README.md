# 05_backprop

## Sesión 5 — Backpropagation: la regla de la cadena convertida en algoritmo

Carpeta oficial del laboratorio de la sesión 5 del curso **Matemáticas de la Inteligencia Artificial** de Cuentos Cuánticos.

[![Abrir en Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CuentosCuanticos/matematicas-ia/blob/main/05_backprop/laboratorio.ipynb)

## Archivo

- `laboratorio.ipynb` — cuaderno de trabajo del alumno.

La solución completa, incluido el **problema final resuelto**, se mantiene exclusivamente en el repositorio privado `CuentosCuanticos/matematicas-ia-docente`.

## Entorno oficial

- Python
- NumPy
- Matplotlib
- Google Colab

Todavía no se utiliza PyTorch ni `autograd`: el objetivo es construir explícitamente el grafo computacional, el *forward pass*, el *backward pass*, los gradientes matriciales, el `gradient checking` y el entrenamiento de una MLP mediante backpropagation manual.

## Problema final

El alumno construye y entrena desde cero una red `2 → 3 → 1` para resolver XOR. Debe:

- implementar `forward` y `backward` exclusivamente con NumPy;
- comprobar gradientes mediante diferencias finitas;
- separar backpropagation de la actualización de parámetros;
- representar la curva de pérdida y las regiones de decisión;
- analizar las normas de gradiente y la saturación de `tanh`;
- explicar qué parte del proceso automatizará posteriormente `autograd`.

## Hito acumulativo

Al terminar la sesión queda construido, sin diferenciación automática, el ciclo

\[
\text{datos}
\rightarrow
\text{forward}
\rightarrow
L
\rightarrow
\text{backpropagation}
\rightarrow
\nabla_\theta L
\rightarrow
\text{actualización}.
\]

La sesión 6 introducirá la necesidad de que la red aprenda distribuciones de probabilidad y conducirá a logits, softmax, entropía y *cross-entropy*.
