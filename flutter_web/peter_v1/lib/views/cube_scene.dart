import 'package:simple_3d/simple_3d.dart';
import 'package:util_simple_3d/util_simple_3d.dart';
import 'package:simple_3d_renderer/simple_3d_renderer.dart';

Sp3dWorld createCubeScene() {
  // Crear el rectángulo (cubo)
  final rectangle = UtilSp3dGeometry.cube(300, 200, 100, 1, 1, 1);

  // Configurar materiales para cada cara del rectángulo
  rectangle.materials.add(FSp3dMaterial.red.deepCopy());
  rectangle.materials.add(FSp3dMaterial.green.deepCopy());
  rectangle.materials.add(FSp3dMaterial.blue.deepCopy());
  rectangle.materials.add(FSp3dMaterial.orange.deepCopy());
  rectangle.materials.add(FSp3dMaterial.pink.deepCopy());
  rectangle.materials.add(FSp3dMaterial.blackNonWire.deepCopy());

  for (int i = 0; i < rectangle.fragments[0].faces.length; i++) {
    rectangle.fragments[0].faces[i].materialIndex = i;
  }

  // Crear las flechas (pilares)
  final arrowYaw = UtilSp3dGeometry.pillar(
    5,
    5,
    100,
    fragments: 16,
    isClosedBottom: true,
    isClosedTop: true,
    material: FSp3dMaterial.blue.deepCopy(),
  )..rotate(Sp3dV3D(1, 0, 0), -90 * 3.1416 / 180)
   ..move(Sp3dV3D(0, 100, 0));

  final arrowPitch = UtilSp3dGeometry.pillar(
    5,
    5,
    100,
    fragments: 16,
    isClosedBottom: true,
    isClosedTop: true,
    material: FSp3dMaterial.red.deepCopy(),
  )..rotate(Sp3dV3D(0, 1, 0), -90 * 3.1416 / 180)
   ..move(Sp3dV3D(250, 50, 0));

  final arrowRoll = UtilSp3dGeometry.pillar(
    5,
    5,
    100,
    fragments: 16,
    isClosedBottom: true,
    isClosedTop: true,
    material: FSp3dMaterial.green.deepCopy(),
  )..rotate(Sp3dV3D(0, 0, 1), -90 * 3.1416 / 180)
   ..move(Sp3dV3D(0, 50, 100));

  // Rotar el rectángulo
  rectangle.rotate(Sp3dV3D(1, 0, 0), -90 * 3.1416 / 180);

  // Crear el mundo que contiene el rectángulo y las flechas
  final world = Sp3dWorld([rectangle, arrowYaw, arrowPitch, arrowRoll]);

  return world;
}
