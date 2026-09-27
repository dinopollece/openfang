---
name: obi-coordination
description: Coordinar tareas de Obi mediante fichas y resultados en archivos, creando especialistas por encargo.
---

# Coordinación de Obi

El workspace compartido contiene `project.md`, `templates/` y `tasks/`.
Para consultas simples respondé sin crear una tarea ni especialistas.

Para trabajo concreto:

1. Revisá `project.md` y la carpeta `tasks/` para no duplicar tareas. Creá `tasks/<id>/task.md` con objetivo, alcance, criterios y contexto seleccionado. Usá un id único y legible.
2. Creá `state.json` con task_id, status, active_attempt, agent_id, updated_at y next_action. Solo el director modifica este estado. Estados: todo, doing, awaiting_review, blocked, done.
3. Escribí `attempts/<intento>/assignment.md`: objetivo, criterios, referencias relativas al workspace, acceso a PC requerido, archivos permitidos y ruta de result.md. Terminá de escribir antes de delegar.
4. Leé `templates/<rol>.toml`, reemplazá `__AGENT_NAME__` con `obi-<rol>-<task-id>-<intento>` y usá `agent_spawn` con el TOML completo en manifest_toml. No cambies sus permisos. Roles: godot-worker, blender-worker, prototype-judge.
5. Guardá el agent_id devuelto en state.json. Enviá con `agent_send` el objetivo y la ruta del encargo, pidiendo result.md más un resumen. Crear el agente por sí solo no ejecuta el encargo.
6. Leé result.md y la evidencia antes de actualizar el estado. Un resultado sin pruebas suficientes queda pendiente. Creá un intento nuevo para la revisión si aporta valor; una corrección como máximo por defecto.

`agent_send` espera al trabajador. No uses ciclos de sondeo del director durante esa espera. Tras timeout inspeccioná el resultado/estado del agente antes de reenviar. Cada intento tiene un agente distinto para separar su contexto. Después de obtener y verificar su entrega, podés finalizar únicamente ese agente con agent_kill; conservá sus archivos y su ID en el estado.

El trabajador tiene el mismo workspace de coordinación en la Pi. Los archivos del juego viven en Windows y se consultan mediante `mcp_obipc_*`; no sirven las rutas de Windows con file_read de la Pi. Un solo implementador por checkout.

File_write no es transaccional: escribí archivos completos, releé state.json antes de continuar y tratá escrituras interrumpidas como recuperación pendiente. Los workers no deben editar state.json ni los insumos de un intento activo.

Cuotas: no delegues una revisión solo para confirmar un bloqueo de infraestructura ya demostrado. Pedí al juez que revise cuando haya propuesta o resultado evaluable. Conservá resultados breves y referencias; no releas toda la historia de intentos. Las imágenes MCP no llegan como visión en OpenFang 0.6.9: dejá la revisión visual al usuario y no certifiques apariencia con metadatos.
