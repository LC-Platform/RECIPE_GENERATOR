import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Stepper Example')),
        body: StepperExample(),
      ),
    );
  }
}

class StepperExample extends StatefulWidget {
  @override
  _StepperExampleState createState() => _StepperExampleState();
}

class _StepperExampleState extends State<StepperExample> {
  int _currentStep = 0;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Stepper(
        currentStep: _currentStep,
        onStepTapped: (int step) {
          setState(() {
            _currentStep = step;
          });
        },
        onStepContinue: () {
          if (_currentStep < 2) {
            setState(() {
              _currentStep++;
            });
          }
        },
        onStepCancel: () {
          if (_currentStep > 0) {
            setState(() {
              _currentStep--;
            });
          }
        },
        steps: [
          Step(
            title: Text('Step 1'),
            content: Column(
              children: <Widget>[
                Text('Content for Step 1'),
                TextField(
                  decoration: InputDecoration(labelText: 'Enter something'),
                ),
              ],
            ),
          ),
          Step(
            title: Text('Step 2'),
            content: Column(
              children: <Widget>[
                Text('Content for Step 2'),
                TextField(
                  decoration: InputDecoration(labelText: 'Enter something else'),
                ),
              ],
            ),
          ),
          Step(
            title: Text('Step 3'),
            content: Column(
              children: <Widget>[
                Text('Content for Step 3'),
                TextField(
                  decoration: InputDecoration(labelText: 'Enter more details'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
