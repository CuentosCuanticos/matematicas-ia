# Proyecto final — EinsteinBot

Práctica acumulativa del curso **Matemáticas de la Inteligencia Artificial**.

El objetivo es construir desde cero un pequeño modelo de lenguaje causal especializado en un corpus de Relatividad General y convertirlo en un chatbot experimental. No se utiliza ningún LLM preentrenado ni una API externa: embeddings, self-attention causal, bloque Transformer, entrenamiento, generación y adaptación conversacional se trabajan explícitamente.

[![Abrir EinsteinBot en Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CuentosCuanticos/matematicas-ia/blob/main/proyecto_final_einsteinbot/EinsteinBot.ipynb)

## Recorrido

1. Preparar un corpus autorizado de Relatividad General.
2. Tokenizar y construir el vocabulario.
3. Formar el dataset causal de predicción del siguiente token.
4. Implementar self-attention a partir de Q, K, V, producto matricial, escala, máscara causal y softmax.
5. Ensamblar y entrenar un mini-Transformer decoder-only.
6. Medir cross-entropy y perplexity.
7. Generar texto con temperatura y top-k.
8. Continuar el entrenamiento con un pequeño corpus conversacional.
9. Comparar el modelo de dominio con el modelo adaptado al diálogo.
10. Construir una recuperación léxica elemental y un modo prudente con abstención.

## Importante sobre los datos

No subas a este repositorio libros o materiales con copyright sin autorización. Para la entrega utiliza textos de dominio público, materiales con licencia compatible, apuntes propios o fuentes para las que tengas permiso. El notebook incorpora un corpus de demostración redactado específicamente para la práctica, suficiente para verificar todo el pipeline.

## Entrega

El notebook del estudiante contiene tareas `TODO`, comprobaciones y preguntas de interpretación. La entrega final debe incluir el cuaderno ejecutado, procedencia/licencia del corpus, curvas de aprendizaje, perplexity, ejemplos de generación, evaluación de errores y alucinaciones, comparación antes/después de la adaptación conversacional y el diseño del **EinsteinBot prudente**.

La idea conceptual de cierre es distinguir entre **modelo**, **algoritmo de decodificación** y **sistema alrededor del modelo**, y comprobar experimentalmente que modelar lenguaje no equivale a disponer de un criterio de verdad.
