# Changelog
Todos los cambios notables de este proyecto serán documentados en este archivo.

Formato basado en Keep a Changelog  
Versionado Semántico (SemVer).

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
