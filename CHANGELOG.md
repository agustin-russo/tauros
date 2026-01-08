# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.0.1] - 2025-12-10
### Added
- Generación de mapas con Perlin noise.
- Normalización básica de alturas.
- Interfaz PySide6 mínima para visualizar mapas.
- Semilla manual para reproducibilidad.
- Estructura inicial del motor.

### Known Issues
- Render lento en mapas grandes.

---


## [1.0.0] - 2025-12-11
### Added
- Implementación de Perlin Noise basada en el artículo de Adrian Biagioli.
- Optimización completa del renderizado del mapa usando `numpy` + `QImage`.
- Ahora se pueden generar y pintar mundos de 2048×1024 píxeles en ~1 segundo.
- Mejora en el manejo de colores y transparencia (canal alpha).

### Fixed
- Render lento en mapas grandes.

---

## [1.1.0] - 2025-1-08
### Added
- Mejora en la UI, más personalización y cambios estéticos.
- Creación de los mapas de humedad, temperatura y biomas para más realismo.
- Cambios en la UI para ver los distintos mapas nuevos.
- Leve perdida de velocidad, casi imperceptible, por los nuevos cambios en mapas muy grandes.

---