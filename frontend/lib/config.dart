// Backend base URL.
// Android emulator: 10.0.2.2 routes to the host machine's localhost.
// For a real device or when using ngrok, override with:
//   flutter run --dart-define=BACKEND_URL=https://xxxx.ngrok-free.app
// ignore: do_not_use_environment
const String backendBaseUrl = String.fromEnvironment(
  'BACKEND_URL',
  defaultValue: 'http://10.0.2.2:8080',
);
