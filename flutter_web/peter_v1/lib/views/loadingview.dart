import 'package:flutter/material.dart';
import 'controlview.dart';
import '../services/websocket_service.dart';
import '../views/initialview.dart';
import 'dart:convert'; // Agrega esta línea

class LoadingView extends StatefulWidget {
  const LoadingView({super.key});

  @override
  LoadingViewState createState() => LoadingViewState();
}

class LoadingViewState extends State<LoadingView> {
  final WebSocketService _webSocketService = WebSocketService();
  String _statusMessage = 'Conectando...';
  bool _isConnected = false; // Indica si la conexión inicial fue exitosa.

  @override
  void initState() {
    super.initState();
    _connectToApi();
  }

Future<void> _connectToApi() async {
  try {
    _webSocketService.connect(
      'ws://192.168.1.84:8765/ws',
      (message) {
        try {
          final Map<String, dynamic> decodedMessage = jsonDecode(message);
          if (decodedMessage['message'] == 'CONFIRMATION') {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (context) => const ControlView()),
            );
          }
        } catch (e) {
          print('Error decodificando el mensaje: $e');
        }
      },
      (error) {
        // Navegar de vuelta a la pantalla inicial
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const InitialView()),
        );
      },
      () {
        // Navegar de vuelta a la pantalla inicial
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const InitialView()),
        );
      },
    );

    // Actualiza el estado cuando la conexión se establece
    setState(() {
      _isConnected = true;
      _statusMessage = 'Conexión con la API exitosa';
    });
  } catch (e) {
    setState(() {
      _statusMessage = 'Error al conectar: $e';
    });

    // Navegar de vuelta a la pantalla inicial
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => const InitialView()),
    );
  }
}

  @override
  void dispose() {
    _webSocketService.disconnect();
    super.dispose();
  }

 @override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(title: const Text('Cargando')),
    body: Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (_isConnected)
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  _statusMessage,
                  style: const TextStyle(fontSize: 18, color: Colors.green),
                ),
                const SizedBox(width: 10), // Espacio entre el texto y el ícono
                const Icon(
                  Icons.check_circle,
                  color: Colors.green,
                  size: 30,
                ),
              ],
            )
          else
            Column(
              children: [
                const CircularProgressIndicator(),
                const SizedBox(height: 40),
                Text(
                  _statusMessage,
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          const SizedBox(height: 40),
          if (_isConnected)
            const Text(
              'Esperando mensaje de confirmación...',
              style: TextStyle(fontSize: 16),
            ),
        ],
      ),
    ),
  );
}
}