import 'package:flutter/material.dart';
import 'package:simple_3d/simple_3d.dart';
import 'package:simple_3d_renderer/simple_3d_renderer.dart';
import 'cube_scene.dart'; // Importar la escena del cubo

class ControlView extends StatefulWidget {
  const ControlView({super.key});

  @override
  State<ControlView> createState() => _ControlViewState();
}

class _ControlViewState extends State<ControlView> {
  late Sp3dWorld world; // Mundo 3D que contiene el cubo y las flechas
  bool isLoaded = false; // Estado de carga

  @override
  void initState() {
    super.initState();
    loadScene(); // Cargar la escena inicial
  }

  void loadScene() async {
    world = createCubeScene(); // Usar la función de `cube_scene.dart`
    await world.initImages(); // Inicializar imágenes (si hay)
    setState(() {
      isLoaded = true; // Marcar como cargado
    });
  }

  // Función para rotar el mundo en su totalidad
  void rotateWorld(Sp3dWorld world, Sp3dV3D axis, double angle) {
    for (var obj in world.objs) {
      obj.rotate(axis, angle); // Aplicar la nueva rotación
    }
    setState(() {}); // Actualizar la vista
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Panel de Control')),
      body: isLoaded
          ? Column(
              mainAxisAlignment: MainAxisAlignment
                  .spaceBetween, // Separar el contenido y el botón
              children: [
                // Contenido principal
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    // Texto al lado izquierdo
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Text(
                        "Descripción del Cubo",
                        style: Theme.of(context).textTheme.headlineMedium,
                      ),
                    ),
                    // Renderizador 3D con cubo reducido
                    Expanded(
                      child: Padding(
                        padding: const EdgeInsets.only(
                            top: 150), // Baja el cubo 50 píxeles
                        child: Center(
                          child: SizedBox(
                            width:
                                200, // Tamaño reducido del área de renderizado
                            height: 200,
                            child: Sp3dRenderer(
                              const Size(200, 200), // Tamaño reducido
                              const Sp3dV2D(100, 100), // Centro ajustado
                              world,
                              Sp3dCamera(
                                Sp3dV3D(0, 0,
                                    5000), // Alejar la cámara para que el cubo sea visible
                                6000,
                              ), // Cámara
                              Sp3dLight(
                                Sp3dV3D(0, 0, -1),
                                syncCam: true, // Sincronizar luz con la cámara
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
                // Botón al final de la pantalla
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: ElevatedButton(
                    onPressed: () {
                      rotateWorld(world, Sp3dV3D(0, 1, 0),
                          3.1416 / 4); // Rotar 45 grados en el eje z
                    },
                    child: const Text("Rotar Mundo"),
                  ),
                ),
              ],
            )
          : const Center(
              child: CircularProgressIndicator()), // Loader mientras se carga
    );
  }

  @override
  void dispose() {
    super.dispose();
  }
}
