---
name: godot-prototype-loop
description: Implementar y comprobar un incremento pequeño de Godot en la PC desde un encargo de Obi.
---

# Ciclo Godot

Leé el encargo con file_read (Pi). Para el proyecto Windows usá `mcp_obipc_status`, `files`, `read`, `diff` y `write` (los nombres completos llevan el prefijo `mcp_obipc_`). No confundas ambos filesystems.

`read` devuelve sha256; `write` requiere ese valor en expected_sha256 o NEW al crear. Solo permite scenes/, scripts/, assets/ y obi_checks/. Si el editor está abierto, las ediciones de escenas/scripts van por Beckett: consultá beckett_tools con el nombre de la operación antes de beckett_call. No fuerces una escritura sobre cambios del usuario.

Después de modificar escenas/scripts, ejecutá start_job con kind=godot_validate y un job_id único que incluya tarea/intento. Consultá job hasta estado terminal; esperá entre consultas y no crees un job distinto para el mismo reintento. Un resultado completed con log es evidencia de importación/parseo, no de jugabilidad. El runner pide cerrar Godot antes de validación headless; conservá primero trabajo sin guardar y pedí intervención si hace falta.

Si el editor está conectado podés inspeccionar árbol, ejecutar escena y pedir captura mediante Beckett. Si está cerrado, decí qué evidencia visual falta. Nunca afirmes haber jugado basándote solo en el log headless.

Guardá result.md en la Pi con resumen, archivos/hash, job_id y resultados, referencias a evidencia y limitaciones. Para evidencias grandes guardá un archivo acotado; no copies respuestas enteras innecesarias.

LIMITACIÓN VISUAL V1: OpenFang 0.6.9 devuelve MCP como texto. artifact confirma el archivo pero no permite ver sus píxeles; solicitá revisión humana del PNG. No envíes base64 como texto ni afirmes haber visto la imagen.
