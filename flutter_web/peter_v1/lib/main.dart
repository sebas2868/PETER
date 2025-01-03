import 'package:flutter/material.dart';
import 'views/initialview.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Robot Control',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const InitialView(),
    );
  }
}
