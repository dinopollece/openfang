---
name: blender-game-asset
description: Crear assets simples con Blender en background, conservar fuente y script, y exportar GLB para Godot.
---

# Asset Blender

Trabajá con el encargo y herramientas `mcp_obipc_*`. El runner de Blender está disponible en Windows; no hay un addon MCP para editar la sesión de Blender abierta.

Prepará un script .py bajo assets/<encargo>/ o obi_checks/<prueba>/ mediante write (NEW para un archivo nuevo). El script usa bpy y os.environ['OBI_OUTPUT_DIR'] para todos sus resultados. Guardá .blend mediante bpy.ops.wm.save_as_mainfile y .glb mediante bpy.ops.export_scene.gltf(export_format='GLB'). Conservá el script de generación.

Lanzá start_job con kind=blender_script, job_id único, script_path y output_dir relativos al proyecto. El runner utiliza --background --factory-startup y --python-exit-code 1. Ejecuta Python con permisos del usuario: no es un sandbox. Limitá el script a la tarea, sus archivos y bpy; no hagas red ni instales dependencias.

Consultá job y comprobá los archivos con files. Para inspección visual generá un PNG pequeño y consultalo con artifact si el encargo lo requiere. Luego comprobá importación con un job godot_validate o dejá explícita la necesidad de validación por Godot.

Entregá en result.md (Pi) rutas del script, .blend, .glb, captura si aplica, dimensiones/origen acordados, job IDs, comprobaciones y limitaciones. No inventes un límite de polígonos ni certifiques un aspecto visual sin verlo.

LIMITACIÓN VISUAL V1: OpenFang 0.6.9 devuelve MCP como texto. artifact confirma el archivo pero no permite ver sus píxeles; solicitá revisión humana del PNG. No envíes base64 como texto ni afirmes haber visto la imagen.
