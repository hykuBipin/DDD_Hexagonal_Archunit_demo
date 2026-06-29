import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Stores and retrieves the Swiggy access token received via the deep link
/// after the server-side OAuth PKCE flow completes.
class AuthService {
  static const _storage = FlutterSecureStorage();
  static const _keyAccessToken = 'swiggy_access_token';

  static Future<String?> get accessToken => _storage.read(key: _keyAccessToken);

  static Future<bool> get isLoggedIn async =>
      (await _storage.read(key: _keyAccessToken)) != null;

  /// Called from main.dart when the app receives the deep link
  /// com.ordertogether://auth?token=ACCESS_TOKEN
  static Future<void> saveToken(String token) =>
      _storage.write(key: _keyAccessToken, value: token);

  static Future<void> logout() => _storage.delete(key: _keyAccessToken);
}
