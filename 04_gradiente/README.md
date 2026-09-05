# 04_gradiente

## Sesión 4 — Funciones de pérdida, derivadas y descenso de gradiente

Carpeta oficial del laboratorio de la sesión 4 del curso **Matemáticas de la Inteligencia Artificial** de Cuentos Cuánticos.

[![Abrir en Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CuentosCuanticos/matematicas-ia/blob/main/04_gradiente/laboratorio.ipynb)

## Archivos

- `laboratorio.ipynb` — cuaderno de trabajo del alumno.

La solución completa, incluido el **problema final resuelto**, se mantiene exclusivamente en el repositorio privado `CuentosCuanticos/matematicas-ia-docente`.

## Entorno oficial

- Python
- NumPy
- Matplotlib
- Google Colab

Todavía no se utiliza PyTorch ni `autograd`: el objetivo es implementar explícitamente función de pérdida, derivadas, gradiente, Hessiano, diferencias finitas y descenso de gradiente.

## Problema final

El alumno entrena desde cero una neurona logística bidimensional. Debe implementar el *score*, la pérdida logística media, el gradiente analítico, `gradient checking`, descenso de gradiente, comparación de varios `learning rates`, frontera de decisión e interpretación del aprendizaje.

## Hito acumulativo

La sesión deja construido el ciclo

\[
\text{modelo}\rightarrow\mathcal L(\theta)\rightarrow\nabla\mathcal L(\theta)\rightarrow\theta_{n+1}=\theta_n-\eta\nabla\mathcal L(\theta_n).
\]

La siguiente sesión responderá al problema abierto: cómo calcular eficientemente todos los gradientes de una red multicapa mediante **backpropagation**.
