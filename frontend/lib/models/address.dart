class Address {
  final String id;
  final String addressLine;
  final String? phoneNumber;
  final String? addressCategory;
  final String? addressTag;

  const Address({
    required this.id,
    required this.addressLine,
    this.phoneNumber,
    this.addressCategory,
    this.addressTag,
  });

  factory Address.fromJson(Map<String, dynamic> json) => Address(
        id: json['id'] as String,
        addressLine: json['addressLine'] as String,
        phoneNumber: json['phoneNumber'] as String?,
        addressCategory: json['addressCategory'] as String?,
        addressTag: json['addressTag'] as String?,
      );

  String get displayTitle => addressTag?.isNotEmpty == true ? addressTag! : addressCategory ?? 'Address';
}
