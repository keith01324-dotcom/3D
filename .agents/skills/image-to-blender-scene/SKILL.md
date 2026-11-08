---
name: image-to-blender-scene
description: Convert reference images into editable Blender scenes using image analysis, independent mesh assets, bpy assembly and multi-view verification. Use for image-to-scene reconstruction and Blender scene refinement.
---

# Image to Blender scene

Read docs/setup.md in this repository for environment and provider constraints. Run scripts/build_scene.py with a scene plan, then scripts/check_scene.py in a fresh process. These scripts use bpy without a GUI or API key.

1. Inspect reference images. Write a scene plan with meter units, known scale anchors, reference camera, named objects, independent meshes, materials and semantic collections. Record uncertain dimensions and hidden surfaces separately from observations. A single photo cannot establish exact scale or hidden geometry. Prefer calibrated overlapping photos when accuracy matters.
2. Build architecture and rough object placement first. Match perspective and silhouettes before detail. Generate or obtain complex objects individually as GLB assets and record provenance and licenses. Obtain authorization for image uploads and paid generation. Generated alternate views are hypotheses, never ground truth.
3. Keep architecture, furniture, props, lights and cameras in distinct named collections. Keep objects editable. A textured plane, fused whole-scene mesh or Gaussian splat alone does not satisfy this goal. Complete backs and thickness where the camera can travel, marking inferred areas.
4. Assemble with bpy. Check imported asset scale, axes, floor contact and materials. Save to a new absolute path, pack textures, and preserve any existing user project. CPU rendering is the fallback; enable GPU only after testing support.
5. Render the reference camera and at least three alternate views. Inspect geometry, appearance and occlusions. Reopen the saved blend in a fresh process and check expected objects, meshes, collections, materials, cameras, transforms and missing textures. Structural validation does not prove reference accuracy.
6. Deliver blend, previews, validation JSON, asset provenance and limitations. State exactly which inference, visual comparison and cloud jobs were actually performed. The included example plan is only a runtime smoke test.

Use token-saver when available. Request compact object summaries before detailed queries, store full inventories on disk, and never print mesh vertices or base64 assets into context. Keep a concise progress file for long builds. Do not remove evidence needed to debug errors.

For interactive MCP editing, separately install Blender GUI and the reviewed addon; connect the local socket before enabling the MCP config. A bpy wheel does not supply a GUI or running addon. For cloud batch jobs use bpy directly rather than exposing a Blender socket to the Internet.
