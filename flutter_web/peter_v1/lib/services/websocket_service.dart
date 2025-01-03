import 'package:web_socket_channel/web_socket_channel.dart';

class WebSocketService {
  late WebSocketChannel _channel;

  void connect(
    String url,
    void Function(dynamic)? onMessage, // Corregido: dynamic para mensajes
    void Function(Object)? onError,   // Corregido: Object para errores
    void Function()? onDone,          // Corregido: función vacía para finalizar
  ) {
    _channel = WebSocketChannel.connect(Uri.parse(url));

    _channel.stream.listen(
      onMessage,
      onError: onError,
      onDone: onDone,
    );
  }

  void sendMessage(String message) {
    _channel.sink.add(message);
  }

  void disconnect() {
    _channel.sink.close();
  }
}
