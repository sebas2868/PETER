import 'package:flutter/material.dart';
import 'loadingview.dart';

class InitialView extends StatelessWidget {
  const InitialView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Robot Control')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const LoadingView()),
            );
          },
          child: const Text('Conectar'),
        ),
      ),
    );
  }
}
