# DoVi Games — contexto de Obi

Prototipo de aprendizaje. Idea, nombre y mecánicas pueden cambiar. Godot 4.7.2 estándar/GDScript; Blender 5.2.2 LTS en Windows. Priorizamos escena, movimiento, interacción, comprobación y prueba con el equipo. Explicar nodos/scripts y evitar sistemas grandes antes de probar la mecánica.

## Hosts y herramientas

- Pi: workspace de coordinación, tareas y resultados. file_read/file_write operan aquí.
- Windows: checkout `C:\DoVi Games`, Godot y Blender. Acceso con MCP obipc a través de SSH. Usar rutas relativas al proyecto en esas herramientas.
- Beckett Lite está instalado. Sus herramientas requieren el editor abierto; comprobar disponibilidad, nunca asumirla. Los puertos/credenciales quedan dentro del puente.
- Blender funciona en background con scripts reproducibles; no se instaló un addon MCP de Blender.
- Si la PC está apagada o el túnel está caído, se puede planificar pero no ejecutar ni verificar allí.

Leer AGENTS.md de Windows con mcp_obipc_read antes de implementar; es la referencia vigente. Inspeccionar estado/diff y respetar cambios sin guardar. Después de editar escenas/scripts: validar Godot headless; para cambios visuales obtener captura/revisión humana. Conservar .blend, .glb y scripts usados.

## Coordinación

Tareas en tasks/<id>/task.md y state.json; encargos/resultados en attempts/<id>/. El director escribe el estado global. Los especialistas trabajan por encargo y no delegan. Un solo implementador del checkout. El juez revisa criterios y evidencia; el equipo valida sensación de control/diversión.

Modelos: GPT-6 Sol con medium a través de la ruta de LiteLLM probada. Los límites de OpenFang son límites locales, no un saldo de Plus. No mantener agentes ejecutando trabajo periódico ni cargar conversaciones completas sin necesidad.

Plantillas de spawn revisadas en templates/godot-worker.toml, templates/blender-worker.toml y templates/prototype-judge.toml. Solo reemplazar __AGENT_NAME__ por un nombre único.
