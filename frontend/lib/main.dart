import 'package:app_links/app_links.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'services/auth_service.dart';

void main() {
  runApp(const OrderTogetherApp());
}

class OrderTogetherApp extends StatelessWidget {
  const OrderTogetherApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Order Together',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        textTheme: GoogleFonts.poppinsTextTheme(),
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFFC8019),
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      home: const _AuthGate(),
    );
  }
}

class _AuthGate extends StatefulWidget {
  const _AuthGate();

  @override
  State<_AuthGate> createState() => _AuthGateState();
}

class _AuthGateState extends State<_AuthGate> {
  final _appLinks = AppLinks();
  late final Future<bool> _authCheck;
  bool? _loggedIn;

  @override
  void initState() {
    super.initState();
    _authCheck = AuthService.isLoggedIn;

    _appLinks.uriLinkStream.listen(_handleDeepLink);

    _appLinks.getInitialLink().then((uri) {
      if (uri != null) _handleDeepLink(uri);
    });
  }

  void _handleDeepLink(Uri uri) async {
    if (uri.scheme == 'com.ordertogether' && uri.host == 'auth') {
      final token = uri.queryParameters['token'];
      if (token != null && token.isNotEmpty) {
        await AuthService.saveToken(token);
        if (mounted) setState(() => _loggedIn = true);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loggedIn != null) {
      return _loggedIn! ? const HomeScreen() : const LoginScreen();
    }

    return FutureBuilder<bool>(
      future: _authCheck,
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const Scaffold(
            backgroundColor: Color(0xFFFC8019),
            body: Center(
              child: CircularProgressIndicator(color: Colors.white),
            ),
          );
        }
        return snapshot.data! ? const HomeScreen() : const LoginScreen();
      },
    );
  }
}
