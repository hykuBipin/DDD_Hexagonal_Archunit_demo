import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config.dart';
import '../models/address.dart';
import '../models/restaurant.dart';
import 'auth_service.dart';

class ApiService {
  static final _client = http.Client();

  static Future<Map<String, String>> get _headers async {
    final token = await AuthService.accessToken;
    return {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  static Future<List<Address>> getAddresses() async {
    final uri = Uri.parse('$backendBaseUrl/api/addresses');
    final response = await _client.get(uri, headers: await _headers);
    _checkStatus(response, 'getAddresses');
    final List<dynamic> json = jsonDecode(response.body) as List<dynamic>;
    return json
        .map((e) => Address.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  static Future<MatchResponse> matchRestaurants(
    List<String> preferences,
    String addressId,
  ) async {
    final uri = Uri.parse('$backendBaseUrl/api/match');
    final body = jsonEncode({'preferences': preferences, 'addressId': addressId});
    final response = await _client.post(uri, headers: await _headers, body: body);
    _checkStatus(response, 'matchRestaurants');
    return MatchResponse.fromJson(
        jsonDecode(response.body) as Map<String, dynamic>);
  }

  static void _checkStatus(http.Response response, String op) {
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception('$op failed: HTTP ${response.statusCode}\n${response.body}');
    }
  }
}
